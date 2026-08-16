import uuid
import json
import logging
import os
from datetime import datetime
import boto3
from botocore.exceptions import ClientError
from src.common.models import RequestPayload

logger = logging.getLogger("tf.request_intake.service")
logger.setLevel(logging.INFO)

s3 = boto3.client("s3")
ddb = boto3.client("dynamodb")
eb = boto3.client("events")


def _now_iso():
    return datetime.utcnow().isoformat() + "Z"


def _put_raw(bucket: str, request_id: str, payload: RequestPayload):
    key = f"raw/{request_id}.json"
    body = json.dumps(payload.dict(), default=str)
    logger.info("Persisting raw payload to S3", extra={"bucket": bucket, "key": key})
    s3.put_object(Bucket=bucket, Key=key, Body=body.encode("utf-8"))
    return key


def _create_idempotency_record(table: str, event_id: str, request_id: str):
    # Use a conditional write to ensure single processing for same event_id
    now = _now_iso()
    try:
        ddb.put_item(
            TableName=table,
            Item={
                "event_id": {"S": event_id},
                "request_id": {"S": request_id},
                "status": {"S": "RECEIVED"},
                "created_at": {"S": now}
            },
            ConditionExpression="attribute_not_exists(event_id)"
        )
        logger.info("Idempotency record created", extra={"event_id": event_id})
        return True
    except ClientError as e:
        if e.response.get("Error", {}).get("Code") == "ConditionalCheckFailedException":
            logger.warning("Duplicate event detected", extra={"event_id": event_id})
            return False
        logger.exception("DynamoDB put_item failed")
        raise


def _emit_request_received(event_bus: str, request_id: str, correlation_id: str, payload: RequestPayload):
    detail = {
        "request_id": request_id,
        "correlation_id": correlation_id,
        "customer_id": payload.customer_id,
        "channel": payload.channel,
        "received_at": _now_iso()
    }
    logger.info("Publishing RequestReceived event to EventBridge", extra={"bus": event_bus, "detail": detail})
    eb.put_events(Entries=[{
        "Source": "telcoflow.nexus",
        "DetailType": "RequestReceived",
        "Detail": json.dumps(detail),
        "EventBusName": event_bus
    }])


def process_request(payload: RequestPayload, raw_bucket: str, idempotency_table: str, event_bus: str):
    # generate ids
    request_id = payload.request_id or f"req-{uuid.uuid4()}"
    correlation_id = payload.correlation_id or f"corr-{uuid.uuid4()}"

    payload.request_id = request_id
    payload.correlation_id = correlation_id

    # Persist raw payload
    raw_key = _put_raw(raw_bucket, request_id, payload)

    # Idempotency: guard with event id (use correlation_id as proxy)
    created = _create_idempotency_record(idempotency_table, correlation_id, request_id)
    if not created:
        return {"status": "duplicate", "request_id": request_id, "correlation_id": correlation_id}

    # Emit domain event
    _emit_request_received(event_bus, request_id, correlation_id, payload)

    return {
        "status": "accepted",
        "request_id": request_id,
        "correlation_id": correlation_id,
        "raw_key": raw_key
    }

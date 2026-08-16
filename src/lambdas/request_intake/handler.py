import os
import logging
from src.common.models import RequestPayload
from .service import process_request

logger = logging.getLogger("tf.request_intake")
logger.setLevel(logging.INFO)

RAW_BUCKET = os.getenv("RAW_REQUEST_BUCKET", "tf-nexus-dev-raw-requests")
IDEMPOTENCY_TABLE = os.getenv("IDEMPOTENCY_TABLE", "tf-nexus-dev-idempotency")
EVENT_BUS = os.getenv("EVENT_BUS", "telcoflow-nexus-events")


def lambda_handler(event, context):
    """Lambda entrypoint for request intake. Expects API Gateway, SQS or adapter event.

    Responsibilities:
    - validate minimal schema
    - generate request_id and correlation_id if missing
    - persist raw payload to S3
    - create idempotency record in DynamoDB
    - emit RequestReceived event to EventBridge
    - return a lightweight ack with request_id and correlation_id
    """
    logger.info("Received event", extra={"event_source": event.get("source") if isinstance(event, dict) else 'unknown'})
    payload = RequestPayload(
        request_id=event.get("request_id"),
        correlation_id=event.get("correlation_id"),
        customer_id=event.get("customer_id"),
        channel=event.get("channel", "api"),
        body=event.get("body", {})
    )

    result = process_request(payload, raw_bucket=RAW_BUCKET, idempotency_table=IDEMPOTENCY_TABLE, event_bus=EVENT_BUS)
    return result

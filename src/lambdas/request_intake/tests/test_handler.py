import json
import os
from moto import mock_s3, mock_dynamodb2, mock_events
import boto3
import pytest

from src.lambdas.request_intake.handler import lambda_handler


@mock_s3
@mock_dynamodb2
@mock_events
def test_lambda_handler_accepts_event(monkeypatch):
    # Setup mocked S3
    s3 = boto3.client("s3", region_name="us-east-1")
    s3.create_bucket(Bucket="tf-nexus-dev-raw-requests")

    # Setup mocked DynamoDB
    ddb = boto3.client("dynamodb", region_name="us-east-1")
    ddb.create_table(TableName='tf-nexus-dev-idempotency', KeySchema=[{'AttributeName':'event_id','KeyType':'HASH'}], AttributeDefinitions=[{'AttributeName':'event_id','AttributeType':'S'}], BillingMode='PAY_PER_REQUEST')

    # Setup mocked EventBridge
    eb = boto3.client('events', region_name='us-east-1')

    event = {
        'customer_id': 'cust-123',
        'body': {'text': 'Internet is down'},
        'channel': 'portal'
    }

    result = lambda_handler(event, {})
    assert result['status'] in ('accepted', 'duplicate')
    assert 'request_id' in result
    assert 'correlation_id' in result

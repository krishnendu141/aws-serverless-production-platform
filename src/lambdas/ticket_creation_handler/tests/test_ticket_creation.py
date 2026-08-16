from moto import mock_dynamodb2
import boto3
from src.lambdas.ticket_creation_handler.service import create_ticket
from src.common.models import RequestPayload

@mock_dynamodb2
def test_create_ticket_writes_ddb():
    ddb = boto3.client('dynamodb', region_name='us-east-1')
    ddb.create_table(TableName='tf-nexus-dev-tickets', KeySchema=[{'AttributeName':'ticket_id','KeyType':'HASH'}], AttributeDefinitions=[{'AttributeName':'ticket_id','AttributeType':'S'}], BillingMode='PAY_PER_REQUEST')

    payload = RequestPayload(request_id='req-1', correlation_id='c1', customer_id='cust', channel='portal', body={'priority':'P2','sla_deadline':'2026-01-01T00:00:00Z'})
    out = create_ticket(payload, table='tf-nexus-dev-tickets')
    assert out['status'] == 'OPEN'
    assert out['ticket_id'].startswith('TCK-')

import uuid
import logging
from datetime import datetime
import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger("tf.ticket_creation.service")
logger.setLevel(logging.INFO)

ddb = boto3.client('dynamodb')


def _now_iso():
    return datetime.utcnow().isoformat() + 'Z'


def create_ticket(payload, table: str):
    ticket_id = f"TCK-{uuid.uuid4()}"
    item = {
        'ticket_id': {'S': ticket_id},
        'request_id': {'S': payload.request_id},
        'status': {'S': 'OPEN'},
        'priority': {'S': payload.body.get('priority','P4')},
        'created_at': {'S': _now_iso()},
        'sla_deadline': {'S': payload.body.get('sla_deadline','')}
    }
    try:
        ddb.put_item(TableName=table, Item=item)
        logger.info('Ticket created', extra={'ticket_id': ticket_id})
        return {'ticket_id': ticket_id, 'status': 'OPEN'}
    except ClientError:
        logger.exception('Failed to create ticket')
        raise

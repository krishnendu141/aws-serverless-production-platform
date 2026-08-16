import logging
import os
from src.common.models import RequestPayload
from .service import create_ticket

logger = logging.getLogger("tf.ticket_creation")
logger.setLevel(logging.INFO)

TICKETS_TABLE = os.getenv('TICKETS_TABLE', 'tf-nexus-dev-tickets')


def lambda_handler(event, context):
    payload = RequestPayload(**event)
    ticket = create_ticket(payload, table=TICKETS_TABLE)
    return ticket

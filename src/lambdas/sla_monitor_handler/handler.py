import logging
from .service import evaluate_slas
from src.common.models import RequestPayload

logger = logging.getLogger("tf.sla_monitor")
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    # event may contain a list of tickets (for tests) or be invoked as scheduled check
    tickets = event.get('tickets') if isinstance(event, dict) else None
    return evaluate_slas(tickets)

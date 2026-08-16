import logging
from src.common.models import RequestPayload
from .service import calculate_priority

logger = logging.getLogger("tf.priority_calculator")
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    payload = RequestPayload(**event)
    result = calculate_priority(payload)
    return result

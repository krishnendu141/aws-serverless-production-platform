import logging
from src.common.models import RequestPayload
from .service import calculate_sla

logger = logging.getLogger("tf.sla_calculator")
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    payload = RequestPayload(**event)
    res = calculate_sla(payload)
    return res

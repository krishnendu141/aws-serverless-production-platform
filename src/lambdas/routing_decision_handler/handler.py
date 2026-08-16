import logging
from src.common.models import RequestPayload
from .service import decide_routing

logger = logging.getLogger("tf.routing_decision")
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    payload = RequestPayload(**event)
    return decide_routing(payload)

import logging
from src.common.models import RequestPayload
from .service import classify

logger = logging.getLogger("tf.request_classifier")
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    payload = RequestPayload(**event)
    result = classify(payload)
    return result

import logging
from src.common.models import RequestPayload
from .service import normalize_request

logger = logging.getLogger("tf.request_normalizer")
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    # event expected to contain request payload or S3 pointer
    payload = RequestPayload(**event)
    result = normalize_request(payload)
    return result

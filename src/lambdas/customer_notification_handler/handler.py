import logging
from .service import notify_customer

logger = logging.getLogger("tf.customer_notification")
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    result = notify_customer(event)
    return result

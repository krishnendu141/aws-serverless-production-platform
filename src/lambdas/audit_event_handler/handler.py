import logging
from .service import record_audit

logger = logging.getLogger("tf.audit_event")
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    return record_audit(event)

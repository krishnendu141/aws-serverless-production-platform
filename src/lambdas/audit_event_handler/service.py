import logging
from src.common.models import AuditEvent

logger = logging.getLogger("tf.audit_event.service")
logger.setLevel(logging.INFO)


def record_audit(event: dict):
    # In production: validate schema and write to DynamoDB table 'audit'
    audit = AuditEvent(**event)
    logger.info('Audit recorded', extra={'event_type': audit.event_type, 'entity_id': audit.entity_id})
    return {'status': 'recorded', 'event_type': audit.event_type}

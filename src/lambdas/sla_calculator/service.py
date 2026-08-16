from datetime import datetime, timedelta
import logging
from src.common.models import RequestPayload

logger = logging.getLogger("tf.sla_calculator.service")
logger.setLevel(logging.INFO)

SLA_RULES = {
    'P1': 15,   # minutes
    'P2': 60,
    'P3': 8*60,
    'P4': 24*60
}


def calculate_sla(payload: RequestPayload):
    priority = payload.body.get('priority') or payload.body.get('classification',{}).get('priority','P4')
    minutes = SLA_RULES.get(priority, 24*60)
    deadline = datetime.utcnow() + timedelta(minutes=minutes)
    logger.info('Calculated SLA', extra={'request_id': payload.request_id, 'priority': priority, 'deadline': deadline.isoformat()})
    return {'request_id': payload.request_id, 'priority': priority, 'sla_minutes': minutes, 'sla_deadline': deadline.isoformat() + 'Z'}

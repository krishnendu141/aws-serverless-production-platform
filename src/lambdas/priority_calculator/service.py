import logging
from src.common.models import RequestPayload

logger = logging.getLogger("tf.priority_calculator.service")
logger.setLevel(logging.INFO)


def calculate_priority(payload: RequestPayload):
    # Combine classification priority with customer tier heuristics
    classification = payload.body.get('classification') or {}
    base_priority = classification.get('priority', 'P4')
    customer_tier = payload.body.get('customer_tier', 'residential')

    if customer_tier == 'enterprise' and base_priority in ('P2','P3','P4'):
        logger.info('Bumping priority for enterprise customer', extra={'request_id': payload.request_id})
        return {'priority': 'P1', 'reason': 'enterprise_customer'}

    return {'priority': base_priority, 'reason': 'rules'}

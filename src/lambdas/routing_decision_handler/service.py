import logging
from src.common.models import RequestPayload

logger = logging.getLogger("tf.routing_decision.service")
logger.setLevel(logging.INFO)

ROUTE_MAP = {
    'BILLING': 'billing-routing-queue',
    'NETWORK': 'network-routing-queue',
    'ENTERPRISE': 'enterprise-support-queue',
    'MOBILE': 'customer-service-routing-queue',
    'GENERAL': 'customer-service-routing-queue'
}


def decide_routing(payload: RequestPayload):
    category = (payload.body or {}).get('classification',{}).get('category') or 'GENERAL'
    queue = ROUTE_MAP.get(category, 'customer-service-routing-queue')
    logger.info('Routing decision', extra={'request_id': payload.request_id, 'queue': queue})
    return {'request_id': payload.request_id, 'route_queue': queue}

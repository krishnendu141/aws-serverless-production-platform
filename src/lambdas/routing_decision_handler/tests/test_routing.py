from src.lambdas.routing_decision_handler.service import decide_routing
from src.common.models import RequestPayload


def test_routing_network():
    payload = RequestPayload(request_id='r1', correlation_id='c1', customer_id='cust', channel='portal', body={'classification': {'category':'NETWORK'}})
    out = decide_routing(payload)
    assert out['route_queue'] == 'network-routing-queue'


def test_routing_default():
    payload = RequestPayload(request_id='r2', correlation_id='c2', customer_id='cust', channel='portal', body={})
    out = decide_routing(payload)
    assert out['route_queue'] == 'customer-service-routing-queue'

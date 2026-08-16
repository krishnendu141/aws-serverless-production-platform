from src.lambdas.priority_calculator.service import calculate_priority
from src.common.models import RequestPayload


def test_enterprise_promotes_to_p1():
    payload = RequestPayload(request_id='r1', correlation_id='c1', customer_id='cust', channel='portal', body={'classification': {'priority':'P3'}, 'customer_tier':'enterprise'})
    out = calculate_priority(payload)
    assert out['priority'] == 'P1'


def test_residential_keeps_priority():
    payload = RequestPayload(request_id='r2', correlation_id='c2', customer_id='cust', channel='portal', body={'classification': {'priority':'P3'}, 'customer_tier':'residential'})
    out = calculate_priority(payload)
    assert out['priority'] == 'P3'

from src.lambdas.sla_calculator.service import calculate_sla
from src.common.models import RequestPayload


def test_sla_p1():
    payload = RequestPayload(request_id='r1', correlation_id='c1', customer_id='cust', channel='portal', body={'priority':'P1'})
    out = calculate_sla(payload)
    assert out['sla_minutes'] == 15


def test_sla_default():
    payload = RequestPayload(request_id='r2', correlation_id='c2', customer_id='cust', channel='portal', body={})
    out = calculate_sla(payload)
    assert out['sla_minutes'] == 24*60

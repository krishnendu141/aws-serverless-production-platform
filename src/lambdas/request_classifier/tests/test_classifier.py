from src.lambdas.request_classifier.service import classify
from src.common.models import RequestPayload


def test_rules_match_network():
    payload = RequestPayload(request_id='r1', correlation_id='c1', customer_id='cust', channel='portal', body={'text':'My internet is down since 9AM'})
    out = classify(payload)
    assert out['category'] == 'NETWORK'
    assert out['intent'] == 'OUTAGE'
    assert out['confidence'] >= 0.9


def test_fallback_low_confidence():
    payload = RequestPayload(request_id='r2', correlation_id='c2', customer_id='cust', channel='portal', body={'text':'I have a question about my plan'})
    out = classify(payload)
    assert out['category'] == 'GENERAL'
    assert out['confidence'] < 0.9

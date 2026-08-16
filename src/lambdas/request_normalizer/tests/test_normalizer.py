from src.lambdas.request_normalizer.service import _normalize_text, normalize_request
from src.common.models import RequestPayload


def test_normalize_text_basic():
    assert _normalize_text("  Hello \n WORLD ") == "hello world"


def test_normalize_request_adds_normalized():
    payload = RequestPayload(request_id='req-1', correlation_id='corr-1', customer_id='c1', channel='portal', body={'text':'Internet is DOWN since 10AM'})
    out = normalize_request(payload)
    assert 'normalized_text' in payload.body
    assert payload.body['normalized_text'].startswith('internet is down')

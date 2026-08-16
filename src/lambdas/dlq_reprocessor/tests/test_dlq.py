from src.lambdas.dlq_reprocessor.service import reprocess_dlq_item


def test_retryable():
    item = {'id':'i1','failure_reason':'Timeout while calling downstream'}
    out = reprocess_dlq_item(item)
    assert out['action'] == 'retry'


def test_quarantine():
    item = {'id':'i2','failure_reason':'Invalid payload format'}
    out = reprocess_dlq_item(item)
    assert out['action'] == 'quarantine'

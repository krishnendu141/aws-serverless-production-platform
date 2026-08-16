from src.lambdas.email_request_adapter.handler import lambda_handler\n\ndef test_stub():\n    out = lambda_handler({'test':true}, {})\n    assert out['status'] == 'ok'\n

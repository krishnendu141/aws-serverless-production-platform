from src.lambdas.team_notification_handler.handler import lambda_handler\n\ndef test_stub():\n    out = lambda_handler({'test':true}, {})\n    assert out['status'] == 'ok'\n

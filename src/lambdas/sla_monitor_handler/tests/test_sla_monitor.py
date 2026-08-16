from datetime import datetime, timedelta
from src.lambdas.sla_monitor_handler.service import evaluate_slas


def test_sla_warning_and_breach():
    now = datetime.utcnow()
    tickets = [
        {'ticket_id':'t1','sla_deadline': (now + timedelta(minutes=10)).isoformat()+'Z'},
        {'ticket_id':'t2','sla_deadline': (now - timedelta(minutes=1)).isoformat()+'Z'},
        {'ticket_id':'t3','sla_deadline': (now + timedelta(hours=2)).isoformat()+'Z'}
    ]
    out = evaluate_slas(tickets)
    assert out['warnings'] == 1
    assert out['breaches'] == 1

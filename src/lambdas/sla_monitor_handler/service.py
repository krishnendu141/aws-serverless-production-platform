from datetime import datetime, timedelta
import logging

logger = logging.getLogger("tf.sla_monitor.service")
logger.setLevel(logging.INFO)


def evaluate_slas(tickets=None):
    """Evaluate a list of ticket dicts for warning/breach. If tickets is None, this function would scan the DB in a full implementation."""
    warnings = []
    breaches = []
    now = datetime.utcnow()
    if not tickets:
        return {"warnings": 0, "breaches": 0}

    for t in tickets:
        sla_deadline = datetime.fromisoformat(t.get('sla_deadline').replace('Z',''))
        delta = (sla_deadline - now).total_seconds()
        if delta <= 0:
            breaches.append(t['ticket_id'])
        elif delta <= 15*60:
            warnings.append(t['ticket_id'])

    logger.info('SLA evaluation completed', extra={'warnings': len(warnings), 'breaches': len(breaches)})
    return {'warnings': len(warnings), 'breaches': len(breaches), 'warning_ids': warnings, 'breach_ids': breaches}

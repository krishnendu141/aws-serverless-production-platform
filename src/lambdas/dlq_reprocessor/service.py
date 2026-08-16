import logging

logger = logging.getLogger("tf.dlq_reprocessor.service")
logger.setLevel(logging.INFO)

RETRYABLE_ERRORS = ['Throttling', 'Timeout', 'Transient']


def reprocess_dlq_item(item: dict):
    reason = item.get('failure_reason','')
    if any(err.lower() in reason.lower() for err in RETRYABLE_ERRORS):
        # re-enqueue logic would be here
        logger.info('DLQ item retryable', extra={'item': item.get('id')})
        return {'action': 'retry', 'id': item.get('id')}
    else:
        # quarantine
        logger.info('DLQ item non-retryable, quarantining', extra={'item': item.get('id')})
        return {'action': 'quarantine', 'id': item.get('id')}

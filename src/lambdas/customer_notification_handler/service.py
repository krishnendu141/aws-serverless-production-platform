import logging

logger = logging.getLogger("tf.customer_notification.service")
logger.setLevel(logging.INFO)


def notify_customer(event: dict):
    # In production: publish to SNS topic with templating; here we log for demonstration
    logger.info('Notify customer', extra={'to': event.get('customer_id')})
    return {'status': 'notified', 'customer_id': event.get('customer_id')}

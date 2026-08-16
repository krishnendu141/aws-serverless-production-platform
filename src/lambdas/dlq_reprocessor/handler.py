import logging
from .service import reprocess_dlq_item

logger = logging.getLogger("tf.dlq_reprocessor")
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    # event is expected to include 'records' or single failure item
    item = event.get('item') or event
    return reprocess_dlq_item(item)

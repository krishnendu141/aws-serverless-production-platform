import logging
from .service import aggregate_metrics

logger = logging.getLogger("tf.metrics_aggregation")
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    return aggregate_metrics(event.get('metrics', []))

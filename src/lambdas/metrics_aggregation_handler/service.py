import statistics
import logging

logger = logging.getLogger("tf.metrics_aggregation.service")
logger.setLevel(logging.INFO)


def aggregate_metrics(metrics):
    # metrics: list of numeric values or dicts with 'latency'
    latencies = []
    for m in metrics:
        if isinstance(m, dict) and 'latency' in m:
            latencies.append(m['latency'])
        elif isinstance(m, (int, float)):
            latencies.append(m)
    if not latencies:
        return {'count': 0}
    return {'count': len(latencies), 'avg': statistics.mean(latencies), 'p95': statistics.quantiles(latencies, n=100)[94]}

import logging
import json

logger = logging.getLogger("tf.request_intake.utils")


def safe_json(obj):
    try:
        return json.dumps(obj, default=str)
    except Exception:
        logger.exception("Failed to JSON-serialize object")
        return "{}\n"

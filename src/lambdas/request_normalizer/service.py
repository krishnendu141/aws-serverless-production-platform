import re
import logging
from typing import Dict
from src.common.models import RequestPayload

logger = logging.getLogger("tf.request_normalizer.service")
logger.setLevel(logging.INFO)


def _normalize_text(text: str) -> str:
    if not text:
        return ""
    # simple normalization: lower, collapse whitespace, remove unusual control chars
    text = text.lower()
    text = re.sub(r"\s+", " ", text).strip()
    text = re.sub(r"[\x00-\x1f]+", "", text)
    return text


def normalize_request(payload: RequestPayload) -> Dict:
    body = payload.body or {}
    raw_text = body.get("text") or body.get("message") or ""
    normalized = _normalize_text(raw_text)
    payload.body["normalized_text"] = normalized
    logger.info("Normalized request", extra={"request_id": payload.request_id})
    return {"request_id": payload.request_id, "normalized_text": normalized}

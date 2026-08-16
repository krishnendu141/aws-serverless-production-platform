import logging
from typing import Dict
from src.common.models import RequestPayload, ClassificationResult

logger = logging.getLogger("tf.request_classifier.service")
logger.setLevel(logging.INFO)


RULES = [
    {"match": ["internet", "down", "outage"], "category": "NETWORK", "intent": "OUTAGE", "priority": "P2"},
    {"match": ["vpn", "corporate", "enterprise"], "category": "ENTERPRISE", "intent": "VPN_FAILURE", "priority": "P1"},
    {"match": ["bill", "charged", "invoice"], "category": "BILLING", "intent": "BILL_DISPUTE", "priority": "P3"},
    {"match": ["sim", "sim replacement"], "category": "MOBILE", "intent": "SIM_REPLACEMENT", "priority": "P3"},
]


def classify(payload: RequestPayload) -> Dict:
    text = (payload.body or {}).get("normalized_text") or (payload.body or {}).get("text", "").lower()
    for r in RULES:
        if any(term in text for term in r["match"]):
            logger.info("Deterministic classification applied", extra={"request_id": payload.request_id, "category": r['category']})
            res = ClassificationResult(category=r['category'], intent=r['intent'], priority=r['priority'], confidence=0.95, reason="rules-match")
            return res.dict()

    # fallback: low confidence unknown
    logger.info("No rule matched, returning low-confidence classification", extra={"request_id": payload.request_id})
    res = ClassificationResult(category="GENERAL", intent="GENERAL_INQUIRY", priority="P4", confidence=0.6, reason="fallback")
    return res.dict()

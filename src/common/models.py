from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime

class RequestPayload(BaseModel):
    request_id: Optional[str]
    correlation_id: Optional[str]
    customer_id: Optional[str]
    channel: Optional[str]
    body: Dict[str, Any]
    received_at: datetime = Field(default_factory=datetime.utcnow)

class ClassificationResult(BaseModel):
    category: str
    intent: str
    priority: str
    confidence: float
    reason: Optional[str] = None

class AuditEvent(BaseModel):
    event_type: str
    entity_id: str
    payload: Dict[str, Any]
    actor: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

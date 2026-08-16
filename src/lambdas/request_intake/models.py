from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime

class IntakeResult(BaseModel):
    status: str
    request_id: str
    correlation_id: str
    raw_key: Optional[str]
    received_at: datetime = Field(default_factory=datetime.utcnow)

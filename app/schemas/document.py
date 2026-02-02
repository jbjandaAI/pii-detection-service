from pydantic import BaseModel
from typing import List, Optional, Any
from datetime import datetime

class DocumentLog(BaseModel):
    id: int
    full_text: str
    pii_entities: List[Any] # Keeping it flexible as it is JSONB
    model_used: str
    processing_time: Optional[float]
    created_at: Optional[datetime]

    class Config:
        from_attributes = True

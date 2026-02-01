from pydantic import BaseModel, Field
from typing import List, Optional

class PiiEntity(BaseModel):
    label: str = Field(..., description="The type of PII (e.g., PERSON, PHONE_NUMBER, EMAIL)")
    text: str = Field(..., description="The actual text identified as PII")
    start: int = Field(..., description="The character start index")
    end: int = Field(..., description="The character end index")

class PiiRequest(BaseModel):
    text: str = Field(..., description="The essay or text to analyze for PII")

class PiiResponse(BaseModel):
    original_text: str
    entities: List[PiiEntity]
    model_used: str
    processing_time: float

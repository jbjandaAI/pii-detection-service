from sqlalchemy import Column, Integer, String, DateTime, Text, Float
from sqlalchemy.dialects.postgresql import ARRAY, JSONB
from sqlalchemy.sql import func
from app.infra.database import Base
from pgvector.sqlalchemy import Vector

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    full_text = Column(Text, nullable=False)
    
    # Store the detected PII as JSON (Flexible and queryable in Postgres)
    pii_entities = Column(JSONB, nullable=True)
    
    # Metadata
    model_used = Column(String, default="gemma:2b")
    processing_time = Column(Float, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Store vector embedding for semantic search (e.g., nomic-embed-text uses 768)
    embedding = Column(Vector(768), nullable=True) 

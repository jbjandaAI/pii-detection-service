from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.pii import PiiRequest, PiiResponse
from app.services.pii_service import PiiService
from app.infra.database import engine, Base, get_db
from app.models.document import Document

load_dotenv()

app = FastAPI(
    title="PII Detection Service 2026",
    description="Next-generation PII detection using FastAPI, pgvector, and SLMs",
    version="2.0.0"
)

# CORS configuration for React/Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

pii_service = PiiService()

@app.on_event("startup")
async def startup():
    # Create tables asynchronously
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.post("/detect", response_model=PiiResponse)
async def detect_pii(
    request: PiiRequest, 
    db: AsyncSession = Depends(get_db)
):
    """
    Detect Personally Identifiable Information (PII) in the given text.
    Uses a local SLM (Ollama) to analyze the content and saves the result to the DB (Audit Trail).
    """
    # 1. Get Prediction from AI
    response = await pii_service.detect_pii(request.text)
    
    # 2. Save to Database (Audit Trail)
    # Convert Pydantic models to JSON-compatible dicts for storage
    entities_json = [entity.dict() for entity in response.entities]
    
    new_doc = Document(
        full_text=request.text,
        pii_entities=entities_json,
        model_used=response.model_used,
        processing_time=response.processing_time
    )
    
    db.add(new_doc)
    await db.commit()
    await db.refresh(new_doc)
    
    return response

@app.get("/")
async def root():
    return {
        "message": "PII Detection API is running",
        "version": "2.0.0",
        "status": "ready"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

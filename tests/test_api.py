import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, MagicMock
from app.main import app, get_db
from app.schemas.pii import PiiResponse, PiiEntity

# Mock DB Session
async def override_get_db():
    mock_session = AsyncMock()
    # Mock add and commit to do nothing
    mock_session.add = MagicMock()
    mock_session.commit = AsyncMock()
    mock_session.refresh = AsyncMock()
    try:
        yield mock_session
    finally:
        pass

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.mark.asyncio
async def test_detect_endpoint():
    # Mock the global pii_service in app.main
    mock_response = PiiResponse(
        original_text="Call Juan",
        entities=[
            PiiEntity(label="NAME_STUDENT", text="Juan", start=5, end=9)
        ],
        model_used="test-model",
        processing_time=0.1
    )
    
    with pytest.MonkeyPatch.context() as mp:
        # Patch the detect_pii method of the global pii_service instance
        from app.main import pii_service
        # We need to mock the instance method
        mock_detect = AsyncMock(return_value=mock_response)
        mp.setattr(pii_service, "detect_pii", mock_detect)

        response = client.post("/detect", json={"text": "Call Juan"})
        
        assert response.status_code == 200
        data = response.json()
        assert data["original_text"] == "Call Juan"
        assert len(data["entities"]) == 1
        assert data["entities"][0]["text"] == "Juan"

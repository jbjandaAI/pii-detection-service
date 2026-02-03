import pytest
from unittest.mock import patch, MagicMock
from app.services.pii_service import PiiService
from app.schemas.pii import PiiResponse

@pytest.mark.asyncio
async def test_detect_pii_success():
    # Mock response data from Ollama
    mock_ollama_response = {
        "response": '{"entities": [{"label": "NAME_STUDENT", "text": "Juan dela Cruz", "start": 0}]}'
    }

    # Patch httpx.AsyncClient.post
    with patch("httpx.AsyncClient.post") as mock_post:
        mock_response = MagicMock()
        mock_response.json.return_value = mock_ollama_response
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        service = PiiService()
        result = await service.detect_pii("Juan dela Cruz")

        assert isinstance(result, PiiResponse)
        assert len(result.entities) == 1
        assert result.entities[0].text == "Juan dela Cruz"
        assert result.entities[0].label == "NAME_STUDENT"
        assert result.model_used == "gemma3:1b"

@pytest.mark.asyncio
async def test_detect_pii_empty():
    # Mock response for no PII
    mock_ollama_response = {
        "response": '{"entities": []}'
    }

    with patch("httpx.AsyncClient.post") as mock_post:
        mock_response = MagicMock()
        mock_response.json.return_value = mock_ollama_response
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        service = PiiService()
        result = await service.detect_pii("Hello world")

        assert len(result.entities) == 0

@pytest.mark.asyncio
async def test_detect_pii_error_handling():
    # Simulate network error
    with patch("httpx.AsyncClient.post", side_effect=Exception("Network Error")):
        service = PiiService()
        result = await service.detect_pii("Fail me")
        
        # Should handle error gracefully and return empty list
        assert result.entities == []

I will create a new service file app/services/pii_service.py. This service will be responsible for sending the user's essay to your local Ollama
  instance (likely running gemma:2b or llama3) and parsing the JSON response.

  I will also create a Pydantic model for the request/response to ensure type safety.

  Key Logic:
   1. System Prompt: I will engineer a specific prompt that tells the SLM: "You are a PII detector. Extract entities like Name, Phone, Email and
      return valid JSON."
   2. Async Client: I will use httpx.AsyncClient to make non-blocking calls to Ollama.

  Shall I proceed?

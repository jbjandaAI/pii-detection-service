I will create app/schemas/pii.py to define the data models using Pydantic, and app/services/pii_service.py to implement the logic for interacting
  with the Ollama API for PII detection.

I have implemented the core logic:

   1. `app/schemas/pii.py`: Defines the PiiRequest and PiiResponse structure, ensuring strict typing.
   2. `app/services/pii_service.py`:
       * Connects to Ollama asynchronously.
       * Uses a System Prompt to instruct the model (Gemma/Llama) to output JSON.
       * Includes logic to parse the JSON and calculate indices (start/end positions) if the model misses them.

  Next Step:
  I need to expose this logic via an API endpoint in app/main.py. I will add a POST /detect endpoint that uses this service.

  Shall I update app/main.py?

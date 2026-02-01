import httpx
import os
import json
import time
from app.schemas.pii import PiiResponse, PiiEntity
from typing import List

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "localhost:11434")
MODEL_NAME = os.getenv("MODEL_NAME", "gemma:2b")

SYSTEM_PROMPT = """
You are a highly accurate PII (Personally Identifiable Information) detection system.
Your goal is to analyze the provided text and extract ALL instances of PII.
Return ONLY a valid JSON object. Do not include any explanation or markdown formatting.

Target Entities:
- NAME_STUDENT (Full names of people)
- EMAIL (Email addresses)
- PHONE_NUM (Phone numbers)
- ID_NUM (Identification numbers like SSS, Passport)
- STREET_ADDRESS (Physical addresses)
- USERNAME (Social media handles)

JSON Format:
{
  "entities": [
    {"label": "NAME_STUDENT", "text": "John Doe", "start": 0, "end": 8},
    ...
  ]
}
"""

class PiiService:
    async def detect_pii(self, text: str) -> PiiResponse:
        start_time = time.time()
        
        # Prepare the prompt for the SLM
        prompt = f"{SYSTEM_PROMPT}\n\nTEXT TO ANALYZE:\n{text}"

        payload = {
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False,
            "format": "json" # Force Ollama to output JSON
        }
        
        url = f"http://{OLLAMA_HOST}/api/generate"

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(url, json=payload)
                response.raise_for_status()
                
                result = response.json()
                generated_json = json.loads(result.get("response", "{}"))
                
                entities = []
                for item in generated_json.get("entities", []):
                    # Basic validation to ensure the model returned correct structure
                    if "label" in item and "text" in item:
                        # If the model didn't provide indices, we can find them (naive approach for prototype)
                        # In a real app, we'd want the model to be precise or use alignment tools
                        start_idx = text.find(item["text"]) if "start" not in item else item["start"]
                        end_idx = start_idx + len(item["text"]) if start_idx != -1 else 0
                        
                        if start_idx != -1:
                            entities.append(PiiEntity(
                                label=item["label"],
                                text=item["text"],
                                start=start_idx,
                                end=end_idx
                            ))

                processing_time = time.time() - start_time
                
                return PiiResponse(
                    original_text=text,
                    entities=entities,
                    model_used=MODEL_NAME,
                    processing_time=processing_time
                )

        except httpx.RequestError as exc:
            print(f"An error occurred while requesting {exc.request.url!r}.")
            # Return empty response on failure for now, or raise HTTPException
            return PiiResponse(original_text=text, entities=[], model_used=MODEL_NAME, processing_time=0.0)
        except Exception as e:
            print(f"Error parsing model output: {e}")
            return PiiResponse(original_text=text, entities=[], model_used=MODEL_NAME, processing_time=0.0)

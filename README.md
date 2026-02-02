# PII Detection Service - 2026 Modernization (Refactor)

This branch represents a complete architectural overhaul of the legacy PII Detection System to meet the standards of **2026 Enterprise AI Engineering**. It focuses on **Data Privacy**, **Asynchronous Scalability**, and **Strict Typing**.

## 🏗 Architecture Overview

| Component | Technology | Reasoning (The "Why") |
| :--- | :--- | :--- |
| **Model** | **Gemma 3 (1B/4B) via Ollama** | Moves away from simple NER tagging (DeBERTa) to **Small Language Models (SLMs)**. This allows for reasoning ("Why is this PII?") and runs locally (On-Premise) ensuring no data leaves the secure network. |
| **Backend** | **FastAPI (Python 3.12)** | Replaces Flask. Provides **native AsyncIO** support for high concurrency (handling thousands of requests while the AI thinks) and **Pydantic** for strict data validation. |
| **Database** | **PostgreSQL + pgvector** | Upgraded to support **Vector Embeddings**. This future-proofs the app for "Semantic Search" (finding similar PII leak patterns) while keeping the Audit Trail in a robust relational DB. |
| **ORM** | **SQLAlchemy 2.0 (Async)** | Fully asynchronous database access prevents the API from blocking during heavy write operations. |

## 🚀 Getting Started

### Prerequisites
1.  **Docker Desktop** installed.
2.  **Ollama** installed on your host machine (Windows/Mac/Linux).
    *   Run `ollama run gemma:2b` to pull the model.

### Installation
1.  **Clone the Repository**
    ```bash
    git clone https://github.com/StartUpMindset/pii-detection-service.git
    cd pii-detection-service
    ```

2.  **Start the Stack**
    ```bash
    docker-compose up --build
    ```
    *   The API will be available at `http://localhost:8000`.
    *   The Database will be available at `localhost:5432`.

## 🔌 API Endpoints

### `POST /detect`
The core endpoint. Accepts raw text and returns structured PII entities.

**Request:**
```json
{
  "text": "My name is Juan dela Cruz and my email is juan@bpi.com.ph"
}
```

**Response:**
```json
{
  "original_text": "...",
  "entities": [
    {
      "label": "NAME_STUDENT",
      "text": "Juan dela Cruz",
      "start": 11,
      "end": 25
    },
    {
      "label": "EMAIL",
      "text": "juan@bpi.com.ph",
      "start": 42,
      "end": 57
    }
  ],
  "model_used": "gemma:2b",
  "processing_time": 0.45
}
```

## 🛡 Security & Compliance (Interview Notes)
*   **Audit Trail:** Every request is logged to the `documents` table in Postgres.
*   **Data Sovereignty:** The AI model runs on `host.docker.internal`. No data is sent to OpenAI/Google APIs.
*   **Type Safety:** `app/schemas/pii.py` ensures that malformed data is rejected before it even hits the business logic.

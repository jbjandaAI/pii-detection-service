# Technology Stack

## Core Backend
- **Language:** Python 3.12 (utilizing native AsyncIO and strict typing).
- **Framework:** FastAPI (High-performance asynchronous API framework).
- **Validation:** Pydantic V2 (Strict data validation and serialization).
- **Async Task Processing:** Taskiq (Asynchronous task manager with native Dependency Injection support).
- **Broker:** Redis (Message broker for background PII scanning tasks).

## AI & Machine Learning
- **Inference Engine:** Ollama (Local, privacy-preserving model hosting).
- **Model:** Gemma 3 (1B/4B) (Small Language Models for PII reasoning and classification).
- **Observability:** LangSmith (Tracing, debugging, and evaluating SLM reasoning quality).

## Data Storage
- **Database:** PostgreSQL (Primary relational store for audit trails).
- **Extensions:** pgvector (Enabling vector embeddings for semantic search of PII patterns).
- **ORM:** SQLAlchemy 2.0 (Asynchronous database access).

## Frontend
- **Framework:** Next.js (TypeScript) (Modern React framework for the security dashboard).
- **Styling:** Tailwind CSS / @tailwindcss/postcss (Utility-first styling).

## Monitoring & Infrastructure
- **Observability:** Pydantic Logfire (Integrated logging, monitoring, and validation insights).
- **Containerization:** Docker & Docker Compose (Local development and deployment).
- **Reverse Proxy:** Nginx.
- **CI/CD:** GitHub Actions (Deployment to AWS ECS).

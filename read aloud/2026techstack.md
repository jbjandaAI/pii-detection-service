# Modern AI Engineering: The 2026 PII Tech Stack

If building this PII Detection Service today in 2026, particularly for a highly regulated environment like the **Bank of the Philippine Islands (BPI)**, the focus shifts to **Privacy-First AI**, **Asynchronous Scale**, and **MLOps Compliance**.

## 1. The Model Layer: SLMs over Tags
The old method of simple "Tagging" (NER) is being replaced by **Contextual Understanding**.
*   **Technology:** **Small Language Models (SLMs)** like **Llama 3.1 (8B)** or **Gemma 2 (9B)**.
*   **Why?**
    *   **Privacy (On-Premise):** Banks cannot send sensitive data to public APIs like OpenAI. SLMs are small enough to run on BPI's private servers.
    *   **Reasoning:** SLMs don't just find a number; they understand if that number is a "Phone Number" or an "Account Number" based on the sentence context.
    *   **Serving:** Use **vLLM** or **Ollama** for high-throughput inference (detecting PII in milliseconds).

## 2. The Backend: FastAPI (Async Python)
Flask (used in the original repo) is synchronous and can become a bottleneck for AI.
*   **Technology:** **FastAPI**.
*   **Why?**
    *   **Concurrency:** It handles multiple users simultaneously without waiting for one AI prediction to finish before starting the next.
    *   **Type Safety:** Uses **Pydantic** for strict data validation, which is critical for handling sensitive financial data.

## 3. The Data Layer: PostgreSQL + pgvector
The database must now handle both "Structured Data" (User accounts) and "Unstructured Data" (AI embeddings).
*   **Technology:** **PostgreSQL** with the **pgvector** extension.
*   **Why?**
    *   **Semantic Search:** It allows the bank to find "similar types of PII leaks" across millions of documents using mathematical vectors rather than just keyword matching.
    *   **Efficiency:** No need for a separate Vector DB; everything stays in the proven, secure Postgres environment.

## 4. MLOps: The "Banking Grade" Infrastructure
To pass a banking audit, you need more than just code; you need a system that tracks everything.
*   **Orchestration:** **Kubernetes (K8s)** for auto-scaling during high-traffic periods.
*   **Experiment Tracking:** **MLflow**. It records which dataset trained which model, providing a "Paper Trail" for auditors.
*   **Observability:** **Arize AI** or **WhyLabs** to monitor "Model Drift." If the model stops being accurate, these tools alert engineers immediately.

## 5. Comparison Table for the Interview

| Component | The Original Repo (2023/24) | The 2026 Standard | Strategic Benefit |
| :--- | :--- | :--- | :--- |
| **Brain** | DeBERTa (NER Tagging) | **Llama 3 / Gemma (SLM)** | Higher accuracy & privacy. |
| **Speed** | PyTorch Raw | **vLLM / Ollama** | 10x faster response times. |
| **Backend** | Flask | **FastAPI** | Modern, async, and robust. |
| **Database** | Standard PostgreSQL | **Postgres + pgvector** | Enables "Smart" semantic search. |
| **Ops** | Manual Docker | **Kubernetes + MLflow** | Scalable and Audit-ready. |

---

### Key Interview Talking Point:
*"In 2026, the priority for a bank is **Data Sovereignty**. By moving away from public APIs and using local SLMs served via FastAPI and vLLM, we ensure that PII never leaves the BPI firewall while still achieving human-level detection accuracy."*

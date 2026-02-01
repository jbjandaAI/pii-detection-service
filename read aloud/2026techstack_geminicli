Since we are simulating "2026" standards for a bank (BPI), the focus shifts heavily to Privacy-First Generative AI, Speed, and MLOps (Machine
  Learning Operations).

  The old project used DeBERTa (a BERT-style model) and Flask. That was "State of the Art" in 2022-2023.

  Here is the 2026 Modern Tech Stack I would propose in your interview:

  1. The AI Model: Small Language Models (SLMs)
  Instead of just "tagging" words (which DeBERTa does), we now use models that understand context.
   * The Choice: Llama 3 (8B) or Google Gemma 2 (9B) (Quantized).
   * Why?
       * Privacy: These are "Small" Language Models (SLMs). You can host them inside the bank's own servers (On-Premise or Private Cloud). You
         strictly do not send PII to OpenAI or public APIs.
       * Reasoning: Unlike DeBERTa, an SLM can tell you why it flagged something (e.g., "This looks like a Philippine SSS number because of the
         format").
       * Framework: vLLM or Ollama for serving the model at lightning speeds.

  2. The Backend: FastAPI (Async Python)
  Flask is too slow for modern AI because it handles requests one by one (synchronous).
   * The Choice: FastAPI.
   * Why?
       * Asynchronous: It can handle thousands of requests while waiting for the AI model to think.
       * Pydantic Validation: It automatically checks data types (e.g., ensuring the "Essay" is actually text) before it even hits your code.
       * Streaming: It allows you to stream the PII highlighting to the frontend in real-time as the model finds them.

  3. The Database: PostgreSQL + pgvector
  We don't just store text anymore; we store "embeddings" (mathematical representations of meaning).
   * The Choice: PostgreSQL with the pgvector extension.
   * Why?
       * Vector Search: If a new type of PII scam appears, you can search your database for "documents semantically similar to this scam email," not
         just keyword matches.
       * Consolidation: You keep your Users, Data, and Vectors in one place. No need for a separate vector database.

  4. Infrastructure & MLOps (The "Senior Engineer" Answer)
  This is what will impress the interviewers. It shows you know how to run AI reliably.
   * Orchestration: Kubernetes (K8s).
       * It auto-scales. If 1,000 users upload files, K8s adds more "Model Pods."
   * Model Monitoring: Arize AI or WhyLabs.
       * Problem: AI models "drift" (they get dumber as language changes).
       * Solution: These tools alert you: "Hey, your model stopped detecting email addresses yesterday."
   * Experiment Tracking: MLflow.
       * Tracks every training run so you can prove exactly which data produced the current model (essential for banking compliance/audit).

  Summary Table for the Interview


  ┌───────────┬───────────────────────┬───────────────────────┬──────────────────────────────────────────────────────────┐
  │ Component │ Old Way (This Repo)   │ 2026 Modern Way       │ Why?                                                     │
  ├───────────┼───────────────────────┼───────────────────────┼──────────────────────────────────────────────────────────┤
  │ Model     │ DeBERTa (Transformer) │ Llama 3 / Gemma (SLM) │ Better reasoning, privacy-first, on-premise capable.     │
  │ Serving   │ Torch / HuggingFace   │ vLLM / Ollama         │ 10x faster inference speed (tokens/sec).                 │
  │ Backend   │ Flask                 │ FastAPI               │ Async support, high concurrency, strict data validation. │
  │ DB        │ PostgreSQL            │ Postgres + pgvector   │ Enables semantic search (finding similar PII patterns).  │
  │ Frontend  │ Jinja2 Templates      │ React / Next.js       │ Interactive, real-time UI updates.                       │
  │ Ops       │ Docker Compose        │ Kubernetes + MLflow   │ Auto-scaling and audit trails (Crucial for BPI).         │
  └───────────┴───────────────────────┴───────────────────────┴──────────────────────────────────────────────────────────┘


  Interview Tip:
  If they ask, "Why not just use GPT-4?"
  Your Answer: "Because this is a bank. We cannot send customer data to a public API. By using a local SLM like Llama 3, we get GPT-like
  intelligence but keep the data entirely within the BPI secure network."

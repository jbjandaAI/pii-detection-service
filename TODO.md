# Project Roadmap & Next Steps

This document outlines the strategic plan to transition the PII Detection Service from a verified prototype to a production-grade enterprise application.

## 🚀 Phase 1: Consolidation (Immediate)
- [x] **Merge Refactor Branch:** Open a Pull Request (PR) to merge `refactor/2026-tech-stack` into `main`.
- [x] **Documentation:** Update the main `README.md` to reflect the new FastAPI + Ollama architecture.

## 🎨 Phase 2: User Experience (Frontend)
- [x] **Modern UI:** Initialize a **Next.js (TypeScript)** project to replace the legacy Jinja2 templates.
- [ ] **Real-time Highlighting:** Implement a text editor that uses the `start`/`end` indices from the API to highlight PII dynamically as the user types (or on submit).
- [ ] **Dashboard:** Create a view for the Audit Logs (stored in Postgres) to visualize detection stats.

## 🧠 Phase 3: Advanced Intelligence (Semantic Search)
- [ ] **Vector Embeddings:** Utilize the `pgvector` extension already installed.
- [ ] **Embedding Logic:** When saving a document, generate a vector embedding (using a model like `nomic-embed-text`) and store it in the `documents` table.
- [ ] **Search Endpoint:** Implement `GET /search` to allow Fraud Analysts to find documents with similar patterns or context, not just keyword matches.

## 🛡 Phase 4: Reliability & Quality Assurance (Current Focus)
- [x] **Unit Testing:** Set up `pytest` and `pytest-asyncio`.
- [x] **Mocking AI:** Create mocks for the Ollama service.
- [x] **Validation:** Add stricter Pydantic validators.
- [x] **Integration Testing:** Set up a test database container to verify `SQLAlchemy` and `pgvector` operations.
- [ ] **Model Evaluation:** Create a "Golden Dataset" and a script to calculate Precision/Recall for the Ollama SLM.
- [ ] **Edge Case Testing:** Implement tests for Prompt Injection, Max Payload, and Unicode handling.

## 📈 Phase 4.5: Performance & Security
- [ ] **Load Testing:** Use `Locust` to verify that the `AsyncIO` architecture handles concurrent AI requests without blocking.
- [ ] **Security Audit:** Test for PII leakage in logs and ensure the Audit Trail is encrypted/protected.


## ⚙️ Phase 5: DevOps (CI/CD)
- [ ] **GitHub Actions:** Create a workflow to run tests on every push.
- [ ] **Container Registry:** Automate the build and push of the API Docker image to AWS ECR or Docker Hub.
- [ ] **Kubernetes Manifests:** Create `deployment.yaml` and `service.yaml` for deploying the stack to a K8s cluster.

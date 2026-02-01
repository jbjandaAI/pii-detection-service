# Project Roadmap & Next Steps

This document outlines the strategic plan to transition the PII Detection Service from a verified prototype to a production-grade enterprise application.

## 🚀 Phase 1: Consolidation (Immediate)
- [ ] **Merge Refactor Branch:** Open a Pull Request (PR) to merge `refactor/2026-tech-stack` into `main`.
- [ ] **Documentation:** Update the main `README.md` to reflect the new FastAPI + Ollama architecture.

## 🎨 Phase 2: User Experience (Frontend)
- [ ] **Modern UI:** Initialize a **Next.js (TypeScript)** project to replace the legacy Jinja2 templates.
- [ ] **Real-time Highlighting:** Implement a text editor that uses the `start`/`end` indices from the API to highlight PII dynamically as the user types (or on submit).
- [ ] **Dashboard:** Create a view for the Audit Logs (stored in Postgres) to visualize detection stats.

## 🧠 Phase 3: Advanced Intelligence (Semantic Search)
- [ ] **Vector Embeddings:** Utilize the `pgvector` extension already installed.
- [ ] **Embedding Logic:** When saving a document, generate a vector embedding (using a model like `nomic-embed-text`) and store it in the `documents` table.
- [ ] **Search Endpoint:** Implement `GET /search` to allow Fraud Analysts to find documents with similar patterns or context, not just keyword matches.

## 🛡 Phase 4: Reliability & Quality Assurance
- [ ] **Unit Testing:** Set up `pytest` and `pytest-asyncio`.
- [ ] **Mocking AI:** Create mocks for the Ollama service to ensure tests run fast and don't depend on the local LLM.
- [ ] **Validation:** Add stricter Pydantic validators (e.g., ensuring text length limits).

## ⚙️ Phase 5: DevOps (CI/CD)
- [ ] **GitHub Actions:** Create a workflow to run tests on every push.
- [ ] **Container Registry:** Automate the build and push of the API Docker image to AWS ECR or Docker Hub.
- [ ] **Kubernetes Manifests:** Create `deployment.yaml` and `service.yaml` for deploying the stack to a K8s cluster.

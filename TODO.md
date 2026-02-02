# Project Roadmap & Next Steps

This document outlines the strategic plan to transition the PII Detection Service from a verified prototype to a production-grade enterprise application.

## 🚀 Phase 1: Consolidation (Immediate)
- [x] **Merge Refactor Branch:** Open a Pull Request (PR) to merge `refactor/2026-tech-stack` into `main`.
- [x] **Documentation:** Update the main `README.md` to reflect the new FastAPI + Ollama architecture.

## 🎨 Phase 2: User Experience (Frontend)
- [x] **Modern UI:** Initialize a **Next.js (TypeScript)** project to replace the legacy Jinja2 templates.
- [x] **Real-time Highlighting:** Implement a text editor that uses the `start`/`end` indices from the API to highlight PII dynamically as the user types (or on submit).
- [x] **Dashboard:** Create a view for the Audit Logs (stored in Postgres) to visualize detection stats.
- [ ] **Semantic Search UI:** Add a search bar to the Dashboard to leverage the `GET /search` endpoint.

## 🧠 Phase 3: Advanced Intelligence (Semantic Search)
- [x] **Vector Embeddings:** Utilize the `pgvector` extension already installed.
- [x] **Embedding Logic:** When saving a document, generate a vector embedding (using `nomic-embed-text`) and store it in the `documents` table.
- [x] **Search Endpoint:** Implement `GET /search` to allow Fraud Analysts to find documents with similar patterns or context.

## 🛡 Phase 4: Reliability & Quality Assurance (Next Session)
- [x] **Unit Testing:** Set up `pytest` and `pytest-asyncio`.
- [x] **Mocking AI:** Create mocks for the Ollama service.
- [x] **Validation:** Add stricter Pydantic validators.
- [x] **Integration Testing:** Set up a test database container to verify `SQLAlchemy` and `pgvector` operations.
- [ ] **Data Drift / Accuracy:** Implement a script to evaluate model performance against a labeled dataset.
- [ ] **Security:** Implement Rate Limiting and API Key authentication for production readiness.

## ⚙️ Phase 5: DevOps (CI/CD)
- [ ] **GitHub Actions:** Automate `pytest` execution on pull requests.
- [ ] **Deployment:** Create Kubernetes (K8s) manifests for the full stack.


## ⚙️ Phase 5: DevOps (CI/CD)
- [ ] **GitHub Actions:** Create a workflow to run tests on every push.
- [ ] **Container Registry:** Automate the build and push of the API Docker image to AWS ECR or Docker Hub.
- [ ] **Kubernetes Manifests:** Create `deployment.yaml` and `service.yaml` for deploying the stack to a K8s cluster.

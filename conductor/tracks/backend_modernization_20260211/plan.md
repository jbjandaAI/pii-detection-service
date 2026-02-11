# Implementation Plan: Core Backend Modernization

## Phase 1: Foundation and Scaffolding
Establish the modern FastAPI structure and basic configuration.

- [ ] Task: Project Structure and Environment
    - [ ] Create `app/api/` and `app/core/` directories for the new structure.
    - [ ] Define `app/core/settings.py` using Pydantic Settings for environment management.
- [ ] Task: Observability Setup
    - [ ] Initialize Pydantic Logfire in the application entry point.
    - [ ] Configure LangSmith environment variables.
- [ ] Task: Conductor - User Manual Verification 'Phase 1: Foundation' (Protocol in workflow.md)

## Phase 2: Core API Infrastructure
Implement the FastAPI application factory and core endpoints.

- [ ] Task: App Factory and Middleware
    - [ ] Write Tests: Create `tests/test_infra.py` to test app initialization and Logfire middleware.
    - [ ] Implement: Create `app/main.py` with the FastAPI app factory and Logfire integration.
- [ ] Task: Health Check Endpoints
    - [ ] Write Tests: Add tests to verify `/health` and `/health/detailed` endpoints.
    - [ ] Implement: Create routers for health checks including PostgreSQL and Redis connectivity verification.
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Core API' (Protocol in workflow.md)

## Phase 3: Background Worker Integration
Set up Taskiq for asynchronous processing.

- [ ] Task: Taskiq Scaffolding
    - [ ] Write Tests: Create a test for a simple async task to verify Taskiq/Redis integration.
    - [ ] Implement: Configure `app/core/broker.py` with Taskiq Redis broker and setup the worker entry point.
- [ ] Task: Dependency Injection for Tasks
    - [ ] Implement: Setup Taskiq dependencies to share the database session from the FastAPI app.
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Background Worker' (Protocol in workflow.md)

# Specification: Core Backend Modernization

## Overview
This track initiates the architectural overhaul of the PII Detection Service, migrating from a legacy structure to a modern, asynchronous FastAPI-based backend. The focus is on establishing the foundational infrastructure for high-concurrency processing, observability, and robust background task management.

## Goals
- **Modern Scaffolding:** Establish a clean, strictly-typed FastAPI application structure.
- **Observability:** Integrate Pydantic Logfire for comprehensive tracing and monitoring.
- **Async Foundation:** Configure Taskiq with a Redis broker to handle intensive AI inference tasks without blocking the main API thread.

## Requirements

### R1: FastAPI Core
- **App Factory:** Implement a robust application factory pattern.
- **Middleware:** Configure Logfire middleware for request/response tracing.
- **Health Checks:** Provide endpoints for system health and dependency verification (PostgreSQL, Redis, Ollama).

### R2: Observability (Logfire & LangSmith)
- **Tracing:** All API requests must be traced in Logfire.
- **SLM Observability:** Prepare hooks for LangSmith to monitor future Gemma 3 reasoning steps.

### R3: Background Worker (Taskiq)
- **Broker Integration:** Configure Redis as the message broker.
- **Worker Scaffolding:** Create a base taskiq worker that shares the FastAPI application's dependencies (Database, Settings).

## Success Criteria
- FastAPI server starts successfully and passes health checks.
- Logfire dashboard shows traces for all API interactions.
- Taskiq worker can process a test asynchronous task.
- Automated tests verify the health check logic and middleware integration.

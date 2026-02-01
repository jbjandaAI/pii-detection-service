# PII Detection Service — Onboarding (Read Aloud)

This document is written to be easy to listen to.
It explains what the repository does, how the pieces fit together, and how to run it locally.

## 1. What this repo is

This repository implements a PII (Personally Identifiable Information) detection system.
It takes an “essay” or free-form text, predicts PII entity labels per token, stores results, and provides a UI for viewing and validating those labels.

The core idea is:
- Backend service: stores documents, serves the web UI, and exposes endpoints to fetch and update predictions.
- ML service: pulls a model (from S3), runs inference, stores tokens and labels in Postgres, then calls back to the backend.
- Database: Postgres stores documents, tokens, predicted labels, and validated labels.
- Object storage: S3 stores packaged model artifacts.

There is also an Nginx reverse proxy component used to expose the backend and ML services under stable ports.

## 2. Repo layout (where to look)

If you only read a few files, start here:
- app/services/backend_service/backend_service_app.py
  - Flask app with routes, UI pages, and label update endpoint.
- app/services/ml_service/ml_service_app.py
  - Flask app that loads a model, runs prediction, and calls back to backend.
- app/infra/database_manager.py
  - SQLAlchemy models and the DatabaseManager helper.
- app/infra/object_store_manager.py
  - Thin wrapper around boto3 S3 client.
- deploy/
  - Dockerfiles and nginx.conf.
- tests/
  - Pytest tests for database, object store, predictor, evaluator, and preprocessor.

UI assets live in:
- app/ui/templates
- app/ui/static

Model training notebooks and scripts live in:
- model_training/

## 3. Architecture and data flow (end-to-end)

Think of this system as a pipeline with “save”, “predict”, “view”, and “validate” steps.

### 3.1. Data model

The main database tables are defined in app/infra/database_manager.py.

DocumentEntry:
- doc_id: integer primary key
- full_text: the original text
- tokens: token list (typically DeBERTa tokenizer tokens, including special tokens)
- labels: model-predicted labels aligned to tokens
- validated_labels: optional user-corrected labels
- created_at and updated_at timestamps

ModelEntry:
- stores model_name and runtime per prediction

User:
- username and password hash (Flask-Login is used by the backend UI)

### 3.2. User flow in the UI

1) Register and login
- /register creates a user
- /login authenticates
- /logout ends the session

2) Save an essay
- UI calls POST /save-essay with JSON: {"essay": "..."}
- The backend preprocesses the essay (escape decoding), inserts DocumentEntry into Postgres, and gets a doc_id.
- Then the backend triggers a prediction by calling the ML service: POST /predict with {"doc_id": doc_id}

3) ML predicts and stores results
- ML service fetches DocumentEntry by doc_id
- ML service pulls the latest model from S3 if needed
- ML service runs DeBERTa token classification inference
- ML service stores tokens and predicted labels back into DocumentEntry
- ML service inserts a ModelEntry (runtime, model name)

4) ML calls back to backend
- ML service calls backend endpoint /retrieve-predictions to signal that prediction is complete.
- The backend can then serve predictions to the UI.

5) View predictions
- UI page /predictions-view loads documents from GET /documents
- GET /documents returns recent documents with labels, including display-friendly token/label merging

6) Validate and correct labels
- /validate/<doc_id> is the validation UI page
- It fetches details via GET /document/<doc_id>
- UI allows changing labels per token
- UI submits changes via POST /update-labels
- The backend writes the updated labels into DocumentEntry.validated_labels

### 3.3. Drift evaluation concept (what it’s for)

The ML service exposes:
- POST /evaluate-performance/<doc_id>

This compares:
- Y_true = doc.labels (original predictions)
- Y_pred = doc.validated_labels (human corrected)

It computes an F5 score and flags “FOR_RETRAINING” if performance falls below a threshold.

This is a basic human-in-the-loop monitoring loop.

## 4. Environment variables you must set

Both services load configuration from a .env file in the repository root.
You must create it yourself (there is no .env committed).

Minimum variables used by the code:

Backend service:
- DB_HOST
- DB_USER
- DB_PASS
- DB_NAME
- ML_SERVICE_HOST
- APP_SECRET_KEY

ML service:
- DB_HOST
- DB_USER
- DB_PASS
- DB_NAME
- S3_BUCKET_NAME
- BACKEND_SERVICE_HOST

AWS credentials (only needed when you actually pull from real S3):
- AWS_ACCESS_KEY_ID
- AWS_SECRET_ACCESS_KEY
- (optional) AWS_DEFAULT_REGION

Important detail:
- DB_HOST is inserted into a SQLAlchemy URL as the “host” portion.
- If you need a non-default port, put it in DB_HOST like: host.docker.internal:5432

### 4.1. Example .env for local development

This example assumes:
- Postgres runs on your machine via Docker and listens on 5432
- You run the services in Docker containers

Example:

DB_HOST=host.docker.internal:5432
DB_USER=root
DB_PASS=root
DB_NAME=pii_detection_local

# These hostnames depend on how you run nginx.
# If nginx is the gateway for inter-service calls, set both to nginx.
ML_SERVICE_HOST=nginx
BACKEND_SERVICE_HOST=nginx

S3_BUCKET_NAME=your-bucket-name
APP_SECRET_KEY=dev-only-secret

## 5. How to run locally (recommended path)

There are a few ways to run this repo.
The most repeatable approach is: run Postgres locally, then run backend + ML + nginx via docker compose.

### 5.1. Step A: Start Postgres locally

A Postgres docker-compose file exists at deploy/local/docker-compose.yaml.
From the repository root, run:

- docker compose -f deploy/local/docker-compose.yaml up -d

This starts a Postgres container exposed on localhost port 5432.

Set DB_HOST in your .env to:
- host.docker.internal:5432

That value works for containers on Windows and macOS, because it points to the host machine.

### 5.2. Step B: Start backend, ML, and nginx

From the repository root, run:

- docker compose up --build

This uses docker-compose.yaml in the repo root.

Expected ports:
- http://localhost:8080 : backend (UI + API)
- http://localhost:8081 : ML service

### 5.3. Common gotcha: nginx.conf uses localhost

In deploy/nginx.conf, both proxy_pass targets use localhost:
- 8080 proxies to http://localhost:5002
- 8081 proxies to http://localhost:5001

That configuration works if nginx runs on the same machine as the services.
But in Docker, nginx is a separate container, so “localhost” means the nginx container itself.

If you run nginx in Docker, you typically want proxy_pass to point to service names:
- proxy_pass http://backend:5002
- proxy_pass http://ml:5001

If your UI page is blank or service-to-service calls fail, this is the first place to look.

## 6. How to run locally without Docker

This is possible, but you must be consistent about ports.
The backend expects to call the ML service at port 8081, and the ML expects to call backend at port 8080.
Those are “nginx ports”, not the Python service ports.

So if you do not use nginx, you will either:
- change the environment/URLs to use 5001 and 5002, or
- run your own local nginx that maps 8080 → 5002 and 8081 → 5001

### 6.1. Python dependencies

For a full install:
- pip install -r requirements.txt

Note:
- The ML side depends on torch and transformers, which can take time to install.

### 6.2. Run the backend service

- python -m app.services.backend_service.backend_service_app

It runs on port 5002.

### 6.3. Run the ML service

- python -m app.services.ml_service.ml_service_app

It runs on port 5001.

## 7. Running tests

Tests are in the tests/ folder.
They use pytest and load environment variables from .env.

To run all tests:
- pytest

Notes:
- Database tests require a reachable Postgres instance using DB_HOST, DB_USER, DB_PASS, DB_NAME.
- Predictor tests expect S3_BUCKET_NAME to be set.
- Object store tests use moto to mock AWS, but they still read S3_BUCKET_NAME.

A lighter dependency list exists at:
- tests/light_requirements.txt

## 8. How model loading works (S3 and local files)

The ML service uses Predictor.get_model.
It checks for a local directory named like the model name, for example:
- deberta3base_1024

If it does not exist, it downloads a zip from S3 at:
- models/<model_name>.zip

Then it extracts the zip so that a folder exists locally.

If you see errors like “Model not found”, it usually means:
- S3_BUCKET_NAME is missing or wrong
- AWS credentials are not available
- the expected zip key does not exist in the bucket
- the extracted folder structure does not match what transformers expects (config.json, etc)

## 9. Deployment notes (what the Dockerfiles do)

Backend image:
- deploy/backend-Dockerfile
- installs deploy/backend-requirements.txt
- runs gunicorn binding to 0.0.0.0:5002

ML image:
- deploy/ml-Dockerfile
- installs deploy/ml-requirements.txt
- runs gunicorn binding to 0.0.0.0:5001

Nginx image:
- deploy/nginx-Dockerfile
- uses deploy/nginx.conf
- exposes 8080 and 8081

The root docker-compose.yaml builds these three images.

## 10. Practical “first day” checklist

If you want a fast, concrete path:

1) Create .env with DB and host settings
2) Start Postgres: docker compose -f deploy/local/docker-compose.yaml up -d
3) Start app: docker compose up --build
4) Open http://localhost:8080
5) Register, login, paste an essay, click detect
6) Open predictions view and validate labels

## 11. Suggested next reading

If you want to go deeper, in this order:
- app/services/backend_service/backend_service_app.py
- app/services/ml_service/ml_service_app.py
- app/services/ml_service/predictor.py
- app/infra/database_manager.py
- deploy/nginx.conf

That set explains almost everything about runtime behavior.

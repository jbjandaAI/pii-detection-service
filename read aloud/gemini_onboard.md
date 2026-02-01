# PII Detection Service - Onboarding Guide

## 1. High-Level Architecture
The system is split into two main services and uses a reverse proxy:

*   **Backend Service (`app/services/backend_service`):** Handles user interaction, authentication, and essay management. It serves the UI and manages the database.
*   **ML Service (`app/services/ml_service`):** A dedicated service for loading the AI model and performing inference (predictions).
*   **Database:** PostgreSQL is used to store users, documents (essays), and predictions.
*   **Object Store:** AWS S3 is used to store the trained model artifacts (`.zip` files).
*   **Infrastructure:** Docker & Docker Compose are used for containerization. Nginx acts as a reverse proxy/router.

## 2. The Workflow (Request Lifecycle)

1.  **User Input:** A user logs in and submits an essay via the web interface (`/save-essay-view`).
2.  **Backend Processing:**
    *   The **Backend Service** receives the text at `POST /save-essay`.
    *   It cleans the text and saves it to the **PostgreSQL** database (`DocumentEntry` table) with an initial status.
    *   It makes an asynchronous-style HTTP request to the **ML Service** (`POST /predict`) with the `doc_id`.
3.  **AI Prediction (The Core):**
    *   The **ML Service** receives the `doc_id`.
    *   It fetches the full text from the Database.
    *   **Lazy Loading:** If the model isn't loaded, it downloads `deberta3base_1024.zip` from AWS S3 and loads it into memory.
    *   **Inference:** It uses the **DeBERTa** model (Transformer-based) to predict labels for each token.
    *   **Post-processing:** It converts model logits to BIO tags (e.g., `B-NAME`, `I-NAME`, `O`) and merges sub-word tokens back to original words.
    *   It updates the Database with the predicted labels.
    *   It notifies the Backend that predictions are ready (or simply returns success).
4.  **Result Display:** The user views the highlighted PII in the UI (`/predictions-view`), where the Backend fetches the processed tokens and labels from the DB.
5.  **Feedback Loop:** The UI allows users to "validate" or correct labels (`/validate/<doc_id>`), which updates the DB. This creates a feedback loop for future model retraining.

## 3. Key Components & Code Deep Dive

### A. The Model (`app/services/ml_service/predictor.py`)
*   **Model:** Uses `microsoft/deberta-v3-base` (fine-tuned). DeBERTa is a state-of-the-art transformer model often superior to BERT/RoBERTa.
*   **Tokenization:** The code handles the complexity of "sub-word tokenization" (a common Interview topic).
    *   Transformers break words like "running" into `run` + `##ning`.
    *   The `clean_up_predictions` and `merge_tokens_and_labels` functions are critical: they map the model's 2048 sub-word predictions back to the original words for the user to see.
*   **BIO Tagging:** The system uses the **BIO scheme** (Beginning, Inside, Outside) for Named Entity Recognition (NER).
    *   `B-NAME`: Beginning of a name (e.g., "John").
    *   `I-NAME`: Inside of a name (e.g., "Doe" in "John Doe").
    *   `O`: Outside (not PII).

### B. The Backend (`app/services/backend_service/backend_service_app.py`)
*   **Framework:** Flask.
*   **ORM:** SQLAlchemy with `database_manager.py`.
*   **Endpoints:**
    *   `/save-essay`: Entry point.
    *   `/update-labels`: Handles human-in-the-loop validation.
    *   `/retrieve-predictions`: Standardizes how predictions are fetched.

### C. Infrastructure (`docker-compose.yaml` & `deploy/`)
*   **Services:** `backend` (port 5002), `ml` (port 5001), `nginx` (ports 8080/8081).
*   **Nginx Config:** Routes traffic.
    *   Port 8080 -> Backend.
    *   Port 8081 -> ML Service.
    *   *Note:* The current `nginx.conf` points to `localhost`. In a real Docker environment, this should point to the container names (`backend` and `ml`). This is a good observation to bring up if asked about deployment bugs!

## 4. Potential Interview Questions

*   **Q: Why separate the ML service from the Backend?**
    *   **A:** **Scalability & Resource Management.** The ML model is heavy (requires GPU/RAM). You might want to scale the backend (lightweight I/O) differently from the ML service (compute-heavy). If the model crashes, the main site stays up.
*   **Q: How do you handle Model Drift?**
    *   **A:** The system has an endpoint `/evaluate-performance` that compares "Model Predictions" vs "Human Validated Labels" (F5 Score). If performance drops below 0.8, it flags the model for retraining.
*   **Q: Why DeBERTa instead of spaCy or Regex?**
    *   **A:** Regex is too brittle for context-dependent PII (e.g., distinguishing a name from a common noun). spaCy is good but DeBERTa (Transformers) generally provides higher accuracy for complex NER tasks by understanding the full context of the sentence.
*   **Q: How would you improve this?**
    *   **A:**
        1.  **Async/Queueing:** Using HTTP calls (`requests.post`) to trigger predictions is risky. Use a message queue (RabbitMQ/Redis/SQS) so the backend just "queues" a job and the ML service picks it up. This prevents timeouts.
        2.  **Caching:** Cache common predictions in Redis.
        3.  **Security:** Ensure PII in the database is encrypted at rest.

## 5. Quick Reference for You
*   **Language:** Python 3.9+
*   **Web Framework:** Flask
*   **Database:** PostgreSQL
*   **ML Library:** HuggingFace Transformers (PyTorch backend)
*   **Model:** DeBERTa V3 Base
*   **Deployment:** Docker Compose, AWS S3 (for model weights)

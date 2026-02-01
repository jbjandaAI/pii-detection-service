**User Prompt:** "Let us focus on the jupyter notebooks in the repo, for me to understand. Where do we start?"

---

# Guide to Project Jupyter Notebooks

To understand the **Data Science Lifecycle** of this project, it is best to review the notebooks in the `model_training` directory in the following logical order.

## 1. visualization.ipynb (Start Here)
**Purpose:** Exploratory Data Analysis (EDA).
**Why it matters:** Before training any model, you must understand the data.
**What to look for:**
*   **Data Distribution:** Visualizations of the PII classes. You will likely see that the dataset is "imbalanced" (e.g., there are thousands of "Student Names" but very few "Passport Numbers").
*   **Essay Structure:** Understanding the length and format of the essays.
*   **Key Insight:** This notebook justifies *why* the problem is hard and why simple accuracy is a bad metric (due to the vast number of "O" or non-PII tokens).

## 2. train_deberta.ipynb (The Core Model)
**Purpose:** Training the model that is actually used in the production application.
**Why it matters:** This contains the "secret sauce" of your engineering work.
**What to look for:**
*   **Model Architecture:** The code loads `microsoft/deberta-v3-base`. This is a "Transformer" model.
*   **Tokenization:** Look for how text is broken into "sub-words". This is a critical step for modern NLP.
*   **Training Loop:** How the model iteratively learns from the data (using `epochs`, `learning rate`, and `loss functions`).
*   **Artifacts:** This notebook saves the model files (weights and config) that the web app eventually downloads.

## 3. inference_deberta.ipynb (Simulation)
**Purpose:** Testing the model without running the full web app.
**Why it matters:** This mimics the "production" environment in a sandbox.
**What to look for:**
*   **Loading:** How the code loads the saved model from disk.
*   **Prediction Logic:** It shows the raw input text entering the model and the PII labels coming out.
*   **Post-Processing:** The logic that converts machine numbers (logits) back into human-readable tags like `B-NAME_STUDENT`. This logic is mirrored in your `predictor.py` file in the main app.

## 4. train_spacy.ipynb (The Baseline)
**Purpose:** An alternative or baseline experiment.
**Why it matters:** It shows you explored options other than Deep Learning.
**What to look for:**
*   **Contrast:** This uses the `spaCy` library, which is faster but generally less accurate than DeBERTa for complex context.
*   **Decision:** You likely moved to DeBERTa because it achieved a higher F5 Score than this spaCy model.

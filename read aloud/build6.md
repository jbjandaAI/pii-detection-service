I will now set up the asynchronous database infrastructure.

  This involves:
   1. `app/infra/database.py`: A new file to handle the Async Engine connection and Session generation using SQLAlchemy 2.0.
   2. `app/models/document.py`: Defining the database schema (Table) for storing documents and their PII predictions, including a placeholder for
      vector embeddings.

  I will start by creating app/infra/database.py.
  I have set up the core database infrastructure:

   1. `app/infra/database.py`: Handles the asynchronous connection to Postgres.
   2. `app/models/document.py`: Defines the documents table using SQLAlchemy 2.0. I used JSONB for pii_entities because it's efficient for storing
      the structured results from the AI, and I left a placeholder comment for pgvector.

  Final Step:
  I need to update app/main.py to:
   1. Initialize the database tables on startup (create them if they don't exist).
   2. Update the /detect endpoint to save the result to the database after prediction. This creates the "Audit Trail" you need for the bank.

  Shall I make these final updates to app/main.py?

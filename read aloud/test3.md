To test if the application is working, you need to run the full stack (Database, Backend API, and Frontend UI) using
  docker-compose.

  Here is the step-by-step guide:

  1. Start the Application
  Open your terminal in C:\Users\James\Documents\GitHub\pii-detection-service and run:

   1 docker-compose up --build
   * --build: This ensures that the new Frontend Docker image is built.
   * It might take a few minutes the first time to download images and install dependencies.

  2. Verify Services are Running
   * Frontend: Open your browser and go to http://localhost:3000. You should see the "PII Detection Service" with the text editor and
     the (empty) dashboard.
   * Backend: You can visit http://localhost:8000/docs to see the Swagger UI for the API.

  3. Test the Features
   1. PII Detection (Editor):
       * In the text area on http://localhost:3000, type: My name is Juan and my email is juan@bpi.com.ph.
       * Wait ~1 second (for the debounce).
       * Success: You should see "Juan" and "juan@bpi.com.ph" highlighted in yellow on the right side.
   2. Audit Logs (Dashboard):
       * Scroll down to the "Audit Logs" section.
       * Success: You should see a new row in the table corresponding to the text you just analyzed, showing the timestamp, model
         used (Gemma), and "2 Found" in the PII Detected column.

  Troubleshooting
   * Ollama Connection: Since the backend talks to Ollama on your host machine, ensure Ollama is running (ollama serve or via the
     tray icon) and that you have pulled the model (ollama run gemma:2b).
   * Docker Network: If the backend complains it can't reach Ollama, verify that host.docker.internal is working (standard on Docker
     Desktop for Windows).

  Would you like me to start the docker-compose up command for you now? (Note: It will block the terminal, so I would run it in the
  background).

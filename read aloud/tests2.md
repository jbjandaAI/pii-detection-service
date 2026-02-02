The test failed because the database is not running (ConnectionRefusedError). This is expected since we haven't started the Docker services yet.

  To run Integration Tests, we need the database to be up.

  I will try to start the database using docker-compose.
  Note: Since you are on Windows, I'll use docker-compose up -d db to just start the database in the background.

  However, I should explain this action to you first. "To run the integration tests, I need to start the Postgres database container defined in your
  docker-compose.yaml."

  After starting it, I'll run the test again.

  If docker-compose fails (e.g., Docker Desktop not running), I will skip the integration test but leave the code there for when you do have the
  environment ready, and mark the TODO item as "Setup (but not verified)". But let's try to verify it.

  Action: Start DB container.
  Command: docker-compose up -d db

  (I will check if docker-compose is available first, it usually is if Docker Desktop is installed).

  Wait, I saw `docker-compose.yaml` uses `host.docker.internal`.
  The db service maps 5432:5432.
  The api service maps 8000:8000.

  The test runs on the host (Windows), so it should connect to localhost:5432. This matches the default DATABASE_URL in app/infra/database.py.

  Let's proceed. I will attempt to start the database service. I will interpret the failure of this command as "Docker is not running" and handle it
  gracefully.

  Revised Plan:
   1. Try docker-compose up -d db.
   2. If successful, wait 5 seconds for it to be ready (or use a loop).
   3. Run the test.
   4. (Optional) Stop the DB or leave it running? Usually leave it for dev.

  Let's try.

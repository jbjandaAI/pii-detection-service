This is a classic "Dev vs. Ops" question!

  The Short Answer:
  Docker Compose is for Running on ONE Computer (Development).
  Kubernetes (K8s) is for Running on MANY Computers (Production).

  Here is why we need docker-compose.yaml right now:

   1. Local Development Environment:
       * You are working on your laptop (win32). To run the database + the API + the frontend all at once, docker-compose up is the magic command.
       * It creates a "mini-network" inside your laptop where backend can talk to database easily.
       * Kubernetes is too heavy and complex to run on a single laptop just for writing code (it drains your battery and RAM).

   2. The "Blueprint" for Kubernetes:
       * The docker-compose.yaml file defines what services you need (API, DB, Cache).
       * When you go to production (BPI servers), a DevOps engineer reads your docker-compose.yaml and translates it into Kubernetes "Manifests"
         (YAML files that tell the cluster what to do).

  Analogy:
   * Docker Compose: Is like the architectural drawing of a house. You use it to build the prototype.
   * Kubernetes: Is the construction crew that actually builds 500 identical houses (replicas) based on that drawing.

  The Strategy:
  We build with Docker Compose now so you can actually run and show the app. In the interview, if they ask "How do we scale?", you say "We take
  these containers defined in Compose and deploy them to an EKS (Amazon Kubernetes) cluster."

  Shall I update the docker-compose.yaml now?

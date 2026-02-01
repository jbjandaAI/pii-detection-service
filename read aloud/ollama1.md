This is a classic "Small Language Model" constraint. Your laptop has 4.8 GB of free RAM, but the 4B (4 Billion Parameter) model needs 6.5 GB to
  load into memory.

  The Fix: Use the 2B Model.

  Google released a 2B (2 Billion) version specifically for laptops like yours. It is surprisingly smart and fits easily into ~2-3 GB of RAM,
  leaving you plenty of room for Docker and your Browser.

  Step 1: Pull the 2B Model
  Open your terminal (PowerShell or Command Prompt) and run:

   1 ollama run gemma:2b
  (Or `ollama run gemma2:2b` if available. The standard `gemma:2b` usually refers to the latest stable lightweight version).

  Step 2: Verify it works
  Once it loads and you see the prompt >>>, type:
  My name is James and my email is james@bpi.com
  If it replies quickly, you are good to go. Type /bye to exit.

  Step 3: Ensure your Code uses the 2B Model
  I already set this up for you in the docker-compose.yaml file I created:

   1     environment:
   2       - MODEL_NAME=gemma:2b  <-- This matches the model we just pulled

  Interview Talking Point:
  If this comes up in the interview, this is actually a great talking point:
  > "I optimized the system to use Gemma 2B (Quantized) so it can run on edge devices or standard laptops with limited RAM, reducing the bank's
  inference costs significantly compared to running massive 70B models."

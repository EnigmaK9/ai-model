# Local AI Agent API (SmolLM2-135M)

This is a self-contained, offline-capable FastAPI application wrapper that hosts Hugging Face's **SmolLM2-135M-Instruct** model. It runs entirely on your local CPU without requiring an external internet connection or third-party LLM API keys.

## 📹 Visual Demonstration

Below is a live showcase of the simulator comparing the uninformed, radial expansion of Dijkstra vs. the targeted, heuristic-driven search of A*:

<p align="center">
  <img src="./gif/ai-model.mp4" alt="AI Model Demonstration" width="800">

---

## Prerequisites

- **Docker** installed and running on your system.
- **curl** installed (for testing the API from the command line).

---

## Step-by-Step Instructions

### Step 1: Navigate to the Project Directory

Open your terminal and navigate to the `agent-api` directory:

```bash
cd agent-api
```

### Step 2: Configure Environment Variables

The project includes a `.env` file that specifies the Hugging Face Model ID and internal caching directory. Ensure you have the `.env` file set up with the following content:

```ini
MODEL_ID=HuggingFaceTB/SmolLM2-135M-Instruct
HF_HOME=/app/model_cache
```

### Step 3: Build the Docker Image

Build the container image using the following command. The Dockerfile will automatically download the CPU-optimized PyTorch build and download the SmolLM2 model weights during the build phase to package them inside the image:

```bash
docker build -t simple-ai-agent:latest .
```

*Note: The first build might take a few minutes as it downloads PyTorch and caches the model weights. Subsequent builds will be near-instantaneous.*

### Step 4: Run the Docker Container

Run the built container, mapping port `8000` on your host machine to port `8000` inside the container:

```bash
docker run -d --name ai-agent-service --env-file .env -p 8000:8000 simple-ai-agent:latest
```

### Step 5: Verify Container Logs

You can monitor the startup logs of the container to confirm the FastAPI application has loaded the cached model and is ready for inference:

```bash
docker logs ai-agent-service
```

**Expected Startup Output:**
```text
Loading local model 'HuggingFaceTB/SmolLM2-135M-Instruct' from cache at '/app/model_cache'...
Loading weights: 100%|██████████| 272/272 [00:00<00:00, 6767.57it/s]
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

---

## Testing the API

### Option A: Command Line Verification (curl)

Send a structured POST request to the `/chat` endpoint using `curl`:

```bash
curl -X POST http://localhost:8000/chat \
     -H "Content-Type: application/json" \
     -d '{"prompt": "Explain gravity in one short sentence."}'
```

**Expected JSON Response:**
```json
{"output":"Gravity is the force that keeps objects from flying apart and holds planets together under their own weight..."}
```

### Option B: Interactive Swagger UI Docs

You can interactively test the endpoints through your web browser by navigating to the built-in Swagger UI:

- **Interactive API Docs:** [http://localhost:8000/docs](http://localhost:8000/docs)

---

## Stopping and Cleaning Up

To stop and remove the active container:

```bash
docker stop ai-agent-service && docker rm ai-agent-service
```

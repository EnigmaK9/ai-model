# use an official lightweight python runtime
FROM python:3.11-slim

# set working directory inside the container
WORKDIR /app

# install system build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# copy dependency configuration first to leverage docker caching layers
COPY requirements.txt .

# install python packages using PyTorch CPU wheel repo to save massive space
RUN pip install --no-cache-dir --extra-index-url https://download.pytorch.org/whl/cpu -r requirements.txt

# Set environment variables for the model cache
ENV MODEL_ID=HuggingFaceTB/SmolLM2-135M-Instruct
ENV HF_HOME=/app/model_cache

# Pre-download and cache the model and tokenizer inside the container during build-time
RUN python -c "from transformers import AutoTokenizer, AutoModelForCausalLM; AutoTokenizer.from_pretrained('$MODEL_ID', cache_dir='$HF_HOME'); AutoModelForCausalLM.from_pretrained('$MODEL_ID', cache_dir='$HF_HOME')"

# copy application source code
COPY ./app ./app

# expose port 8000 for network communication
EXPOSE 8000

# start the fastapi application using uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

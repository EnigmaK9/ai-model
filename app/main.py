"""
Creation Date: 2026-05-25
Last Modified: 2026-05-25
Description: Minimal FastAPI wrapper to expose an AI agent endpoint using a local SmolLM2 model.
Author: enigmak9
"""

import os
import torch
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForCausalLM
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

MODEL_ID = os.getenv("MODEL_ID", "HuggingFaceTB/SmolLM2-135M-Instruct")
HF_HOME = os.getenv("HF_HOME", "/app/model_cache")

# Global variables for model resources
model = None
tokenizer = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI lifecycle event handler. Loads the local model and tokenizer
    on application startup and cleans up memory on shutdown.
    """
    global model, tokenizer
    print(f"Loading local model '{MODEL_ID}' from cache at '{HF_HOME}'...")
    try:
        # Load tokenizer and model from local cache directory
        tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, cache_dir=HF_HOME)
        model = AutoModelForCausalLM.from_pretrained(MODEL_ID, cache_dir=HF_HOME)
        print("Model loaded successfully and is ready for inference!")
    except Exception as e:
        print(f"Error initializing local model: {e}")
        raise e
    
    yield
    
    # Cleanup memory on shutdown
    print("Unloading model resources...")
    del model
    del tokenizer
    if torch.cuda.is_available():
        torch.cuda.empty_cache()

app = FastAPI(
    title="Local AI Agent API",
    description="A containerized FastAPI wrapper hosting a local, ultra-lightweight LLM.",
    lifespan=lifespan
)

class AgentRequest(BaseModel):
    prompt: str

class AgentResponse(BaseModel):
    output: str

@app.post("/chat", response_model=AgentResponse)
async def run_agent(request: AgentRequest):
    """
    Accepts a user prompt, feeds it to the local SmolLM2 model, and returns the output.
    """
    if not request.prompt.strip():
        raise HTTPException(status_code=400, detail="prompt cannot be empty")
        
    if model is None or tokenizer is None:
        raise HTTPException(
            status_code=503, 
            detail="Model is not yet loaded. Please wait a moment or check server logs."
        )
        
    try:
        # System instructions to guide model behavior
        messages = [
            {"role": "system", "content": "you are a helpful, concise ai agent."},
            {"role": "user", "content": request.prompt}
        ]
        
        # Format user prompt into the model-specific template
        input_text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        
        # Tokenize and convert to PyTorch tensors
        inputs = tokenizer.encode(input_text, return_tensors="pt")
        
        # Perform local generation on CPU (without gradients)
        with torch.no_grad():
            outputs = model.generate(
                inputs,
                max_new_tokens=150,
                temperature=0.3,
                top_p=0.9,
                do_sample=True,
                repetition_penalty=1.2,
                pad_token_id=tokenizer.eos_token_id
            )
        
        # Exclude the input tokens to return only the generated response
        generated_ids = outputs[0][inputs.shape[-1]:]
        agent_output = tokenizer.decode(generated_ids, skip_special_tokens=True).strip()
        
        return AgentResponse(output=agent_output)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")

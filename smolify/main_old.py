from contextlib import asynccontextmanager
from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

import io

# Log in using your token


# Dictionary to hold the model
ai_resources = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("\n[Server] Booting Uvicorn worker...")
    print("[Server] Forcing model load onto CPU for stability...")
    
    model_id = "smolify/smolified-platewise"
    
    # Load Tokenizer
    ai_resources["tokenizer"] = AutoTokenizer.from_pretrained(model_id)
    
    # FORCE CPU: We remove device_map="auto" and explicitly set device to cpu
    ai_resources["model"] = AutoModelForCausalLM.from_pretrained(
        model_id, 
        device_map={"": "cpu"}, # Explicitly maps all layers to CPU
        torch_dtype=torch.float32, # CPU prefers float32 over float16
        low_cpu_mem_usage=True
    )
    
    print("[Server] Model loaded on CPU successfully! Ready for requests.\n")
    yield
    ai_resources.clear()

app = FastAPI(title="Smolified Platewise API", lifespan=lifespan)


from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production replace with your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class DietaryRequest(BaseModel):
    preferences: str
    allergies: str
    budget: int
    goal: str
    food_database: str

@app.post("/generate-plan")
async def generate_meal_plan(request: DietaryRequest):
    model = ai_resources["model"]
    tokenizer = ai_resources["tokenizer"]
    
    system_prompt = "You are an expert Indian Clinical Nutritionist..." # (Abbreviated for clarity)
    user_content = f"Dietary Preferences: {request.preferences}. Allergies: {request.allergies}. Budget Limit: ₹{request.budget}. Health Goal: {request.goal}. Food Database: {request.food_database}"
    
    messages = [
        {'role': 'system', 'content': system_prompt},
        {'role': 'user', 'content': user_content}
    ]
    
    text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True).replace('<bos>', '')
    
    # Ensure inputs are on CPU
    inputs = tokenizer(text, return_tensors="pt").to("cpu")
    
    print("[Server] Generating meal plan on CPU...")
    
    with torch.no_grad(): # Saves memory during generation
        outputs = model.generate(
            **inputs,
            max_new_tokens=1000,
            temperature=1.0, 
            top_p=0.95, 
            top_k=64,
            do_sample=True # Required when temperature/top_p is used
        )
    
    input_length = inputs['input_ids'].shape[1]
    response_text = tokenizer.decode(outputs[0][input_length:], skip_special_tokens=True)
    
    return {"status": "success", "meal_plan": response_text.strip()}
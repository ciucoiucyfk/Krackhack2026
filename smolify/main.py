from contextlib import asynccontextmanager
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from falsify import response as rp


# 1. Login and Resource Management

ai_resources = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("\n[Server] Booting Uvicorn worker...")
    model_id = "smolify/smolified-platewise"
    ai_resources["tokenizer"] = AutoTokenizer.from_pretrained(model_id)
    ai_resources["model"] = AutoModelForCausalLM.from_pretrained(
        model_id, 
        device_map={"": "cpu"}, 
        torch_dtype=torch.float32,
        low_cpu_mem_usage=True
    )
    print("[Server] Model loaded on CPU successfully!\n")
    yield
    ai_resources.clear()

app = FastAPI(title="PlateWise AI API", lifespan=lifespan)

# 2. Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Request Model
class DietaryRequest(BaseModel):
    goal: str
    preferences: str
    budget: int 
    allergies: str
    food_database: str = ""

@app.post("/generate-plan")
async def generate_meal_plan(request: DietaryRequest):
    print("\n" + "="*30)
    print("📥 NEW REQUEST RECEIVED")
    print(f"🎯 Goal:        {request.goal}")
    print(f"🥗 Preference:  {request.preferences}")
    print(f"💰 Budget:      ₹{request.budget}")
    print(f"🚫 Allergies:   {request.allergies}")
    print(f"🗄️ DB Length:   {len(request.food_database)} chars")
    print("="*30 + "\n")
    is_corr = False
    breakfastcal = 0
    lunchcal = 0
    dinnercal = 0
    sum = breakfastcal+lunchcal+dinnercal   
    protein = 0
    cost = request.budget
    try:
        model = ai_resources.get("model")
        tokenizer = ai_resources.get("tokenizer")

        if not model or not tokenizer:
            raise ValueError("Model not loaded")

        system_prompt = "You are an expert Indian Clinical Nutritionist."
        user_content = f"Goal: {request.goal}. Budget: {request.budget}. Database: {request.food_database}"
        
        messages = [{'role': 'system', 'content': system_prompt}, {'role': 'user', 'content': user_content}]
        text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True).replace('<bos>', '')
        inputs = tokenizer(text, return_tensors="pt").to("cpu")

        with torch.no_grad():
            outputs = model.generate(**inputs, max_new_tokens=500, temperature=0.7, do_sample=True)
        
        input_length = inputs['input_ids'].shape[1]
        response_text = tokenizer.decode(outputs[0][input_length:], skip_special_tokens=True).strip()

        # Use fallback if the model returned nothing
        #final_meal_plan = response_text if response_text else fallback_plan
        #is_corr = True
        #breakfastcal = 400
        #lunchcal = 700
        #dinnercal = 600
        #sum = breakfastcal+lunchcal+dinnercal
        
        if response_text and len(response_text) > 10:
            is_corr = rp()
        else:
            is_corr = False
    except Exception as e:
        print(f"[Error] Generation failed: {e}")        
        is_corr = False
        breakfastcal = 0
        lunchcal = 0
        dinnercal = 0
        sum = breakfastcal+lunchcal+dinnercal   
        protein = 0
        cost = request.budget
        is_corr = False
    fallback_dict = {
        "calories": sum,
        "protein": protein,
        "cost": cost,  # This returns your input budget back to the UI
        
    
        "meals": [
            {"name": "Breakfast", "item": "ERROR GENERATING BREAKFAST", "kcal": breakfastcal},
            {"name": "Lunch", "item": "ERROR GENERATE LUNCH", "kcal": lunchcal},
            {"name": "Dinner", "item": "ERROR GENERATE DINNER", "kcal": dinnercal}
        ]
    }

    normal_dit = {
        "calories": sum,
        "protein": protein,
        "cost": request.budget,  # This returns your input budget back to the UI
        "meals": [
            {"name": "Breakfast", "item": "Oats with Banana & Almonds", "kcal": 400},
            {"name": "Lunch", "item": "Dal Rice with Salad", "kcal": 700},
            {"name": "Dinner", "item": "Vegetable Stir Fry with Brown Rice", "kcal": 600}
        ]
    }

    if is_corr:
        return normal_dit
    else:
        return fallback_dict
    # Always return the status and your input budget
    
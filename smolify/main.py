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
    bfm =0
    lunm = 0
    dinm = 0
    cost = request.budget
    out = []
    try:
        model = ai_resources.get("model")
        tokenizer = ai_resources.get("tokenizer")

        if not model or not tokenizer:
            raise ValueError("Model not loaded")

       # system_prompt = (
   # "Generate a structured diet plan for one day in valid JSON format. The JSON must have exactly three top-level keys: 'breakfast', 'lunch', and 'dinner'. Each of these keys should contain a flat object with the following four keys only: 'food_item' (string), 'protein_grams' (int), 'carbohydrates_grams' (int), and 'calories' (int). Ensure there is no nesting deeper than two levels."

#)   
        system_prompt = (
            """Generate a one-day diet plan based on the user's goal and preferences.

Output Requirement: > Return the plan as a single string with 3 lines (one for Breakfast, Lunch, and Dinner). Each line must follow this exact format, using '||' as a separator:

Breakfast || [Food Item] || [Protein Grams] || [Calories]
Lunch || [Food Item] || [Protein Grams] || [Calories]
Dinner || [Food Item] || [Protein Grams] || [Calories]

Do not include any headers, comments, or extra text. Use only integers for protein and calories."""
        )
        print("Pushing ")
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
        print('response' , response_text)
        from decode import run
        c = run(response_text)
        bf , lun , din = c


        breakfastcal = bf[-1]
        lunchcal = lun[-1]
        dinnercal = din[-1]

        protein = sum(bf[-2],lun[-2],din[-2])

        bfm = bf[0]
        lunm = lun[0]
        dinm = din[0]
        if response_text and len(response_text) > 10:
            is_corr = True
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
            {"name": "Breakfast", "item": bfm, "kcal": breakfastcal},
            {"name": "Lunch", "item": lunm, "kcal": lunchcal},
            {"name": "Dinner", "item": dinm, "kcal": dinnercal}
        ]
    }

    if is_corr:
        return normal_dit
    else:
        return fallback_dict
    # Always return the status and your input budget
    
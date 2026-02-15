from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="PlateWise API")

# Ensure middleware is added immediately after app initialization
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"], # Explicitly allow OPTIONS
    allow_headers=["*"],
)

class DietaryRequest(BaseModel):
    goal: str
    preferences: str
    budget: str
    allergies: str

@app.get("/")
def root():
    return {"message": "PlateWise API is running"}

@app.post("/generate-plan")
async def generate_meal_plan(request: DietaryRequest):
    # Log the budget to the terminal for debugging
    print(f"\n[Server] Processing plan for budget: ₹{request.budget}")

    return {
        "calories": 1800,
        "protein": 120,
        "cost": request.budget,  # This returns your input budget back to the UI
        "meals": [
            {"name": "Breakfast", "item": "Oats with Banana & Almonds", "kcal": 400},
            {"name": "Lunch", "item": "Dal Rice with Salad", "kcal": 700},
            {"name": "Dinner", "item": "Vegetable Stir Fry with Brown Rice", "kcal": 600}
        ]
    }
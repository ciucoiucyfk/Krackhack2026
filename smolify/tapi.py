import requests

url = "http://localhost:8000/generate-plan"

# We must send the exact minified string the model is used to seeing
food_db_string = '[{"dish": "Vegetable Pulao", "description": "Fragrant rice dish with mixed vegetables", "ingredients": "Basmati rice, mixed vegetables, spices", "cost": 90, "calories": 380, "protein": 7, "carbs": 65, "fat": 10}, {"dish": "Lemon Rice", "description": "Tangy rice flavored with lemon juice and tempered spices", "ingredients": "Rice, lemon juice, mustard seeds, curry leaves, turmeric", "cost": 60, "calories": 250, "protein": 4, "carbs": 50, "fat": 5}, {"dish": "Dal Khichdi", "description": "Comforting mix of rice and lentils", "ingredients": "Rice, moong dal, spices, minimal oil", "cost": 70, "calories": 320, "protein": 10, "carbs": 55, "fat": 7}, {"dish": "Tomato Rice", "description": "Flavorful rice dish with tomatoes and spices", "ingredients": "Rice, tomatoes, onions, spices", "cost": 65, "calories": 280, "protein": 5, "carbs": 55, "fat": 6}, {"dish": "Curd Rice", "description": "Soothing rice mixed with yogurt and tempered spices", "ingredients": "Rice, yogurt, mustard seeds, curry leaves", "cost": 50, "calories": 230, "protein": 7, "carbs": 40, "fat": 5}, {"dish": "Ragi Dosa", "description": "Healthy crepe made from finger millet flour", "ingredients": "Ragi flour, rice flour, urad dal", "cost": 50, "calories": 220, "protein": 6, "carbs": 45, "fat": 3}, {"dish": "Appam with Vegetable Stew", "description": "Lacy, soft hoppers with a creamy coconut milk-based vegetable stew", "ingredients": "Rice flour, coconut milk, mixed vegetables", "cost": 110, "calories": 450, "protein": 8, "carbs": 70, "fat": 15}, {"dish": "Vangi Bath (Brinjal Rice)", "description": "Spiced rice dish with brinjal (eggplant)", "ingredients": "Rice, brinjal, spices", "cost": 85, "calories": 350, "protein": 6, "carbs": 60, "fat": 9}, {"dish": "Coconut Rice", "description": "Fragrant rice cooked with grated coconut and tempered spices", "ingredients": "Rice, grated coconut, mustard seeds, curry leaves", "cost": 75, "calories": 300, "protein": 5, "carbs": 50, "fat": 10}]'

payload = {
    "preferences": "Vegan, loves rice dishes",
    "allergies": "None",
    "budget": 200,
    "goal": "Weight Loss",
    "food_database": food_db_string
}

print("Sending request across the network...")
response = requests.post(url, json=payload)

if response.status_code == 200:
    print("\n✅ API SUCCESS! Response Payload:\n")
    print(response.json()["meal_plan"])
else:
    print(f"❌ API Error: {response.text}")
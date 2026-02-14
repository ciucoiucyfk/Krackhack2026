import json
import random

# ----------------------------
# CONFIG
# ----------------------------
NUM_EXAMPLES = 100
TOLERANCE = 0.10
OUTPUT_FILE = "Datasets/dataset.jsonl"

# ----------------------------
# LOAD FOOD DATABASE
# ----------------------------
with open("Datasets/dataset.json", "r") as f:
    foods = json.load(f)

# ----------------------------
# CATEGORY SPLIT
# ----------------------------
categories = {}

for food in foods:
    categories.setdefault(food["category"], []).append(food)

# ----------------------------
# TARGET GENERATOR
# ----------------------------
def generate_target():
    return {
        "calories": random.randint(1800, 2400),
        "protein": random.randint(75, 120),
        "carbs": random.randint(220, 320),
        "fat": random.randint(50, 90)
    }

# ----------------------------
# PORTION LOGIC (SMART)
# ----------------------------
def get_serving(category):
    if category == "grain":
        return random.randint(2, 3)   # 200–300g
    elif category in ["legume", "poultry", "meat"]:
        return random.randint(1, 2)   # 100–200g
    elif category == "vegetable":
        return random.randint(1, 2)
    elif category == "dairy":
        return random.randint(1, 2)
    elif category == "fruit":
        return 1
    else:
        return 1

# ----------------------------
# MACRO CALCULATION
# ----------------------------
def calculate_totals(plan):
    totals = {"calories": 0, "protein": 0, "carbs": 0, "fat": 0}

    for item in plan:
        factor = item["servings"]
        totals["calories"] += item["calories_kcal"] * factor
        totals["protein"] += item["protein_g"] * factor
        totals["carbs"] += item["carbs_g"] * factor
        totals["fat"] += item["fat_g"] * factor

    return totals

# ----------------------------
# TOLERANCE CHECK
# ----------------------------
def within_tolerance(totals, target):
    for key in target:
        if abs(totals[key] - target[key]) > target[key] * TOLERANCE:
            return False
    return True

# ----------------------------
# PLAN BUILDER (STRUCTURED)
# ----------------------------
def build_plan():
    plan = []

    # Breakfast
    breakfast_items = [
        random.choice(categories["grain"]),
        random.choice(categories["legume"] + categories["poultry"] + categories["dairy"])
    ]

    if random.random() < 0.5:
        breakfast_items.append(random.choice(categories["fruit"]))

    # Lunch
    lunch_items = [
        random.choice(categories["grain"]),
        random.choice(categories["legume"] + categories["poultry"] + categories["meat"]),
        random.choice(categories["vegetable"])
    ]

    # Dinner
    dinner_items = [
        random.choice(categories["legume"] + categories["poultry"] + categories["meat"]),
        random.choice(categories["vegetable"])
    ]

    if random.random() < 0.5:
        dinner_items.append(random.choice(categories["dairy"]))

    meals = {
        "Breakfast": breakfast_items,
        "Lunch": lunch_items,
        "Dinner": dinner_items
    }

    # Assign servings
    final_plan = []

    for meal in meals.values():
        for item in meal:
            final_plan.append({
                **item,
                "servings": get_serving(item["category"])
            })

    return meals, final_plan

# ----------------------------
# FORMAT OUTPUT
# ----------------------------
def format_output(meals, totals):
    text = "Meal Plan:\n\n"

    for meal_name, items in meals.items():
        text += f"{meal_name}:\n"
        for item in items:
            text += f"- {item['food_name']} ({item['servings']*100}g)\n"
        text += "\n"

    text += "Macro Summary:\n"
    text += f"Calories: {int(totals['calories'])} kcal\n"
    text += f"Protein: {int(totals['protein'])}g\n"
    text += f"Carbohydrates: {int(totals['carbs'])}g\n"
    text += f"Fat: {int(totals['fat'])}g"

    return text.strip()

# ----------------------------
# FORMAT INPUT
# ----------------------------
def format_input(target, plan):
    ingredients = list(set([item["food_name"] for item in plan]))

    return f"""You are a nutrition planning assistant.

Target Macros:
Calories: {target['calories']} kcal
Protein: {target['protein']}g
Carbohydrates: {target['carbs']}g
Fat: {target['fat']}g

Available Ingredients:
{', '.join(ingredients)}

Generate a structured 3-meal Indian diet plan using only the listed ingredients.
""".strip()

# ----------------------------
# DATASET GENERATION
# ----------------------------
count = 0

with open(OUTPUT_FILE, "w") as f:
    while count < NUM_EXAMPLES:

        target = generate_target()
        meals, full_plan = build_plan()

        totals = calculate_totals(full_plan)

        if not within_tolerance(totals, target):
            continue

        # Inject servings back into meals
        idx = 0
        for meal_name in meals:
            for i in range(len(meals[meal_name])):
                meals[meal_name][i] = full_plan[idx]
                idx += 1

        input_text = format_input(target, full_plan)
        output_text = format_output(meals, totals)

        json.dump({"input": input_text, "output": output_text}, f)
        f.write("\n")

        count += 1
        print("Generated:", count)

print("DONE — 2000 clean examples created.")

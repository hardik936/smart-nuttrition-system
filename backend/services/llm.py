from huggingface_hub import InferenceClient
import os
from dotenv import load_dotenv
from pathlib import Path
import json
import re

# Explicitly load .env from backend directory
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path, override=True)

HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

# Initialize the client
# Using a model that supports text_generation on free tier
MODEL_ID = "google/flan-t5-base"

client = InferenceClient(token=HUGGINGFACE_API_KEY)

def generate_meal_plan(calories: int, diet_type: str, allergies: str, context: list[str] = None) -> str:
    """
    Generates a 1-day meal plan using Hugging Face Inference API, augmented with local food context.
    Falls back to rule-based generation if API is unavailable.
    """
    if not HUGGINGFACE_API_KEY:
        return generate_fallback_plan(calories, diet_type, allergies, context)
        
    # Construct prompt with context (simplified for T5)
    context_str = ", ".join(context[:10]) if context else "common foods"
    
    prompt = (
        f"Create a {calories} calorie {diet_type} meal plan avoiding {allergies}. "
        f"Use these foods: {context_str}. "
        "Return ONLY a JSON array with objects having keys: 'meal' (e.g. Breakfast), 'food' (exact name from list), 'calories' (approx int). "
        "Example: [{\"meal\": \"Breakfast\", \"food\": \"Oatmeal\", \"calories\": 300}]"
    )

    try:
        response = client.text_generation(
            prompt,
            model=MODEL_ID,
            max_new_tokens=200,
            temperature=0.7,
            return_full_text=False
        )
        return response
    except Exception as e:
        print(f"Error generating meal plan with AI: {e}")
        # Fallback to rule-based generation
        return generate_fallback_plan(calories, diet_type, allergies, context)

def generate_fallback_plan(calories: int, diet_type: str, allergies: str, context: list[str] = None) -> str:
    """
    Generates a rule-based meal plan when AI is unavailable.
    """
    # Use context foods if available, otherwise use defaults
    if context and len(context) > 0:
        foods = [f.split('(')[0].strip() for f in context[:10]]
    else:
        foods = ["Oatmeal", "Eggs", "Chicken Breast", "Brown Rice", "Broccoli", "Salmon", "Sweet Potato", "Greek Yogurt", "Almonds", "Quinoa"]
    
    # Filter out allergies
    if allergies and allergies.lower() != "none":
        allergy_list = [a.strip().lower() for a in allergies.split(',')]
        foods = [f for f in foods if not any(allergy in f.lower() for allergy in allergy_list)]
    
    # Adjust based on diet type
    if diet_type.lower() in ["vegetarian", "vegan"]:
        foods = [f for f in foods if f.lower() not in ["chicken", "salmon", "eggs"]]
        if not foods:
            foods = ["Tofu", "Lentils", "Chickpeas", "Quinoa", "Spinach"]
    
    # Generate meal plan
    breakfast = foods[0] if len(foods) > 0 else "Oatmeal"
    lunch = foods[1] if len(foods) > 1 else "Salad"
    dinner = foods[2] if len(foods) > 2 else "Grilled Vegetables"
    snack = foods[3] if len(foods) > 3 else "Fruit"
    
    cal_breakfast = int(calories * 0.25)
    cal_lunch = int(calories * 0.35)
    cal_dinner = int(calories * 0.30)
    cal_snack = int(calories * 0.10)
    
    plan = f"""
🍽️ Your {calories} Calorie {diet_type} Meal Plan

🌅 Breakfast ({cal_breakfast} cal): {breakfast} with whole grain toast
🌞 Lunch ({cal_lunch} cal): {lunch} with mixed vegetables
🌙 Dinner ({cal_dinner} cal): {dinner} with side salad
🍎 Snack ({cal_snack} cal): {snack}

💡 Note: This plan uses foods from your database. Adjust portions to meet calorie targets.
"""
    return plan.strip()

def extract_food_from_text(text: str) -> list[dict]:
    """
    Extracts potential food items from natural language text using LLM.
    Returns a list of dicts with inferred name and optional nutrition.
    """
    if not HUGGINGFACE_API_KEY:
        # Simple fallback for demo without LLM
        return [{"name": text, "calories": 0, "protein": 0, "carbs": 0, "fat": 0}]

    prompt = (
        f"Extract foods from: '{text}'. "
        "Return strictly JSON list of objects. Each object needs: 'name' (string), 'calories' (int), 'protein' (g), 'carbs' (g), 'fat' (g). "
        "Estimate values if unknown. "
        "Example output: [{\"name\": \"Apple\", \"calories\": 95, \"protein\": 0.5, \"carbs\": 25, \"fat\": 0.3}]"
    )

    try:
        response = client.text_generation(
            prompt,
            model=MODEL_ID,
            max_new_tokens=300,
            temperature=0.1, # Low temp for structured output
            return_full_text=False
        )
        
        # heuristic to find JSON list in response
        match = re.search(r'\[.*\]', response, re.DOTALL)
        if match:
            json_str = match.group(0)
            return json.loads(json_str)
        else:
             # Fallback if no JSON found
            return [{"name": text, "calories": 0, "protein": 0, "carbs": 0, "fat": 0}]

    except Exception as e:
        print(f"LLM Extraction Error: {e}")
        return [{"name": text, "calories": 0, "protein": 0, "carbs": 0, "fat": 0}]

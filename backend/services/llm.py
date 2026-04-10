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
        f"Create a strict {calories} kcal {diet_type} daily meal plan that is highly satisfying, sustainable, and nutritionally complete for a real human. "
        f"CRITICAL ALLERGY AVOIDANCE: Do NOT include ANY ingredients related to {allergies} or their derivatives! "
        f"Ensure EVERY meal contains a balanced ratio of lean protein, complex carbohydrates, and healthy fats. Use these ingredients as inspiration: {context_str}. "
        "Return ONLY a JSON array with objects having keys: 'meal' (e.g. Breakfast), 'food' (e.g. '150g Grilled Chicken with 1 cup Brown Rice and 100g Roasted Broccoli'), 'calories' (approx int). "
        "Include exact metric amounts (grams, cups) for EVERY food item. Example: [{\"meal\": \"Breakfast\", \"food\": \"1 cup Oatmeal with 30g Almonds, 1 tbsp Peanut Butter, and 50g Berries\", \"calories\": 400}]"
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
        
        # Extended allergen matrix for better filtering
        allergen_map = {
            "dairy": ["milk", "cheese", "yogurt", "butter", "cream", "whey"],
            "nuts": ["almond", "peanut", "cashew", "walnut", "pecan", "macadamia", "nut"],
            "gluten": ["wheat", "bread", "pasta", "flour"],
            "seafood": ["salmon", "fish", "shrimp", "tuna", "crab"],
            "meat": ["chicken", "beef", "pork", "turkey"]
        }
        
        expanded_allergies = set(allergy_list)
        for allergy in allergy_list:
            for key, mapped_items in allergen_map.items():
                if allergy in key or key in allergy:
                    expanded_allergies.update(mapped_items)
                    
        foods = [f for f in foods if not any(allergen in f.lower() for allergen in expanded_allergies)]
    
    # Adjust based on diet type
    if diet_type.lower() in ["vegetarian", "vegan"]:
        foods = [f for f in foods if not any(meat in f.lower() for meat in ["chicken", "salmon", "beef", "pork", "turkey"])]
        if not foods:
            foods = ["150g Tofu", "1 cup Lentils", "1 cup Chickpeas", "1 cup Quinoa", "100g Spinach"]
    
    # Generate meal combinations with sizes and balanced macros
    breakfast_food = f"1 cup {foods[0]} with 1/2 cup Plant Milk, 30g Nuts, and 50g Berries" if len(foods) > 0 else "1 cup Oatmeal with 1 cup Almond Milk, 1 tbsp Peanut Butter, and 50g Blueberries"
    lunch_food = f"2 cups Mixed Salad with 150g {foods[1]}, 1/2 cup Quinoa, and 2 tbsp Olive Oil" if len(foods) > 1 else "2 cups Mixed Salad with 150g Grilled Chicken Breast, 1/2 cup Brown Rice, and 1/4 Avocado"
    dinner_food = f"150g Roasted {foods[2]} with 1 cup Quinoa and 100g Veggies" if len(foods) > 2 else "150g Grilled Salmon with 150g Roasted Vegetables and 1 medium Sweet Potato"
    snack_food = f"30g mixed seeds and 1 medium {foods[3]}" if len(foods) > 3 else "30g Walnuts, 1 medium Apple, and 1 string Cheese (or Vegan alternative)"
    
    cal_breakfast = int(calories * 0.25)
    cal_lunch = int(calories * 0.35)
    cal_dinner = int(calories * 0.30)
    cal_snack = int(calories * 0.10)
    
    plan = [
        {"meal": "Breakfast", "food": breakfast_food, "calories": cal_breakfast},
        {"meal": "Lunch", "food": lunch_food, "calories": cal_lunch},
        {"meal": "Dinner", "food": dinner_food, "calories": cal_dinner},
        {"meal": "Snack", "food": snack_food, "calories": cal_snack}
    ]
    
    return json.dumps(plan)

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

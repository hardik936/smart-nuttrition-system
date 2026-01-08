"""
Script to populate the database with initial food data from OpenFoodFacts.
Run this script from the project root.
"""
import sys
import os
import requests

# Add backend to sys.path so we can import core and models
# This assumes the script is run from project root (e.g. python scripts/import_data.py)
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

# Force DATABASE_URL to point to backend/nutritrack.db if not set
# This ensures we write to the same DB that the backend app uses
if not os.getenv("DATABASE_URL"):
    # Using absolute path to avoid ambiguity with relative paths
    db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend', 'nutritrack.db'))
    os.environ["DATABASE_URL"] = f"sqlite:///{db_path}"
    print(f"Using database at: {os.environ['DATABASE_URL']}")

# Now import backend modules
try:
    from core.database import SessionLocal
    from models.food import Food
except ImportError as e:
    print(f"Error importing backend modules: {e}")
    sys.exit(1)

def fetch_food_data(search_term):
    """Fetch food data from OpenFoodFacts."""
    url = f"https://world.openfoodfacts.org/cgi/search.pl"
    params = {
        "search_terms": search_term,
        "search_simple": 1,
        "action": "process",
        "json": 1,
        "page_size": 1
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if data.get("products"):
            product = data["products"][0]
            nutriments = product.get("nutriments", {})
            
            return {
                "name": product.get("product_name", search_term),
                "calories": nutriments.get("energy-kcal_100g", 0.0),
                "protein": nutriments.get("proteins_100g", 0.0),
                "carbs": nutriments.get("carbohydrates_100g", 0.0),
                "fat": nutriments.get("fat_100g", 0.0)
            }
        return None
    except Exception as e:
        print(f"Error fetching {search_term}: {e}")
        return None

def main():
    session = SessionLocal()
    
    foods_to_add = [
        "Apple", "Banana", "Chicken Breast", "White Rice", "Egg", 
        "Oatmeal", "Milk", "Broccoli", "Almonds", "Salmon",
        "Sweet Potato", "Spinach", "Greek Yogurt", "Quinoa", "Avocado"
    ]
    
    print("Starting data import...")
    
    for food_name in foods_to_add:
        # Check if exists
        existing = session.query(Food).filter(Food.name.ilike(f"%{food_name}%")).first()
        if existing:
            print(f"Skipped {food_name} (Exists as {existing.name})")
            continue
            
        # Fetch data
        print(f"Fetching data for {food_name}...")
        data = fetch_food_data(food_name)
        
        if data:
            # Create Food object
            # Ensure values are floats and not None
            new_food = Food(
                name=data["name"],
                calories=float(data["calories"] or 0.0),
                protein=float(data["protein"] or 0.0),
                carbs=float(data["carbs"] or 0.0),
                fat=float(data["fat"] or 0.0)
            )
            session.add(new_food)
            try:
                session.commit()
                print(f"Added {new_food.name}")
            except Exception as e:
                session.rollback()
                print(f"Failed to commit {food_name}: {e}")
        else:
            print(f"No data found for {food_name}")
            
    session.close()
    print("Import complete.")

if __name__ == "__main__":
    main()

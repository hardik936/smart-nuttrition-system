import sys
import os
from pathlib import Path

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from core.database import SessionLocal
from models.food import Food

def seed_foods():
    db = SessionLocal()
    try:
        foods = [
            Food(name="Steel Cut Oats", calories=150, protein=5, carbs=27, fat=2.5),
            Food(name="Greek Yogurt (Plain)", calories=100, protein=10, carbs=4, fat=0),
            Food(name="Grilled Chicken Breast", calories=165, protein=31, carbs=0, fat=3.6),
            Food(name="Quinoa", calories=120, protein=4, carbs=21, fat=1.9),
            Food(name="Almonds", calories=160, protein=6, carbs=6, fat=14),
            Food(name="Spinach", calories=23, protein=2.9, carbs=3.6, fat=0.4),
            Food(name="Avocado", calories=160, protein=2, carbs=8.5, fat=14.7),
        ]
        
        # Check if exists
        for food in foods:
            existing = db.query(Food).filter(Food.name == food.name).first()
            if not existing:
                db.add(food)
                print(f"Added: {food.name}")
            else:
                print(f"Skipped: {food.name} (Already exists)")
        
        db.commit()
        print("Seeding complete.")
    finally:
        db.close()

if __name__ == "__main__":
    seed_foods()

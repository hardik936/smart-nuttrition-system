import sys
import os
from pathlib import Path

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from core.database import SessionLocal
from models.food import Food

def list_foods():
    db = SessionLocal()
    try:
        foods = db.query(Food).all()
        print(f"Total foods found: {len(foods)}")
        print("-" * 30)
        for food in foods:
            print(f"- {food.name} ({food.calories} kcal)")
        print("-" * 30)
    finally:
        db.close()

if __name__ == "__main__":
    list_foods()

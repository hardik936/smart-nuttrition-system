from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.database import get_db
from models.food import Food
import schemas
from fastapi import HTTPException
from services.openfoodfacts import get_food_by_barcode

router = APIRouter()

@router.get("/search")
async def search_foods(q: str = "", db: Session = Depends(get_db)):
    """
    Search foods by name. Returns up to 10 matching results.
    """
    if not q:
        # Return all foods if no query
        foods = db.query(Food).limit(10).all()
    else:
        # Search by name (case-insensitive)
        foods = db.query(Food).filter(
            Food.name.ilike(f"%{q}%")
        ).limit(10).all()
    
    return [
        {
            "id": food.id,
            "name": food.name,
            "calories": food.calories,
            "protein": food.protein,
            "carbs": food.carbs,
            "fat": food.fat
        }
        for food in foods
    ]

@router.post("/", response_model=schemas.FoodOut, status_code=201)
def create_food(food: schemas.FoodCreate, db: Session = Depends(get_db)):
    """
    Create a new food item.
    """
    db_food = Food(
        name=food.name,
        calories=food.calories,
        protein=food.protein,
        carbs=food.carbs,
        fat=food.fat
    )
    db.add(db_food)
    db.commit()
    db.refresh(db_food)
    return db_food

@router.get("/barcode/{code}")
async def get_food_from_barcode(code: str):
    """
    Fetch food data from OpenFoodFacts by barcode.
    """
    food_data = get_food_by_barcode(code)
    if not food_data:
        raise HTTPException(status_code=404, detail="Product not found")
    return food_data

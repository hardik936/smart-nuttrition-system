from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from services.ml import NutritionRecommender
from models.food import Food
import schemas

router = APIRouter()

# Global instance
recommender = NutritionRecommender()

@router.on_event("startup")
async def startup_event():
    # We need a new session for startup
    from core.database import SessionLocal
    db = SessionLocal()
    try:
        recommender.train(db)
    finally:
        db.close()

@router.get("/{food_id}", response_model=List[schemas.FoodOut])
def get_recommendations(food_id: int, db: Session = Depends(get_db)):
    """Get content-based recommendations for a specific food."""
    recommended_ids = recommender.get_recommendations(food_id)
    
    if not recommended_ids:
        # If no recs found (e.g. food not found or empty DB), return empty list or 404?
        # Specification says "Handle the case where food_id is not found (404)" 
        # But recommender returns empty list if ID not found.
        # Let's check if the food exists first to give proper 404
        food = db.query(Food).filter(Food.id == food_id).first()
        if not food:
            raise HTTPException(status_code=404, detail="Food not found")
        return []

    # Fetch full objects
    recommendations = db.query(Food).filter(Food.id.in_(recommended_ids)).all()
    return recommendations

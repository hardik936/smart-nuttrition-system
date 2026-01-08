from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from core.deps import get_current_user
from core.database import get_db
from models.log import MealLog
from models.food import Food
from models.user import User
import schemas
from services.llm import extract_food_from_text
from pydantic import BaseModel

class VoiceRequest(BaseModel):
    text: str

router = APIRouter()

@router.post("/", response_model=schemas.LogOut)
def create_log(log: schemas.LogCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Check if food exists
    food = db.query(Food).filter(Food.id == log.food_id).first()
    if not food:
        raise HTTPException(status_code=404, detail="Food item not found")

    new_log = MealLog(
        user_id=current_user.id,
        food_id=log.food_id,
        quantity=log.quantity
    )
    db.add(new_log)

    # Gamification: Update Streak
    from datetime import datetime, timedelta
    today = datetime.utcnow().date()
    
    if current_user.last_logged_date != today:
        if current_user.last_logged_date == today - timedelta(days=1):
            # Continue streak
            current_user.streak_count = (current_user.streak_count or 0) + 1
        else:
            # Reset streak (or start new)
            # Only reset if it wasn't today (already checked)
            current_user.streak_count = 1
        
        current_user.last_logged_date = today
        db.add(current_user) # Ensure user update is tracked

    db.commit()
    db.refresh(new_log)
    db.refresh(new_log)
    return new_log

@router.post("/voice")
def process_voice_log(request: VoiceRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Process natural language text to extract food items.
    Tries to match extracted names with existing DB foods.
    """
    extracted_foods = extract_food_from_text(request.text)
    
    # Try to find matches in DB
    result = []
    for item in extracted_foods:
        # Simple case-insensitive match
        db_food = db.query(Food).filter(Food.name.ilike(f"%{item['name']}%")).first()
        if db_food:
            result.append({
                "name": db_food.name,
                "calories": db_food.calories,
                "protein": db_food.protein,
                "carbs": db_food.carbs,
                "fat": db_food.fat,
                "quantity": 100, # Default to 100g if not specified (LLM logic enhancement needed later for quantity)
                "match_found": True,
                "id": db_food.id
            })
        else:
            result.append({
                **item,
                "quantity": 100,
                "match_found": False
            })
            
    return result

@router.get("/", response_model=List[schemas.LogOut])
def get_logs(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Return logs for the current user for TODAY only
    from datetime import datetime, time
    
    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = datetime.utcnow().replace(hour=23, minute=59, second=59, microsecond=999999)

    logs = db.query(MealLog).filter(
        MealLog.user_id == current_user.id,
        MealLog.timestamp >= today_start,
        MealLog.timestamp <= today_end
    ).all()
    return logs

@router.delete("/{log_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_log(log_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    log = db.query(MealLog).filter(MealLog.id == log_id, MealLog.user_id == current_user.id).first()
    if not log:
        raise HTTPException(status_code=404, detail="Log not found")
    
    db.delete(log)
    db.commit()
    return None

@router.put("/{log_id}", response_model=schemas.LogOut)
def update_log_quantity(log_id: int, quantity: float, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    log = db.query(MealLog).filter(MealLog.id == log_id, MealLog.user_id == current_user.id).first()
    if not log:
        raise HTTPException(status_code=404, detail="Log not found")
    
    if quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be positive")

    log.quantity = quantity
    db.commit()
    db.refresh(log)
    return log

@router.get("/stats/weekly")
def get_weekly_stats(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    from datetime import timedelta, datetime
    from sqlalchemy import func, cast, Date

    today = datetime.utcnow().date()
    start_date = today - timedelta(days=6) # Last 7 days including today

    # Query to group by date and sum calories
    # Note: SQLite stores dates as strings, so we might need specific handling if using SQLite.
    # Assuming standard SQLAlchemy usage. If SQLite, simple date(timestamp) works.
    
    stats = db.query(
        func.date(MealLog.timestamp).label('date'),
        func.sum(MealLog.quantity * Food.calories / 100).label('calories')
    ).join(Food).filter(
        MealLog.user_id == current_user.id,
        MealLog.timestamp >= start_date
    ).group_by(func.date(MealLog.timestamp)).all()

    # Format result: fill in missing days with 0
    result = []
    stats_dict = {str(s.date): s.calories for s in stats}
    
    for i in range(7):
        d = (start_date + timedelta(days=i)).strftime("%Y-%m-%d")
        result.append({
            "date": d,
            "calories": stats_dict.get(d, 0)
        })
        
    return result

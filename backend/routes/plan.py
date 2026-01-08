from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from schemas import MealPlanRequest
from services.llm import generate_meal_plan
from core.database import get_db
from models.food import Food
from models.log import MealLog
from models.user import User
from core.deps import get_current_user
from typing import List
from pydantic import BaseModel
import json

router = APIRouter()

@router.post("/generate-plan")
async def create_meal_plan(request: MealPlanRequest, db: Session = Depends(get_db)):
    """
    Generates a meal plan based on user preferences and available ingredients.
    """
    try:
        # Fetch available foods from DB (limit to 50 for context window)
        foods = db.query(Food).limit(50).all()
        food_context = [f"{f.name} ({f.calories} kcal)" for f in foods]

        # Provide a default for allergies if None
        allergies = request.allergies if request.allergies else "None"
        
        plan_text = generate_meal_plan(request.calories, request.diet, allergies, context=food_context)
        
        # basic check if it's an error message
        if plan_text.startswith("Error"):
             raise HTTPException(status_code=503, detail=plan_text)

        # Attempt to parse JSON to ensure valid format, if LLM adhered to instructions
        # If not, we just return the text
        try:
            plan_json = json.loads(plan_text)
            return {"plan": plan_json}
        except json.JSONDecodeError:
            # Fallback if LLM didn't return pure JSON
            return {"plan": plan_text, "note": "Raw output returned"}
            
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class PlanItem(BaseModel):
    meal: str
    food: str
    calories: int | None = None

class CommitPlanRequest(BaseModel):
    plan: List[PlanItem]

@router.post("/commit")
async def commit_plan(request: CommitPlanRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Commits a generated meal plan to the user's daily logs.
    """
    count = 0
    from datetime import datetime, timedelta
    today = datetime.utcnow().date()
    # Update streak since we are logging meals
    if current_user.last_logged_date != today:
        if current_user.last_logged_date == today - timedelta(days=1):
             current_user.streak_count = (current_user.streak_count or 0) + 1
        else:
             current_user.streak_count = 1
        current_user.last_logged_date = today
        db.add(current_user)

    for item in request.plan:
        # Try to find food by name (fuzzy match or exact)
        # For MVP, simple exact match or first match containing string
        food = db.query(Food).filter(Food.name.ilike(f"%{item.food}%")).first()
        
        if not food:
            # If not found, use a placeholder or create one?
            # Creating one is risky without nutrition info.
            # Let's try to find a generic "Unknown" or just skip/warn?
            # Better: Search for "Custom" or create a temporary on the fly?
            # Let's check if we have a "Generic" item. If not, maybe skip logic for now or pick the first item in DB as fallback (bad idea).
            # Fallback: Create a temporary food item (if we had a user-specific food table).
            # MVP: Skip if not found, or maybe try harder to parse.
            # Let's create a "Smart Plan Item" which effectively is just a note if we can't find it.
            # Actually, let's use the first food in the DB if nothing matches, or better, don't log it.
            # Wait, the LLM uses context! So it SHOULD exist in the DB if the prompt worked.
            continue 

        # Default quantity 100g? LLM doesn't give quantity explicitly in the simple format.
        # Let's assume 1 serving / 100g for now.
        new_log = MealLog(
            user_id=current_user.id,
            food_id=food.id,
            quantity=100.0 # Default to 100g
        )
        db.add(new_log)
        count += 1
    
    db.commit()
    return {"message": f"Successfully committed {count} meals to your log!", "streak": current_user.streak_count}

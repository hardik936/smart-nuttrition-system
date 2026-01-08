import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime, timedelta
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from main import app
from core.database import get_db, Base, engine
from models.user import User
from models.food import Food
from models.log import MealLog
from core.deps import get_current_user

# Test client
client = TestClient(app)

def test_daily_logs_filtering():
    # Setup database
    Base.metadata.create_all(bind=engine)
    
    # Create a fresh dependency override
    def override_get_db():
        db = Session(bind=engine)
        try:
            yield db
        finally:
            db.close()
            
    app.dependency_overrides[get_db] = override_get_db
    
    # Create test data
    db = next(override_get_db())
    
    # Clear existing data to avoid conflicts
    db.query(MealLog).delete()
    db.query(User).delete()
    db.query(Food).delete()
    db.commit()
    
    # 1. Create User
    user = User(email="test@example.com", hashed_password="hashed_password")
    db.add(user)
    db.commit()
    db.refresh(user)
    
    # Override auth to return this user
    def override_get_current_user():
        return user
    app.dependency_overrides[get_current_user] = override_get_current_user
    
    # 2. Create Food
    food = Food(name="Apple", calories=50, protein=0, carbs=10, fat=0)
    db.add(food)
    db.commit()
    db.refresh(food)
    
    # 3. Create Log for YESTERDAY
    yesterday = datetime.utcnow() - timedelta(days=1)
    log_yesterday = MealLog(
        user_id=user.id,
        food_id=food.id,
        quantity=1.0,
        timestamp=yesterday
    )
    db.add(log_yesterday)
    
    # 4. Create Log for TODAY
    today = datetime.utcnow()
    # Simulating 150g of Apple
    log_today = MealLog(
        user_id=user.id,
        food_id=food.id,
        quantity=150.0,
        timestamp=today
    )
    db.add(log_today)
    db.commit()
    
    # 5. Call API
    response = client.get("/api/v1/logs/")
    assert response.status_code == 200
    data = response.json()
    
    print(f"Yesterday Log Date: {yesterday}")
    print(f"Today Log Date: {today}")
    print(f"Response Data: {data}")
    
    # 6. Verify only ONE log is returned (Today's)
    assert len(data) == 1
    assert data[0]["quantity"] == 150.0 # Should match input grams
    assert data[0]["food"]["name"] == "Apple"

if __name__ == "__main__":
    try:
        test_daily_logs_filtering()
        print("Test Passed: Daily logs filtering works correctly!")
    except AssertionError as e:
        print(f"Test Failed: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

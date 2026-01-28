from datetime import datetime
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    is_active: bool
    is_public: bool = True
    age: int | None = None
    weight: float | None = None
    height: float | None = None
    activity_level: str | None = None
    goal: str | None = None
    target_calories: int | None = None
    streak_count: int | None = 0

    class Config:
        from_attributes = True

class UserProfileUpdate(BaseModel):
    age: int | None = None
    weight: float | None = None
    height: float | None = None
    activity_level: str | None = None
    goal: str | None = None
    target_calories: int | None = None
    is_public: bool | None = None

class Token(BaseModel):
    access_token: str
    token_type: str

class FoodOut(BaseModel):
    id: int
    name: str
    calories: float
    protein: float
    carbs: float
    fat: float

    class Config:
        from_attributes = True

class FoodCreate(BaseModel):
    name: str
    calories: float
    protein: float
    carbs: float
    fat: float

class LogCreate(BaseModel):
    food_id: int
    quantity: float

class LogOut(BaseModel):
    id: int
    food: FoodOut
    quantity: float
    timestamp: datetime

    class Config:
        from_attributes = True

class MealPlanRequest(BaseModel):
    calories: int
    diet: str
    allergies: str | None = None

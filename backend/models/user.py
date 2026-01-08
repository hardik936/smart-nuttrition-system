from sqlalchemy import Boolean, Column, Integer, String, Date
from sqlalchemy.orm import relationship
from core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    # Profile fields
    age = Column(Integer, nullable=True)
    weight = Column(Integer, nullable=True) # in kg
    height = Column(Integer, nullable=True) # in cm
    activity_level = Column(String, nullable=True) # sedentary, light, moderate, active, very_active
    goal = Column(String, nullable=True) # lose_weight, maintain, gain_muscle
    goal = Column(String, nullable=True) # lose_weight, maintain, gain_muscle
    target_calories = Column(Integer, default=2000)

    # Gamification
    streak_count = Column(Integer, default=0)
    last_logged_date = Column(Date, nullable=True)

    # Relationship to logs
    logs = relationship("MealLog", back_populates="user")

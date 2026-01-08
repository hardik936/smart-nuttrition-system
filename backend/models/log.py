from datetime import datetime
from sqlalchemy import Column, Float, ForeignKey, Integer, DateTime
from sqlalchemy.orm import relationship
from core.database import Base

class MealLog(Base):
    __tablename__ = "meal_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    food_id = Column(Integer, ForeignKey("foods.id"))
    quantity = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="logs")
    food = relationship("Food", back_populates="logs")

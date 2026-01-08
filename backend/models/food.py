from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.orm import relationship
from core.database import Base

class Food(Base):
    __tablename__ = "foods"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    calories = Column(Float)
    protein = Column(Float)
    carbs = Column(Float)
    fat = Column(Float)

    # Relationship to logs
    logs = relationship("MealLog", back_populates="food")

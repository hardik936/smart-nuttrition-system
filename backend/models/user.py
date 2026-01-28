from sqlalchemy import Boolean, Column, Integer, String, Date, Table, ForeignKey
from sqlalchemy.orm import relationship
from core.database import Base

# Association table for many-to-many follower relationship
social_connections = Table(
    'social_connections', Base.metadata,
    Column('follower_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('followed_id', Integer, ForeignKey('users.id'), primary_key=True)
)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_public = Column(Boolean, default=True) # Public profile by default

    # Profile fields
    age = Column(Integer, nullable=True)
    weight = Column(Integer, nullable=True) # in kg
    height = Column(Integer, nullable=True) # in cm
    activity_level = Column(String, nullable=True) # sedentary, light, moderate, active, very_active
    goal = Column(String, nullable=True) # lose_weight, maintain, gain_muscle
    target_calories = Column(Integer, default=2000)

    # Gamification
    streak_count = Column(Integer, default=0)
    last_logged_date = Column(Date, nullable=True)

    # Relationship to logs
    logs = relationship("MealLog", back_populates="user")

    # Social Relationships
    followers = relationship(
        "User",
        secondary=social_connections,
        primaryjoin=id==social_connections.c.followed_id,
        secondaryjoin=id==social_connections.c.follower_id,
        backref="following"
    )

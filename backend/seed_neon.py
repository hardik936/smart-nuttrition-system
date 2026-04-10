import os
import sys

from dotenv import load_dotenv
from pathlib import Path

# Load from .env securely
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)

if not os.environ.get("DATABASE_URL"):
    os.environ["DATABASE_URL"] = "sqlite:///./nutritrack_v2.db"


from seed_data import seed_users, seed_foods
from core.database import Base, engine

print("Creating tables...")
Base.metadata.create_all(bind=engine)

print("Seeding foods...")
seed_foods()
print("Seeding users...")
seed_users()
print("Done!")

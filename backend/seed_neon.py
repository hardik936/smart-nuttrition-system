import os
import sys

# Set it properly in python
neon_url = "postgresql://neondb_owner:npg_0wYaA7RFiuxo@ep-weathered-wave-aioucfqo-pooler.c-4.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
os.environ["DATABASE_URL"] = neon_url

from seed_data import seed_users, seed_foods
from core.database import Base, engine

print("Creating tables...")
Base.metadata.create_all(bind=engine)

print("Seeding foods...")
seed_foods()
print("Seeding users...")
seed_users()
print("Done!")

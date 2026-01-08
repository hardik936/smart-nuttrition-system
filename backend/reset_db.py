from core.database import engine, Base
import models
import models.user
import models.log
import models.food

# CAUTION: This will drop all tables!
print("Dropping all tables...")
Base.metadata.drop_all(bind=engine)

print("Creating all tables...")
Base.metadata.create_all(bind=engine)
print("Database schema updated successfully.")

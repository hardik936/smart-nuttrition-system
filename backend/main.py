from fastapi import FastAPI
from core.database import engine, Base
# Import models to register them with SQLAlchemy metadata
import models

from routes import auth, logs

# Create tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(title="NutriTrack API")

from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost:5173",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(logs.router, prefix="/api/v1/logs", tags=["logs"])

from routes import recommendations
app.include_router(recommendations.router, prefix="/recommend", tags=["recommendations"])

from routes import ocr
app.include_router(ocr.router, prefix="/api/v1/ocr", tags=["ocr"])

from routes import plan
app.include_router(plan.router, prefix="/api/v1/plan", tags=["plan"])

from routes import foods
app.include_router(foods.router, prefix="/api/v1/foods", tags=["foods"])

from routes import social
app.include_router(social.router, prefix="/api/v1", tags=["social"])

@app.get("/")
def read_root():
    return {"message": "NutriTrack API is running"}

# Forced reload trigger

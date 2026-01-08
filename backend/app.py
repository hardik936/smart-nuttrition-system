"""
Entry point for the Smart Nutrition System FastAPI Backend.
"""
from fastapi import FastAPI

app = FastAPI(title="Smart Nutrition System")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Smart Nutrition System API"}

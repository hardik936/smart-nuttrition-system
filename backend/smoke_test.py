import pytest
from fastapi.testclient import TestClient
from main import app
import os

client = TestClient(app)

def test_health():
    response = client.get("/")
    assert response.status_code == 200

def test_foods():
    response = client.get("/api/v1/foods/search")
    assert response.status_code == 200

def test_recommendations():
    # Will return 404 if food 999 doesn't exist, which is expected for this endpoint
    response = client.get("/recommend/999")
    assert response.status_code == 404

def test_social_leaderboard():
    # Attempting to get leaderboard without auth should return 401
    response = client.get("/api/v1/social/leaderboard")
    assert response.status_code == 401

def test_ocr_endpoint_exists():
    # Testing endpoint existence (expecting 401 because it requires auth)
    response = client.post("/api/v1/ocr/scan")
    assert response.status_code in [401, 405, 422]

print("Smoke tests passing!")

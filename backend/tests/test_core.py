import pytest
import sys
from pathlib import Path

# Add backend directory to path
backend_path = Path(__file__).parent.parent
sys.path.append(str(backend_path))

from models.food import Food

def test_register_user(client):
    response = client.post(
        "/auth/register",
        json={"email": "test@example.com", "password": "password123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data

def test_login_user(client):
    # First register
    client.post(
        "/auth/register",
        json={"email": "login@example.com", "password": "securepassword"}
    )
    
    # Then login
    response = client.post(
        "/auth/token",
        data={"username": "login@example.com", "password": "securepassword"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_create_food_and_log_meal(client, db_session):
    # 1. Setup: Create user and login
    client.post("/auth/register", json={"email": "meal@example.com", "password": "pw"})
    login_res = client.post("/auth/token", data={"username": "meal@example.com", "password": "pw"})
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Setup: Pre-populate a food item in the DB
    apple = Food(name="Apple", calories=95, protein=0.5, carbs=25, fat=0.3)
    db_session.add(apple)
    db_session.commit()
    db_session.refresh(apple)

    # 3. Test: Log the meal
    response = client.post(
        "/logs/",
        json={"food_id": apple.id, "quantity": 1.0},
        headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["food"]["name"] == "Apple"
    assert data["quantity"] == 1.0

def test_unauthorized_log_access(client):
    # Try to access protected route without token
    response = client.post(
        "/logs/",
        json={"food_id": 1, "quantity": 1.0}
    )
    assert response.status_code == 401

import sys
import os
from pathlib import Path

# Add backend directory to path
backend_path = Path(__file__).parent
sys.path.append(str(backend_path))

from fastapi.testclient import TestClient
from main import app
from core.database import SessionLocal
from models.user import User

client = TestClient(app)

def test_login_flow():
    email = "repro_test@example.com"
    password = "password123"
    
    print(f"1. Attempting to register user {email}...")
    response = client.post("/auth/register", json={"email": email, "password": password})
    if response.status_code == 200:
        print("   -> Registration successful.")
    elif response.status_code == 400 and "already registered" in response.text:
        print("   -> User already exists (expected).")
    else:
        print(f"   -> Registration FAILED: {response.status_code} - {response.text}")
        return

    print(f"2. Attempting to login with {email}...")
    response = client.post("/auth/token", data={"username": email, "password": password})
    
    if response.status_code != 200:
        print(f"   -> Login FAILED: {response.status_code} - {response.text}")
        
        # Debug: Check if user exists in DB directly
        db = SessionLocal()
        user = db.query(User).filter(User.email == email).first()
        if user:
            print(f"      [DEBUG] User found in DB. ID: {user.id}, Is Active: {user.is_active}")
        else:
            print(f"      [DEBUG] User NOT FOUND in DB.")
        db.close()
        return

    data = response.json()
    token = data.get("access_token")
    if not token:
        print("   -> Login SUCCEEDED but no token returned!")
        print(f"      Response: {data}")
        return
        
    print(f"   -> Login SUCCEEDED. Token received.")
    
    print(f"3. Accessing protected endpoint (/auth/me)...")
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/auth/me", headers=headers)
    
    if response.status_code == 200:
        user_data = response.json()
        print(f"   -> Access SUCCEEDED. User: {user_data.get('email')}")
    else:
        print(f"   -> Access FAILED: {response.status_code} - {response.text}")

if __name__ == "__main__":
    test_login_flow()

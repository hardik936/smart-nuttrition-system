import requests
import sys
import json

# Configuration
BASE_URL = "http://127.0.0.1:8000"
EMAIL = "test@example.com"
PASSWORD = "password123"

def login():
    print(f"Attempting to login with {EMAIL}...")
    try:
        response = requests.post(f"{BASE_URL}/auth/token", data={
            "username": EMAIL,
            "password": PASSWORD
        })
        if response.status_code == 200:
            token = response.json()["access_token"]
            print("Login successful.")
            return token
        else:
            print(f"Login failed: {response.text}")
            return None
    except Exception as e:
        print(f"Connection error: {e}")
        return None

def test_generate_plan(token):
    print("Testing generate plan endpoint...")
    headers = {"Authorization": f"Bearer {token}"}
    
    payload = {
        "calories": 2000,
        "diet": "Balanced",
        "allergies": "None"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/v1/plan/generate-plan", json=payload, headers=headers)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Body: {response.text}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                if "plan" in data:
                    print("Plan generated successfully.")
                    if isinstance(data["plan"], list):
                        print("Plan is a valid list.")
                    else:
                        print("Plan is NOT a list (likely raw text).")
                    return True
                else:
                    print("Response missing 'plan' key.")
                    return False
            except json.JSONDecodeError:
                print("Response is not valid JSON.")
                return False
        else:
            print("Request failed.")
            return False
            
    except Exception as e:
        print(f"Error during generate plan: {e}")
        return False

def main():
    token = login()
    if not token:
        # Try to register if login fails, or just warn
        print("Login failed. Make sure the server is running and user exists.")
        sys.exit(1)
        
    if test_generate_plan(token):
        print("Plan generation test PASSED.")
    else:
        print("Plan generation test FAILED.")

if __name__ == "__main__":
    main()

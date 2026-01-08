import requests
import sys

# Configuration
BASE_URL = "http://127.0.0.1:8000"
EMAIL = "profile_test@example.com"
PASSWORD = "password123"

def login_or_register():
    print(f"Logging in or registering {EMAIL}...")
    # Try register
    requests.post(f"{BASE_URL}/auth/register", json={
        "email": EMAIL,
        "password": PASSWORD
    })
    
    # Try login
    response = requests.post(f"{BASE_URL}/auth/token", data={
        "username": EMAIL,
        "password": PASSWORD
    })
    
    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        print(f"Login failed: {response.text}")
        return None

def test_profile_update(token):
    headers = {"Authorization": f"Bearer {token}"}
    
    print("Testing profile update...")
    update_data = {
        "age": 30,
        "weight": 75.5,
        "height": 180,
        "activity_level": "moderate",
        "goal": "lose_weight",
        "target_calories": 2200
    }
    
    resp = requests.put(f"{BASE_URL}/auth/me", json=update_data, headers=headers)
    if resp.status_code != 200:
        print(f"Update failed: {resp.text}")
        return False
        
    data = resp.json()
    if data["age"] == 30 and data["weight"] == 75.5 and data["target_calories"] == 2200:
        print("Update successful, data verified in response.")
        return True
    else:
        print(f"Data verification failed in response: {data}")
        return False

def test_profile_get(token):
    headers = {"Authorization": f"Bearer {token}"}
    print("Testing profile retrieval...")
    
    resp = requests.get(f"{BASE_URL}/auth/me", headers=headers)
    if resp.status_code != 200:
        print(f"Get failed: {resp.text}")
        return False
        
    data = resp.json()
    if data["age"] == 30 and data["activity_level"] == "moderate":
        print("Get successful, data verified.")
        return True
    else:
        print(f"Data verification failed on GET: {data}")
        return False

def main():
    token = login_or_register()
    if not token:
        sys.exit(1)
        
    if test_profile_update(token) and test_profile_get(token):
        print("Profile verification PASSED.")
    else:
        print("Profile verification FAILED.")
        sys.exit(1)

if __name__ == "__main__":
    main()

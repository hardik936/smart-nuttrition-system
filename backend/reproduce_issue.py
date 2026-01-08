import requests
import sys

# Configuration
BASE_URL = "http://127.0.0.1:8000"
# Use a test user credentials. You might need to adjust this if this user doesn't exist
# or create a new user effectively.
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
            # Try to register if login fails?
            return None
    except Exception as e:
        print(f"Connection error: {e}")
        return None

def create_test_user():
    print("Attempting to create test user...")
    try:
        response = requests.post(f"{BASE_URL}/auth/register", json={
            "email": EMAIL,
            "password": PASSWORD
        })
        if response.status_code == 200 or response.status_code == 400: # 400 likely means already exists
            print("User creation step done (created or already exists).")
            return True
        else:
            print(f"Registration failed: {response.text}")
            return False
    except Exception as e:
        print(f"Connection error: {e}")
        return False

def add_meal_log(token):
    print("Attempting to add meal log...")
    headers = {"Authorization": f"Bearer {token}"}
    
    # First get a food item to log
    try:
        foods_resp = requests.get(f"{BASE_URL}/api/v1/foods/search", headers=headers)
        if foods_resp.status_code != 200:
            print(f"Failed to fetch foods: {foods_resp.text}")
            return False
        
        foods = foods_resp.json()
        if not foods:
            print("No foods found to log.")
            return False
            
        food_id = foods[0]["id"]
        print(f"Found food id: {food_id}, logging it...")
        
        # Log the meal
        log_data = {
            "food_id": food_id,
            "quantity": 2.0
        }
        
        response = requests.post(f"{BASE_URL}/logs/", json=log_data, headers=headers)
        
        if response.status_code == 200:
            print("Successfully added meal log!")
            print(response.json())
            return True
        else:
            print(f"Failed to add meal log: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"Error during add meal logic: {e}")
        return False

def main():
    if not create_test_user():
        print("Could not ensure user exists.")
    
    token = login()
    if not token:
        print("Aborting because login failed.")
        sys.exit(1)
        
    if add_meal_log(token):
        print("Backend verification PASSED.")
    else:
        print("Backend verification FAILED.")
        sys.exit(1)

if __name__ == "__main__":
    main()

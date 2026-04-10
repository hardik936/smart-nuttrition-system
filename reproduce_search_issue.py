import requests
import sys
import json

# Configuration
BASE_URL = "http://127.0.0.1:8000"
EMAIL = "test@example.com"
PASSWORD = "password123"

def login():
    try:
        response = requests.post(f"{BASE_URL}/auth/token", data={
            "username": EMAIL,
            "password": PASSWORD
        })
        if response.status_code == 200:
            return response.json()["access_token"]
        return None
    except Exception:
        return None

def test_search_apple(token):
    print("Testing search for 'apple'...")
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(f"{BASE_URL}/api/v1/foods/search?q=apple", headers=headers)
        
        if response.status_code == 200:
            foods = response.json()
            print(f"Found {len(foods)} results.")
            
            apple_found = False
            for food in foods:
                print(f"- {food['name']} (Cal: {food.get('calories')}, P: {food.get('protein')}, C: {food.get('carbs')}, F: {food.get('fat')})")
                if "apple" in food['name'].lower():
                    apple_found = True
                    # Check if macros are non-zero (or present)
                    if food.get('calories') is not None:
                        print(f"  -> Macros present for {food['name']}")
                    else:
                        print(f"  -> WARNING: Macros missing for {food['name']}")

            if apple_found:
                print("PASS: Apple found in results.")
                return True
            else:
                print("FAIL: Apple NOT found in results.")
                return False
        else:
            print(f"Search request failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"Error during search: {e}")
        return False

def main():
    token = login()
    if not token:
        print("Login failed. Check server status.")
        sys.exit(1)
        
    test_search_apple(token)

if __name__ == "__main__":
    main()

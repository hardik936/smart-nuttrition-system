import requests
import sys

BASE_URL = "http://localhost:8000"

def test_api():
    email = "test_api_v2@example.com"
    password = "password123"

    # 1. Register
    print(f"Registering {email}...")
    resp = requests.post(f"{BASE_URL}/auth/register", json={"email": email, "password": password})
    if resp.status_code == 200:
        print("Registration successful")
    elif resp.status_code == 400 and "Email already registered" in resp.text:
        print("User already exists, proceeding to login")
    else:
        print(f"Registration failed: {resp.status_code} {resp.text}")
        sys.exit(1)

    # 2. Login
    print("Logging in...")
    resp = requests.post(f"{BASE_URL}/auth/token", data={"username": email, "password": password})
    if resp.status_code != 200:
        print(f"Login failed: {resp.status_code} {resp.text}")
        sys.exit(1)
    
    token = resp.json()["access_token"]
    print(f"Got token: {token[:10]}...")
    headers = {"Authorization": f"Bearer {token}"}

    # 3. Create Log
    print("Creating log...")
    # Assuming food_id=1 exists
    log_data = {"food_id": 1, "quantity": 1.5}
    resp = requests.post(f"{BASE_URL}/logs/", json=log_data, headers=headers)
    if resp.status_code != 200:
        print(f"Create log failed: {resp.status_code} {resp.text}")
        sys.exit(1)
    print("Log created successfully")

    # 4. Get Logs
    print("Fetching logs...")
    resp = requests.get(f"{BASE_URL}/logs/", headers=headers)
    if resp.status_code != 200:
        print(f"Get logs failed: {resp.status_code} {resp.text}")
        sys.exit(1)
    
    logs = resp.json()
    print(f"Found {len(logs)} logs")
    print(logs)
    if len(logs) > 0:
        print("Verification PASSED")
    else:
        print("Verification FAILED (No logs found)")

if __name__ == "__main__":
    try:
        test_api()
    except Exception as e:
        print(f"An error occurred: {e}")

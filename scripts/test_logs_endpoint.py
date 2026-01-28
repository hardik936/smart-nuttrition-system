import requests

BASE_URL = "http://localhost:8000"

def test_logs():
    # 1. Login
    res = requests.post(f"{BASE_URL}/auth/token", data={"username": "usera@test.com", "password": "password123"})
    if res.status_code != 200:
        print("Login failed:", res.text)
        return
    token = res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Get Logs
    print("Fetching logs...")
    try:
        res = requests.get(f"{BASE_URL}/api/v1/logs/", headers=headers)
        print(f"Status: {res.status_code}")
        print(f"Response: {res.text}")
    except Exception as e:
        print(f"Exception: {e}")

    # 3. Get Stats
    print("Fetching stats...")
    try:
        res = requests.get(f"{BASE_URL}/api/v1/logs/stats/weekly", headers=headers)
        print(f"Status: {res.status_code}")
        print(f"Response: {res.text}")
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    test_logs()

import requests
import sys

BASE_URL = "http://localhost:8000"

def test_recs():
    food_id = 1
    print(f"Fetching recommendations for Food ID {food_id}...")
    
    url = f"{BASE_URL}/recommend/{food_id}"
    try:
        resp = requests.get(url)
    except requests.exceptions.ConnectionError:
        print("Backend not reachable.")
        sys.exit(1)

    if resp.status_code == 200:
        recs = resp.json()
        print(f"Success! Got {len(recs)} recommendations.")
        for item in recs:
            print(f"- {item['name']} (Cal: {item['calories']})")
    elif resp.status_code == 404:
        print("Food not found (404).")
    else:
        print(f"Failed: {resp.status_code} {resp.text}")
        sys.exit(1)

if __name__ == "__main__":
    test_recs()

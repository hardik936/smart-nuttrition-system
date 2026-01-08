import requests
import json

def test_meal_plan():
    url = "http://127.0.0.1:8000/api/v1/plan/generate-plan"
    
    payload = {
        "calories": 2000,
        "diet": "Vegetarian",
        "allergies": "Peanuts"
    }

    print(f"Sending request to {url} with payload: {payload}")
    
    try:
        response = requests.post(url, json=payload)
        
        if response.status_code == 200:
            print("\nSuccess! Generated Meal Plan:")
            data = response.json()
            print(json.dumps(data, indent=2))
        else:
            print(f"\nFailed with status {response.status_code}:")
            print(response.text)
            
    except Exception as e:
        print(f"\nAn error occurred: {e}")

if __name__ == "__main__":
    test_meal_plan()

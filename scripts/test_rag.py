import requests
import json

URL = "http://127.0.0.1:8000/api/v1/plan/generate-plan"

def test_rag_plan():
    print(f"Requesting meal plan from: {URL}")
    
    payload = {
        "calories": 2000,
        "diet": "High Protein",
        "allergies": "None"
    }
    
    try:
        response = requests.post(URL, json=payload)
        response.raise_for_status()
        
        data = response.json()
        print("\n--- API Response ---")
        # Handle potential raw text vs json object
        plan = data.get("plan", data)
        print(json.dumps(plan, indent=2))
        
        # Verification Logic
        plan_str = json.dumps(plan).lower()
        expected_items = ["steel cut oats", "greek yogurt", "grilled chicken", "quinoa", "almonds", "spinach", "avocado"]
        
        print("\n--- RAG Verification ---")
        found = [item for item in expected_items if item in plan_str]
        
        if found:
            print(f"✅ RAG SUCCESS! Found database items in plan: {', '.join(found)}")
        else:
            print("❌ RAG WARNING: No database items found in plan. The LLM might have ignored the context.")
            
    except Exception as e:
        print(f"Request failed: {e}")
        if hasattr(e, 'response') and e.response:
             print(e.response.text)

if __name__ == "__main__":
    test_rag_plan()

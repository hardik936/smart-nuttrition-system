import requests
import sys

BASE_URL = "http://127.0.0.1:8000"

def register_user(email, password):
    # Try logging in first
    res = requests.post(f"{BASE_URL}/auth/token", data={"username": email, "password": password})
    if res.status_code == 200:
        return res.json()["access_token"]
    
    # Register if login fails (assuming it failed because user doesn't exist)
    res = requests.post(f"{BASE_URL}/auth/register", json={"email": email, "password": password})
    if res.status_code == 200:
        # Login to get token
        res = requests.post(f"{BASE_URL}/auth/token", data={"username": email, "password": password})
        return res.json()["access_token"]
    else:
        print(f"Failed to register/login {email}: {res.text}")
        return None

def test_social_flow():
    print("Testing Social Features Backend...")
    
    # Create User A and User B
    token_a = register_user("usera@test.com", "password123")
    token_b = register_user("userb@test.com", "password123")
    
    if not token_a or not token_b:
        print("Failed to get tokens")
        return

    headers_a = {"Authorization": f"Bearer {token_a}"}
    headers_b = {"Authorization": f"Bearer {token_b}"}

    # Get IDs
    user_a = requests.get(f"{BASE_URL}/auth/me", headers=headers_a).json()
    user_b = requests.get(f"{BASE_URL}/auth/me", headers=headers_b).json()
    id_a = user_a["id"]
    id_b = user_b["id"]
    print(f"User A ID: {id_a}, User B ID: {id_b}")

    # 1. User A follows User B
    print("\n1. Testing Follow...")
    res = requests.post(f"{BASE_URL}/api/v1/social/follow/{id_b}", headers=headers_a)
    if res.status_code == 200:
        print("✅ User A followed User B")
    elif "already following" in res.text:
         print("✅ User A already followed User B")
    else:
        print(f"❌ Failed to follow: {res.text}")

    # 2. Check User A's friends
    print("\n2. Checking Friends List...")
    res = requests.get(f"{BASE_URL}/api/v1/social/friends", headers=headers_a)
    friends = res.json()
    if any(f["id"] == id_b for f in friends):
        print("✅ User B found in User A's friend list")
    else:
        print("❌ User B NOT found in User A's friend list")

    # 3. Check Leaderboard
    print("\n3. Checking Leaderboard...")
    res = requests.get(f"{BASE_URL}/api/v1/social/leaderboard", headers=headers_a)
    leaderboard = res.json()
    if any(u["id"] == id_b for u in leaderboard):
         print("✅ User B is visible on leaderboard")
    else:
         print("⚠️ User B not on leaderboard (Check if streak > 0 or public)")

    # 4. Set User B to Private
    print("\n4. Setting User B to Private...")
    res = requests.put(f"{BASE_URL}/auth/me", json={"is_public": False}, headers=headers_b)
    if res.status_code == 200:
        print("✅ User B is now private")
    else:
        print(f"❌ Failed to update privacy: {res.text}")

    # 5. Check Leaderboard again
    print("\n5. Checking Leaderboard again (User B should be gone)...")
    res = requests.get(f"{BASE_URL}/api/v1/social/leaderboard", headers=headers_a)
    leaderboard = res.json()
    if any(u["id"] == id_b for u in leaderboard):
         print("❌ User B is STILL visible on leaderboard!")
    else:
         print("✅ User B is hidden from leaderboard")
         
    # Reset User B to Public
    requests.put(f"{BASE_URL}/auth/me", json={"is_public": True}, headers=headers_b)

if __name__ == "__main__":
    try:
        test_social_flow()
    except Exception as e:
        print(f"Test failed with error: {e}")

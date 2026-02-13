
import requests
import time
import subprocess
import os
import signal

def test_cors():
    print("Testing CORS configuration...")
    try:
        # Check if backend is running, if not, this test assumes manual start or existing process
        # For this script, we'll try to hit the running local backend
        response = requests.options(
            "http://127.0.0.1:8000/auth/token",
            headers={
                "Origin": "http://localhost:5173",
                "Access-Control-Request-Method": "POST"
            },
            timeout=5
        )
        
        if response.status_code == 200 and response.headers.get("access-control-allow-origin") == "http://localhost:5173":
            print("SUCCESS: CORS Preflight for localhost:5173 accepted.")
        else:
            print(f"FAILURE: CORS Preflight failed. Status: {response.status_code}, Headers: {response.headers}")

        # Test allowed origin
        response_prod = requests.options(
            "http://127.0.0.1:8000/auth/token",
            headers={
                "Origin": "https://smart-nutrition-frontend.onrender.com",
                "Access-Control-Request-Method": "POST"
            },
            timeout=5
        )
         
        if response_prod.status_code == 200 and response_prod.headers.get("access-control-allow-origin") == "https://smart-nutrition-frontend.onrender.com":
             print("SUCCESS: CORS Preflight for production accepted.")
        else:
             print(f"FAILURE: CORS Preflight for production failed. Status: {response_prod.status_code}, Headers: {response_prod.headers}")


    except Exception as e:
        print(f"Error testing CORS: {e}")

if __name__ == "__main__":
    test_cors()

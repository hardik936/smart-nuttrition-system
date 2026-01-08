from fastapi import FastAPI
import uvicorn
import sys

print("Starting minimal server...")
app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    try:
        print("Invoking uvicorn.run...")
        uvicorn.run(app, host="127.0.0.1", port=8001)
    except Exception as e:
        print(f"Error: {e}")

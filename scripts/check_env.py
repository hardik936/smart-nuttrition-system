from pathlib import Path
from dotenv import load_dotenv
import os

def check():
    # Same logic as llm.py
    # Starting from scripts/.. which is root, then backend/.env
    # But llm.py is in backend/services/..
    
    # Let's check from the script's perspective relative to project root
    # script is in project/scripts/
    project_root = Path(__file__).parent.parent
    backend_dir = project_root / 'backend'
    env_path = backend_dir / '.env'
    
    print(f"Checking for .env at: {env_path}")
    if not env_path.exists():
        print("❌ .env file NOT FOUND at this path.")
        return

    print("✅ .env file found.")
    
    # Try loading
    load_dotenv(dotenv_path=env_path)
    
    key = os.getenv("HUGGINGFACE_API_KEY")
    if key:
        print("✅ HUGGINGFACE_API_KEY is present.")
        print(f"Key length: {len(key)}")
        if key.startswith("hf_"):
            print("✅ Key starts with 'hf_'")
        else:
            print("⚠️ Key does NOT start with 'hf_' (Warning)")
    else:
        print("❌ HUGGINGFACE_API_KEY is missing or empty.")
        
        # Print file content with masking to debug syntax
        print("\n--- Raw File Content (Masked) ---")
        try:
            with open(env_path, 'r') as f:
                lines = f.readlines()
                for i, line in enumerate(lines):
                    line = line.strip()
                    if "=" in line:
                        key, val = line.split("=", 1)
                        # Mask value
                        masked_val = val[:2] + "****" + val[-2:] if len(val) > 4 else "****"
                        print(f"Line {i+1}: {key}={masked_val}")
                    else:
                        print(f"Line {i+1}: {line}")
        except Exception as e:
            print(f"Error reading file: {e}")


if __name__ == "__main__":
    check()

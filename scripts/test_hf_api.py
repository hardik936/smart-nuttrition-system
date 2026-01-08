import os
from pathlib import Path
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

# Load env
env_path = Path(__file__).parent.parent / 'backend' / '.env'
load_dotenv(dotenv_path=env_path, override=True)

HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
MODEL_ID = "mistralai/Mistral-7B-Instruct-v0.3"

print(f"API Key present: {bool(HUGGINGFACE_API_KEY)}")
print(f"API Key length: {len(HUGGINGFACE_API_KEY) if HUGGINGFACE_API_KEY else 0}")
print(f"Model: {MODEL_ID}")
print("-" * 50)

client = InferenceClient(token=HUGGINGFACE_API_KEY)

# Simple test
prompt = "<s>[INST] Say 'Hello World' [/INST]"

try:
    print("Testing text_generation...")
    response = client.text_generation(
        prompt,
        model=MODEL_ID,
        max_new_tokens=50,
        temperature=0.7,
        return_full_text=False
    )
    print(f"✅ SUCCESS: {response}")
except Exception as e:
    print(f"❌ FAILED: {e}")

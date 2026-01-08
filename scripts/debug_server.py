import sys
import os

# Add backend to path
current_dir = os.getcwd()
backend_dir = os.path.join(current_dir, 'backend')
sys.path.append(backend_dir)

print(f"Adding {backend_dir} to path")

try:
    print("Attempting to import main...")
    import main
    print("Successfully imported main.")
    print(f"App: {main.app}")
except Exception as e:
    print(f"CRITICAL ERROR: {e}")
    import traceback
    traceback.print_exc()

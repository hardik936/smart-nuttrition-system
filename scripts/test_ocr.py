import requests
import sys
import os

def test_ocr(image_path):
    url = "http://127.0.0.1:8000/api/v1/ocr/scan"
    
    if not os.path.exists(image_path):
        print(f"Error: Image file not found at {image_path}")
        return

    print(f"Sending {image_path} to {url}...")
    
    try:
        with open(image_path, 'rb') as f:
            files = {'file': ('label.png', f, 'image/png')}
            response = requests.post(url, files=files)
            
        if response.status_code == 200:
            print("Success! Extracted Data:")
            print(response.json())
        else:
            print(f"Failed with status {response.status_code}:")
            print(response.text)
            
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # The image path will be passed as an argument or defaulted
    if len(sys.argv) > 1:
        img_path = sys.argv[1]
    else:
        # Default to the generated artifact path logic - I will need to find where generate_image saves it.
        # For now, I'll let the user/agent call it with the right path.
        print("Usage: python test_ocr.py <path_to_image>")
        sys.exit(1)

    test_ocr(img_path)

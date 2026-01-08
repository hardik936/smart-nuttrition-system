import io
import re
import pytesseract
from PIL import Image, ImageOps, ImageEnhance

# Set Tesseract Path explicitly for Windows
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def parse_nutrition_label(image_bytes: bytes) -> dict:
    """
    Parses a nutrition label image and extracts values for Calories, Protein, Carbs, and Fat.
    """
    try:
        # Load image from bytes
        image = Image.open(io.BytesIO(image_bytes))
        
        # Preprocessing for better OCR
        # 1. Convert to grayscale
        image = image.convert('L')
        
        # 2. Increase contrast
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(2.0)
        
        # 3. Binarize (optional, but handling via simple contrast for now)
        
        # Extract text using Tesseract
        text = pytesseract.image_to_string(image)
        
        print("----- OCR EXTRACTED TEXT START -----")
        print(text)
        print("----- OCR EXTRACTED TEXT END -----")
        
        # Initialize result dictionary
        result = {
            "calories": 0.0,
            "protein": 0.0,
            "carbs": 0.0,
            "fat": 0.0
        }
        
        # Helper function to clean extracted value
        def extract_value(pattern, text, default=0.0):
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                val_str = match.group(1).lower()
                # Remove common units and whitespace
                val_str = re.sub(r'[mg\s]', '', val_str) 
                try:
                    return float(val_str)
                except ValueError:
                    return default
            return default

        # Regex patterns
        # Calories: Look for "Calories" or "Energy" followed by digits
        result["calories"] = extract_value(r'(?:Calories|Energy|kcal).*?(\d+(?:\.\d+)?)', text)
        
        # Protein: Look for "Protein" followed by digits
        result["protein"] = extract_value(r'Protein.*?(\d+(?:\.\d+)?)', text)
        
        # Carbohydrates: Look for "Carbohydrate", "Carbs", "Total Carb"
        result["carbs"] = extract_value(r'(?:Carbohydrate|Carbs|Total Carb).*?(\d+(?:\.\d+)?)', text)
        
        # Fat: Look for "Total Fat", "Fat"
        result["fat"] = extract_value(r'(?:Total Fat|Fat).*?(\d+(?:\.\d+)?)', text)

        # Name Guessing Logic
        # Strategy: Look for the first line that is NOT a nutrition fact header or number
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        name_guess = ""
        
        # Keywords to skip
        skip_keywords = ["nutrition", "facts", "serving", "size", "amount", "calories", "daily", "value", "total", "fat", "cholesterol", "sodium", "carbohydrate", "protein", "vitamin", "percent", "ingredients", "contains"]
        
        for line in lines:
            # Skip short lines or lines with digits (likely values)
            if len(line) < 4: 
                continue
            if any(char.isdigit() for char in line):
                continue
                
            # Skip lines containing nutrition keywords
            if any(keyword in line.lower() for keyword in skip_keywords):
                continue
            
            # If we pass all checks, this might be the name
            name_guess = line
            break
            
        result["name_guess"] = name_guess
        
        return result
        
    except Exception as e:
        print(f"Error parsing nutrition label: {e}")
        return {
            "calories": 0.0,
            "protein": 0.0,
            "carbs": 0.0,
            "fat": 0.0,
            "error": str(e)
        }

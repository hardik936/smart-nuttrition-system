import io
import re
import pytesseract
from PIL import Image, ImageOps, ImageEnhance

import os

# Set Tesseract Path explicitly for Windows, otherwise rely on PATH (Linux/Render)
if os.name == 'nt':
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

import json
from services.llm import client, MODEL_ID, HUGGINGFACE_API_KEY

def parse_nutrition_label(image_bytes: bytes) -> dict:
    """
    Parses a nutrition label image using OCR and extracts structured values using HuggingFace LLM.
    """
    try:
        # Load image from bytes
        image = Image.open(io.BytesIO(image_bytes))
        
        # Resize image to prevent Tesseract from hanging on high-res phone photos
        max_dimension = 1200
        if max(image.size) > max_dimension:
            image.thumbnail((max_dimension, max_dimension), Image.Resampling.LANCZOS)
            
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
        
        # 4. Use LLM to extract structured data instead of regexes
        if HUGGINGFACE_API_KEY:
            prompt = (
                f"Extract nutrition facts from this text: '{text}'. "
                "Return ONLY a JSON object with strictly these keys: 'name_guess' (string), "
                "'serving_size_g' (float, the grams in parenthesis of the serving size, or 100.0 if not listed), "
                "'calories' (float, from the label), 'protein' (float, from the label), "
                "'carbs' (float, from the label), 'fat' (float, from the label). "
                "Do NOT scale or convert the numbers. Just extract them exactly as printed. "
                "Example output: {\"name_guess\": \"Oats\", \"serving_size_g\": 50.0, \"calories\": 250.0, \"protein\": 5.0, \"carbs\": 40.0, \"fat\": 8.0}"
            )
            try:
                response = client.text_generation(
                    prompt,
                    model=MODEL_ID,
                    max_new_tokens=200,
                    temperature=0.1,
                    return_full_text=False
                )
                
                # heuristic to find JSON object in response
                match = re.search(r'\{.*\}', response, re.DOTALL)
                if match:
                    json_str = match.group(0)
                    parsed_json = json.loads(json_str)
                    
                    serving_size_g = float(parsed_json.get("serving_size_g", 100.0))
                    if serving_size_g <= 0: serving_size_g = 100.0
                    multiplier = 100.0 / serving_size_g

                    return {
                        "name_guess": str(parsed_json.get("name_guess", "")),
                        "calories": round(float(parsed_json.get("calories", 0.0)) * multiplier, 2),
                        "protein": round(float(parsed_json.get("protein", 0.0)) * multiplier, 2),
                        "carbs": round(float(parsed_json.get("carbs", 0.0)) * multiplier, 2),
                        "fat": round(float(parsed_json.get("fat", 0.0)) * multiplier, 2)
                    }
            except Exception as e:
                print(f"LLM Extraction failed, falling back to regex: {e}")

        # --- Fallback Regex Logic (if LLM fails) ---
        result = {
            "calories": 0.0,
            "protein": 0.0,
            "carbs": 0.0,
            "fat": 0.0
        }
        
        def extract_value(pattern, txt, default=0.0):
            m = re.search(pattern, txt, re.IGNORECASE)
            if m:
                val_str = m.group(1).lower()
                val_str = re.sub(r'[mg\s]', '', val_str) 
                try:
                    return float(val_str)
                except ValueError:
                    return default
            return default

        serving_size_g = extract_value(r'Serving\s*Size.*?(\d+(?:\.\d+)?)\s*g', text, 100.0)
        if serving_size_g <= 0: serving_size_g = 100.0
        multiplier = 100.0 / serving_size_g

        result["calories"] = round(extract_value(r'(?:Calories|Energy|kcal).*?(\d+(?:\.\d+)?)', text) * multiplier, 2)
        result["protein"] = round(extract_value(r'Protein.*?(\d+(?:\.\d+)?)', text) * multiplier, 2)
        result["carbs"] = round(extract_value(r'(?:Carbohydrate|Carbs|Total Carb).*?(\d+(?:\.\d+)?)', text) * multiplier, 2)
        result["fat"] = round(extract_value(r'(?:Total Fat|Fat).*?(\d+(?:\.\d+)?)', text) * multiplier, 2)

        lines = [line.strip() for line in text.split('\n') if line.strip()]
        name_guess = ""
        skip_keywords = ["nutrition", "facts", "serving", "size", "amount", "calories", "daily", "value", "total", "fat", "cholesterol", "sodium", "carbohydrate", "protein", "vitamin", "percent", "ingredients", "contains"]
        
        for line in lines:
            if len(line) < 4: continue
            if any(char.isdigit() for char in line): continue
            if any(keyword in line.lower() for keyword in skip_keywords): continue
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

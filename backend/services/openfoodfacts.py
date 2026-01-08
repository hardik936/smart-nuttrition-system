import requests

def get_food_by_barcode(barcode: str) -> dict:
    """
    Fetches food metadata from OpenFoodFacts using the barcode.
    Returns a dictionary matching the nutrition structure.
    """
    url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
    
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        if data.get('status') != 1:
            return None # Product not found
            
        product = data.get('product', {})
        nutriments = product.get('nutriments', {})
        
        # Extract relevant fields with safe defaults
        return {
            "name": product.get('product_name', 'Unknown Product'),
            "calories": float(nutriments.get('energy-kcal_100g', 0) or 0),
            "protein": float(nutriments.get('proteins_100g', 0) or 0),
            "carbs": float(nutriments.get('carbohydrates_100g', 0) or 0),
            "fat": float(nutriments.get('fat_100g', 0) or 0)
        }
        
    except Exception as e:
        print(f"Error fetching OpenFoodFacts data: {e}")
        return None

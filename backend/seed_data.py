from core.database import SessionLocal
from models.food import Food

def seed_foods():
    db = SessionLocal()
    try:
        # Helper to create food dict
        def f(name, cal, p, c, f):
            return {"name": name, "calories": cal, "protein": p, "carbs": c, "fat": f}

        foods_data = [
            # --- FRUITS (Fresh, 100g) ---
            f("Apple", 52, 0.3, 14, 0.2), f("Banana", 89, 1.1, 23, 0.3), f("Orange", 47, 0.9, 12, 0.1),
            f("Strawberry", 32, 0.7, 7.7, 0.3), f("Grapes", 69, 0.7, 18, 0.2), f("Watermelon", 30, 0.6, 8, 0.2),
            f("Blueberries", 57, 0.7, 14, 0.3), f("Mango", 60, 0.8, 15, 0.4), f("Peach", 39, 0.9, 10, 0.3),
            f("Pineapple", 50, 0.5, 13, 0.1), f("Kiwi", 61, 1.1, 15, 0.5), f("Pear", 57, 0.4, 15, 0.1),
            f("Cherry", 50, 1.0, 12, 0.3), f("Papaya", 43, 0.5, 11, 0.3), f("Plum", 46, 0.7, 11, 0.3),
            f("Raspberries", 53, 1.2, 12, 0.7), f("Blackberries", 43, 1.4, 10, 0.5), f("Cantaloupe", 34, 0.8, 8, 0.2),
            f("Honeydew Melon", 36, 0.5, 9, 0.1), f("Avocado", 160, 2, 9, 15), f("Lemon", 29, 1.1, 9, 0.3),
            f("Lime", 30, 0.7, 11, 0.2), f("Grapefruit", 42, 0.8, 11, 0.1), f("Pomegranate", 83, 1.7, 19, 1.2),
            f("Apricot", 48, 1.4, 11, 0.4), f("Fig (Fresh)", 74, 0.8, 19, 0.3), f("Guava", 68, 2.6, 14, 1),
            f("Lychee", 66, 0.8, 17, 0.4), f("Passion Fruit", 97, 2.2, 23, 0.7), f("Persimmon", 81, 0.5, 18, 0.2),
            
            # --- VEGETABLES (Raw/Cooked, 100g) ---
            f("Spinach", 23, 2.9, 3.6, 0.4), f("Broccoli", 34, 2.8, 7, 0.4), f("Carrot", 41, 0.9, 10, 0.2),
            f("Cucumber", 16, 0.7, 4, 0.1), f("Tomato", 18, 0.9, 3.9, 0.2), f("Bell Pepper (Red)", 31, 1, 6, 0.3),
            f("Onion", 40, 1.1, 9, 0.1), f("Potato (Boiled)", 87, 1.9, 20, 0.1), f("Sweet Potato", 86, 1.6, 20, 0.1),
            f("Cauliflower", 25, 1.9, 5, 0.3), f("Cabbage", 25, 1.3, 6, 0.1), f("Lettuce (Iceberg)", 14, 0.9, 3, 0.1),
            f("Kale", 49, 4.3, 9, 0.9), f("Mushroom", 22, 3.1, 3.3, 0.3), f("Zucchini", 17, 1.2, 3, 0.3),
            f("Asparagus", 20, 2.2, 4, 0.1), f("Green Beans", 31, 1.8, 7, 0.2), f("Peas (Green)", 81, 5, 14, 0.4),
            f("Corn (Sweet)", 86, 3.2, 19, 1.2), f("Celery", 16, 0.7, 3, 0.2), f("Garlic", 149, 6.4, 33, 0.5),
            f("Ginger", 80, 1.8, 18, 0.8), f("Radish", 16, 0.7, 3.4, 0.1), f("Beetroot", 43, 1.6, 10, 0.2),
            f("Eggplant", 25, 1, 6, 0.2), f("Pumpkin", 26, 1, 7, 0.1), f("Okra (Lady Finger)", 33, 1.9, 7.5, 0.2),

            # --- PROTEINS (Meats, Seafood, Eggs, 100g) ---
            f("Chicken Breast (Grilled)", 165, 31, 0, 3.6), f("Chicken Thigh", 209, 26, 0, 11),
            f("Chicken Wings", 203, 30, 0, 8), f("Turkey Breast", 135, 30, 0, 1),
            f("Beef Steak (Sirloin)", 250, 26, 0, 15), f("Ground Beef (85%)", 250, 26, 0, 15),
            f("Pork Chop", 242, 27, 0, 14), f("Bacon", 541, 37, 1.4, 42), f("Sausage (Pork)", 300, 12, 2, 27),
            f("Lamb Chop", 294, 25, 0, 21), f("Salmon (Cooked)", 208, 20, 0, 13), f("Tuna (Canned)", 132, 28, 0, 1),
            f("Shrimp", 99, 24, 0.2, 0.3), f("Cod", 105, 23, 0, 1), f("Tilapia", 128, 26, 0, 3),
            f("Sardines", 208, 25, 0, 11), f("Trout", 190, 27, 0, 9), f("Crab", 97, 19, 0, 1.5),
            f("Egg (Boiled)", 155, 13, 1.1, 11), f("Egg White", 52, 11, 0.7, 0.2), f("Omelette", 154, 11, 0.6, 12),
            f("Tofu", 76, 8, 1.9, 4.8), f("Tempeh", 193, 19, 9, 11), f("Seitan", 370, 75, 14, 2),
            
            # --- DAIRY & ALTERNATIVES (100g/100ml) ---
            f("Milk (Whole)", 61, 3.2, 4.8, 3.3), f("Milk (Skim)", 34, 3.4, 5, 0.1), f("Almond Milk", 15, 0.5, 0.6, 1.2),
            f("Soy Milk", 54, 3.3, 6, 1.8), f("Oat Milk", 50, 1, 9, 1), f("Yogurt (Plain)", 61, 3.5, 4.7, 3.3),
            f("Greek Yogurt", 59, 10, 3.6, 0.4), f("Cottage Cheese", 98, 11, 3.4, 4.3), f("Cheddar Cheese", 402, 25, 1.3, 33),
            f("Mozzarella Cheese", 280, 28, 3.1, 17), f("Parmesan Cheese", 431, 38, 4.1, 29), f("Butter", 717, 0.9, 0.1, 81),
            f("Cream Cheese", 342, 6, 4, 34), f("Heavy Cream", 340, 2.8, 2.7, 36), f("Ghee", 900, 0, 0, 100),

            # --- GRAINS, PASTA & LEGUMES (Cooked, 100g) ---
            f("Rice (White)", 130, 2.7, 28, 0.3), f("Rice (Brown)", 111, 2.6, 23, 0.9), f("Quinoa", 120, 4.4, 21, 1.9),
            f("Oats (Rolled)", 68, 2.4, 12, 1.4), f("Pasta (White)", 131, 5, 25, 1.1), f("Pasta (Whole Wheat)", 124, 5.3, 26, 0.6),
            f("Bread (White)", 265, 9, 49, 3.2), f("Bread (Whole Wheat)", 247, 13, 41, 3.4), f("Sourdough Bread", 289, 11, 55, 3),
            f("Bagel", 250, 10, 49, 1.5), f("Tortilla (Corn)", 218, 6, 45, 2.9), f("Tortilla (Flour)", 299, 8, 49, 7.7),
            f("Lentils", 116, 9, 20, 0.4), f("Chickpeas", 164, 9, 27, 2.6), f("Black Beans", 132, 9, 24, 0.5),
            f("Kidney Beans", 127, 9, 23, 0.5), f("Edamame", 121, 11, 10, 5),

            # --- NUTS & SEEDS (100g) ---
            f("Almonds", 579, 21, 22, 50), f("Walnuts", 654, 15, 14, 65), f("Peanuts", 567, 26, 16, 49),
            f("Cashews", 553, 18, 30, 44), f("Pistachios", 562, 20, 28, 45), f("Chia Seeds", 486, 17, 42, 31),
            f("Flax Seeds", 534, 18, 29, 42), f("Sunflower Seeds", 584, 21, 20, 51), f("Pumpkin Seeds", 559, 30, 10, 49),
            f("Peanut Butter", 588, 25, 20, 50),

            # --- INDIAN CUISINE (100g) ---
            f("Chicken Tikka Masala", 150, 10, 8, 9), f("Butter Chicken", 240, 11, 10, 17), f("Tandoori Chicken", 200, 26, 4, 9),
            f("Chicken Curry", 160, 15, 6, 10), f("Lamb Curry (Rogan Josh)", 210, 18, 5, 14), f("Fish Curry", 140, 16, 4, 8),
            f("Egg Curry", 130, 9, 3, 9), f("Paneer Butter Masala", 280, 10, 12, 22), f("Palak Paneer", 180, 8.6, 6, 14),
            f("Matar Paneer", 190, 8, 12, 12), f("Kadai Paneer", 230, 11, 8, 18), f("Shahi Paneer", 300, 11, 15, 25),
            f("Dal Makhani", 180, 6, 17, 10), f("Dal Tadka", 116, 6, 15, 4), f("Chana Masala", 165, 8, 27, 4),
            f("Rajma", 140, 7, 22, 3), f("Aloo Gobi", 100, 3, 12, 5), f("Bhindi Masala", 110, 4, 8, 8),
            f("Baingan Bharta", 95, 2, 9, 6), f("Malai Kofta", 270, 7, 20, 18),
            f("Biryani (Chicken)", 180, 8, 25, 6), f("Biryani (Mutton)", 220, 10, 24, 10), f("Biryani (Veg)", 160, 4, 26, 5),
            f("Pulao", 140, 3, 28, 2), f("Jeera Rice", 150, 3, 30, 3), f("Khichdi", 120, 4, 18, 3),
            f("Chapati/Roti", 297, 8, 46, 7), f("Naan (Plain)", 310, 9, 50, 6), f("Naan (Butter)", 340, 9, 50, 12),
            f("Naan (Garlic)", 330, 9, 51, 8), f("Paratha (Plain)", 340, 8, 52, 12), f("Aloo Paratha", 280, 6, 40, 10),
            f("Puri", 480, 7, 48, 28), f("Bhatura", 300, 8, 50, 9),
            f("Idli", 130, 6, 25, 0.5), f("Dosa (Plain)", 168, 3.9, 29, 3.7), f("Masala Dosa", 200, 4, 32, 6),
            f("Uttapam", 180, 4, 30, 5), f("Sambar", 85, 4, 12, 1), f("Vada (Medhu)", 290, 10, 25, 18),
            f("Upma", 150, 4, 25, 5), f("Poha", 170, 3, 34, 4), f("Sabudana Khichdi", 250, 1, 40, 12),
            f("Samosa", 262, 3.5, 24, 17), f("Pakora (Veg)", 280, 5, 25, 18), f("Pav Bhaji", 160, 4, 22, 6),
            f("Vada Pav", 250, 6, 40, 10), f("Dhokla", 160, 6, 24, 6), f("Pani Puri", 180, 3, 35, 6),
            f("Gulab Jamun", 315, 3, 40, 12), f("Rasgulla", 186, 2, 43, 1), f("Jalebi", 360, 1, 60, 11),
            f("Kheer", 160, 4, 22, 6), f("Halwa (Gajar)", 250, 2, 35, 12), f("Ladoo (Besan)", 450, 8, 55, 24),
            
            # --- AMERICAN/WESTERN (100g) ---
            f("Hamburger", 250, 12, 31, 9), f("Cheeseburger", 300, 15, 30, 15), f("Bacon Cheeseburger", 340, 16, 29, 18),
            f("Pizza (Cheese)", 266, 11, 33, 10), f("Pizza (Pepperoni)", 290, 11, 31, 13), f("Pizza (Veggie)", 240, 9, 32, 9),
            f("Hot Dog", 290, 10, 24, 17), f("French Fries", 312, 3.4, 41, 15), f("Onion Rings", 400, 4, 43, 24),
            f("Chicken Nuggets", 296, 15, 16, 19), f("Fried Chicken", 246, 19, 11, 12), f("Buffalo Wings", 270, 18, 3, 20),
            f("Macaroni and Cheese", 164, 7, 19, 6), f("Spaghetti Bolognese", 150, 9, 18, 5), f("Lasagna", 160, 10, 15, 8),
            f("Grilled Cheese Sandwich", 350, 12, 33, 20), f("BLT Sandwich", 300, 12, 28, 16), f("Club Sandwich", 270, 15, 25, 12),
            f("Caesar Salad", 44, 3, 4, 2), f("Cobb Salad", 120, 12, 3, 8), f("Coleslaw", 150, 1, 12, 11),
            f("Pancake", 227, 6, 28, 10), f("Waffle", 291, 7, 33, 14), f("French Toast", 240, 8, 28, 11),
            f("Omelette (Cheese)", 220, 14, 2, 18), f("Scrambled Eggs", 160, 11, 2, 11), f("Hash Browns", 270, 3, 30, 15),
            f("Bagel with Cream Cheese", 300, 8, 40, 13), f("Donut", 452, 5, 51, 25), f("Muffin (Blueberry)", 370, 5, 54, 15),
            f("Croissant", 406, 8, 46, 21), f("Cinnamon Roll", 380, 5, 55, 16), f("Apple Pie", 237, 2, 34, 11),
            f("Cheesecake", 321, 5, 25, 22), f("Brownie", 466, 6, 65, 23), f("Chocolate Chip Cookie", 480, 5, 65, 24),
            f("Ice Cream (Vanilla)", 207, 3.5, 24, 11), f("Milkshake (Chocolate)", 140, 4, 20, 5),
            
            # --- BEVERAGES (100ml) ---
            f("Coffee (Black)", 1, 0.1, 0, 0), f("Coffee (Latte)", 40, 3, 4, 1.5), f("Tea (Black)", 1, 0, 0, 0),
            f("Tea (with Milk/Sugar)", 45, 1, 8, 1), f("Orange Juice", 45, 0.7, 10, 0.2), f("Apple Juice", 46, 0.1, 11, 0.1),
            f("Soda (Cola)", 40, 0, 10, 0), f("Beer", 43, 0.5, 3.5, 0), f("Wine (Red)", 85, 0.1, 2.6, 0),
            f("Coconut Water", 19, 0.7, 3.7, 0.2), f("Smoothie (Fruit)", 60, 1, 13, 0.5),
        ]

        for food_item in foods_data:
            exists = db.query(Food).filter(Food.name == food_item["name"]).first()
            if not exists:
                db.add(Food(**food_item))
                print(f"Added {food_item['name']}")
        
        db.commit()
        print("Food database updated.")
    except Exception as e:
        print(f"Error seeding foods: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_foods()

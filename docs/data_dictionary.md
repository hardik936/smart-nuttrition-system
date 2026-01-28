# Smart Nutrition System - Data Dictionary

## 1. User Table (`users`)
Stores user account information, profile details, and gamification stats.

| Column Name | Data Type | Key | Nullable | Description |
| :--- | :--- | :---: | :---: | :--- |
| `id` | Integer | PK | No | Unique identifier for the user. |
| `email` | String | Unique | No | User's email address. |
| `hashed_password` | String | | No | Securely hashed password. |
| `is_active` | Boolean | | No | Account status (default: True). |
| `age` | Integer | | Yes | User's age. |
| `weight` | Integer | | Yes | Weight in kilograms (kg). |
| `height` | Integer | | Yes | Height in centimeters (cm). |
| `activity_level` | String | | Yes | Activity level (e.g., sedentary, active). |
| `goal` | String | | Yes | Fitness goal (e.g., lose_weight). |
| `target_calories` | Integer | | No | Daily calorie target (default: 2000). |
| `streak_count` | Integer | | No | Current streak of logging meals. |
| `last_logged_date` | Date | | Yes | The last date a meal was logged. |

## 2. Food Table (`foods`)
Stores nutritional information for available food items.

| Column Name | Data Type | Key | Nullable | Description |
| :--- | :--- | :---: | :---: | :--- |
| `id` | Integer | PK | No | Unique identifier for the food item. |
| `name` | String | | No | Name of the food. |
| `calories` | Float | | No | Calories per 100g (or serving). |
| `protein` | Float | | No | Protein content in grams. |
| `carbs` | Float | | No | Carbohydrate content in grams. |
| `fat` | Float | | No | Fat content in grams. |

## 3. MealLog Table (`meal_logs`)
Records of meals consumed by users.

| Column Name | Data Type | Key | Nullable | Description |
| :--- | :--- | :---: | :---: | :--- |
| `id` | Integer | PK | No | Unique identifier for the log entry. |
| `user_id` | Integer | FK | No | ID of the user who logged the meal. |
| `food_id` | Integer | FK | No | ID of the food item consumed. |
| `quantity` | Float | | No | Quantity consumed (grams/servings). |
| `timestamp` | DateTime | | No | Date and time when the meal was logged. |

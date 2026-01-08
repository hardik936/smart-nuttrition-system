import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sqlalchemy.orm import Session
from models.food import Food

class NutritionRecommender:
    def __init__(self):
        self.model = NearestNeighbors(metric='cosine', algorithm='brute')
        self.df = None
        self.is_trained = False

    def train(self, db: Session):
        """Train the model with data from the database."""
        foods = db.query(Food).all()
        if not foods:
            print("No foods found in database. Skipping training.")
            return

        # Convert to DataFrame
        data = [
            {
                "id": f.id,
                "calories": f.calories,
                "protein": f.protein,
                "carbs": f.carbs,
                "fat": f.fat
            }
            for f in foods
        ]
        self.df = pd.DataFrame(data)
        self.df.set_index("id", inplace=True)

        # Select features
        features = ['calories', 'protein', 'carbs', 'fat']
        X = self.df[features].fillna(0)

        # Fit model
        self.model.fit(X)
        self.is_trained = True
        print(f"NutritionRecommender trained on {len(self.df)} items.")

    def get_recommendations(self, food_id: int, top_k: int = 5):
        """Get similar food IDs based on the given food_id."""
        if not self.is_trained or self.df is None:
            return []

        if food_id not in self.df.index:
            return []

        # Find features for the given food
        features = ['calories', 'protein', 'carbs', 'fat']
        query_vector = self.df.loc[food_id, features].values.reshape(1, -1)

        # Find neighbors
        # n_neighbors=top_k+1 because the item itself is included
        distances, indices = self.model.kneighbors(query_vector, n_neighbors=top_k+1)

        # Get food IDs (index of the DataFrame)
        # Skip the first one because it's the item itself
        neighbor_indices = indices.flatten()[1:]
        
        # Map back to food IDs using the dataframe's index
        # iloc is used to access by position, but indices returned by kneighbors are positions in X, 
        # which match positions in self.df if we didn't shuffle.
        # X is self.df[features], so indices match.
        food_ids = self.df.iloc[neighbor_indices].index.tolist()
        
        return food_ids

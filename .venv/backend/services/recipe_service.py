from models.recipe_model import RecipeModel
from config import db

class RecipeService:
    def __init__(self):
        self.collection = db["recipes"]

    def create_recipe(self, recipe_data: dict):
        result = self.collection.insert_one(recipe_data)
        return str(result.inserted_id)

    def get_all_recipes(self):
        recipes = list(self.collection.find())
        for recipe in recipes:
            recipe["_id"] = str(recipe["_id"])
        return recipes
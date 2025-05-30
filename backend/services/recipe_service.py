from backend.models.recipe_model import RecipeModel
from backend.config import db
from bson import ObjectId

class RecipeService:
    def __init__(self):
        self.collection = db["recipes"]

    def create_recipe(self, recipe_data: dict):
        result = self.collection.insert_one(recipe_data)
        return str(result.inserted_id)

    def get_recipe(self, recipe_id: str):
        if not ObjectId.is_valid(recipe_id):
            return None
        recipe = self.collection.find_one({"_id": ObjectId(recipe_id)})
        if recipe:
            recipe["_id"] = str(recipe["_id"])  # ✅ převod na string
        return recipe

    def get_all_recipes(self):
        recipes = list(self.collection.find())
        for recipe in recipes:
            recipe["_id"] = str(recipe["_id"])
        return recipes

    def delete_recipe(self, recipe_id: str):
        result = self.collection.delete_one({"_id": ObjectId(recipe_id)})
        return result.deleted_count > 0  #True/False

    def update_recipe(self, recipe_id: str, updated_data: dict):
        result = self.collection.update_one(
            {"_id": ObjectId(recipe_id)},
            {"$set": updated_data}
        )
        return result.modified_count > 0 #True/False

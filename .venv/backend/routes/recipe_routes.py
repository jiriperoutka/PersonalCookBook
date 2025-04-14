from fastapi import APIRouter
from models.recipe_model import RecipeModel
from services.recipe_service import RecipeService

router = APIRouter()
recipe_service = RecipeService()

@router.post("/recipes")
def create_recipe(recipe: RecipeModel):
    recipe_dict = recipe.dict()
    new_id = recipe_service.create_recipe(recipe_dict)
    return {"id": new_id}

@router.get("/recipes")
def get_recipes():
    return recipe_service.get_all_recipes()
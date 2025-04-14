from fastapi import APIRouter
from models.recipe_model import RecipeModel
from services.recipe_service import RecipeService
from services.ai_service import generate_ai_tip
from bson import ObjectId

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

@router.delete("/recipe/{id}")
def delete_recipe(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid recipe ID")

    deleted = recipe_service_delete_recipe(id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return {"status": "deleted"}

@router.put("/recipe/{id}")
def update_recipe(id: str, updated_recipe: dict):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid recipe ID")

    updated = recipe_service.update_recipe(id, updated_recipe)
    if not updated:
        raise HTTPException(status_code=404, detail="Recipe not found")

    return {"status": "updated"}

@router.get("/recipes/{id}/ai-tip")
def get_ai_tip(id: str):
    recipe = recipe_service.get_recipe(id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    return {"tip": generate_ai_tip(recipe)}
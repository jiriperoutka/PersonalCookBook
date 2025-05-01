from fastapi import APIRouter, File, UploadFile, HTTPException, Form
from backend.models.recipe_model import RecipeModel
from backend.services.recipe_service import RecipeService
from backend.services.ai_service import generate_ai_tip
from bson import ObjectId
import base64
import json

router = APIRouter()
recipe_service = RecipeService()

@router.post("/recipes")
async def create_recipe(
    recipe: str = Form(...),
    image: UploadFile = File(None)
):
    try:
        recipe_data = json.loads(recipe)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid recipe JSON")

    if image:
        content = await image.read()
        encoded_image = base64.b64encode(content).decode("utf-8")
        recipe_data["image_data"] = encoded_image

    new_id = recipe_service.create_recipe(recipe_data)
    return {"id": new_id}

@router.get("/recipes")
def get_recipes():
    return recipe_service.get_all_recipes()

@router.get("/recipes/{id}")
def get_recipe(id: str):
    recipe = recipe_service.get_recipe(id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe

@router.delete("/recipe/{id}")
def delete_recipe(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid recipe ID")

    deleted = recipe_service.delete_recipe(id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return {"status": "deleted"}

@router.put("/recipes/{id}")
async def update_recipe(
    id: str,
    recipe: str = Form(...),
    image: UploadFile = File(None)
):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid recipe ID")

    try:
        recipe_data = json.loads(recipe)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid recipe JSON")

    if image:
        content = await image.read()
        encoded_image = base64.b64encode(content).decode("utf-8")
        recipe_data["image_data"] = encoded_image

    updated = recipe_service.update_recipe(id, recipe_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Recipe not found")

    return {"status": "updated"}

@router.get("/recipes/{id}/ai-tip")
def get_ai_tip(id: str):
    recipe = recipe_service.get_recipe(id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    return {"tip": generate_ai_tip(recipe)}
from fastapi import FastAPI
from config import db

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello from Kucharka!"}

@app.get("/recipes")
async def get_recipes():
    recipes = await db["recipes"].find().to_list(100)
    return recipes

#https://fastapi.tiangolo.com/tutorial/
from fastapi import FastAPI
from config import db
from routes import recipe_routes


app = FastAPI()
app.include_router(recipe_routes.router)

@app.get("/")
async def root():
    return {"message": "Hello from Kucharka!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
from fastapi import FastAPI
from app.api.recipe_routes import router as recipe_router
app = FastAPI()

app.include_router(recipe_router)


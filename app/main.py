from fastapi import FastAPI
from app.api.routers.recipe_routes import router as recipe_router
from app.data.database.database import Base, engine

app = FastAPI()

app.include_router(recipe_router)
Base.metadata.create_all(engine)


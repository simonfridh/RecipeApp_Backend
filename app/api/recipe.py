from fastapi import APIRouter
from pydantic import BaseModel

from app.domain.services.recipeservice import RecipeService

router = APIRouter(prefix="/recipe", tags=["recipe"])
recipe_service = RecipeService()

class OptimizeRequest(BaseModel):
    url: str

@router.get("/{recipe_id}")
async def root(recipe_id: str):
    return recipe_service.get_recipe(recipe_id)


@router.post("/optimize")
async def optimize_recipe(payload: OptimizeRequest):
    print(payload.url)
    return {
        "id": "1"
    }
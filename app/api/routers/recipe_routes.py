from fastapi import APIRouter, Depends, HTTPException

from app.api.schemas.optimize_request import OptimizeRequest
from app.dependencies import get_recipe_service
from app.domain.models.recipe import Recipe
from app.domain.services.recipe_service import RecipeService

router = APIRouter(prefix="/recipe", tags=["recipe"])

@router.get("/{recipe_id}")
async def get_recipe(
        recipe_id: str,
        recipe_service: RecipeService = Depends(get_recipe_service)
):
    return recipe_service.get_recipe(recipe_id)


@router.post("/optimize")
async def optimize_recipe(
        request: OptimizeRequest,
        recipe_service: RecipeService = Depends(get_recipe_service)
):
    print(request.url)
    return {
        "id": "1"
    }

@router.post("/test", response_model=Recipe)
async def optimize_recipe(
        request: OptimizeRequest,
        recipe_service: RecipeService = Depends(get_recipe_service)
):
    try:
        return recipe_service.optimize_recipe(request.url)
    except PermissionError as e:
        raise HTTPException(status_code=502, detail=str(e))

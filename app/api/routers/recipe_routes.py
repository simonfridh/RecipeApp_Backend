from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from app.api.schemas.optimize_request import OptimizeRequest
from app.api.schemas.optimize_response import OptimizeResponse
from app.dependencies import get_recipe_service
from app.domain.models.recipe import Recipe
from app.domain.services.recipe_service import RecipeService

router = APIRouter(prefix="/recipe", tags=["recipe"])

@router.get("/{uuid}")
async def get_recipe(
        uuid: UUID,
        recipe_service: RecipeService = Depends(get_recipe_service)
):
    recipe = recipe_service.get_recipe(uuid)
    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")

    return recipe


@router.post("/optimize", response_model = OptimizeResponse)
async def optimize_recipe(
        request: OptimizeRequest,
        recipe_service: RecipeService = Depends(get_recipe_service)
):
    try:
        recipe_uuid = recipe_service.optimize_recipe(request.url)
        return OptimizeResponse(uuid=recipe_uuid)
    except PermissionError as e:
        raise HTTPException(status_code=502, detail=str(e))
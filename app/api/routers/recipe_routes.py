from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from app.api.schemas.optimize_request import OptimizeRequest
from app.api.schemas.test_similarity_request import TestSimilarityRequest
from app.dependencies import get_recipe_service
from app.domain.dto.recipe_comparison_result import RecipeComparisonResult
from app.domain.dto.recipe_result import RecipeResult
from app.domain.services.recipe_service import RecipeService

router = APIRouter(prefix="/recipe", tags=["recipe"])

@router.get("/{uuid}", response_model=RecipeResult)
async def get_recipe(
        uuid: UUID,
        recipe_service: RecipeService = Depends(get_recipe_service)
):
    recipe = recipe_service.get_recipe(uuid)
    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe

@router.get("/{uuid}/comparison", response_model=RecipeComparisonResult)
async def get_recipe_comparison(
        uuid: UUID,
        recipe_service: RecipeService = Depends(get_recipe_service)
):
    recipe_comparison = recipe_service.get_recipe_comparison(uuid)
    if recipe_comparison is None:
        raise HTTPException(status_code=404, detail="Recipe comparison could not be retrieved")
    return recipe_comparison

@router.post("/optimize", response_model = UUID)
async def optimize_recipe(
        request: OptimizeRequest,
        recipe_service: RecipeService = Depends(get_recipe_service)
):
    try:
        recipe_uuid = recipe_service.optimize_recipe(request.url)
        return OptimizeResponse(uuid=recipe_uuid)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=502, detail=str(e))

@router.post("/testsimilarity", response_model=str)
async def test_similarity(
        request: TestSimilarityRequest,
        recipe_service: RecipeService = Depends(get_recipe_service)
):
    similarity = recipe_service.test_similarity(request.first_recipe_url, request.second_recipe_url)
    return f"{round(similarity * 100)}%"
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from app.api.schemas.url_request import UrlRequest
from app.api.schemas.test_similarity_request import TestSimilarityRequest
from app.api.schemas.uuid_response import UuidResponse
from app.dependencies import get_recipe_service, get_evaluation_service
from app.domain.dto.recipe_comparison_result import RecipeComparisonResult
from app.domain.dto.recipe_result import RecipeResult
from app.domain.services.evaluation_service import EvaluationService
from app.domain.services.recipe_service import RecipeService

router = APIRouter(prefix="/recipe", tags=["recipe"])

@router.get("/{uuid}", response_model=RecipeResult)
async def get_recipe(
        uuid: UUID,
        recipe_service: RecipeService = Depends(get_recipe_service)
):
    recipe_result = recipe_service.get_recipe(uuid)
    if recipe_result is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe_result

@router.get("/{uuid}/comparison", response_model=RecipeComparisonResult)
async def get_recipe_comparison(
        uuid: UUID,
        recipe_service: RecipeService = Depends(get_recipe_service)
):
    recipe_comparison = recipe_service.get_recipe_comparison(uuid)
    if recipe_comparison is None:
        raise HTTPException(status_code=404, detail="Recipe comparison could not be retrieved")
    return recipe_comparison

@router.post("/optimize", response_model = UuidResponse)
async def optimize_recipe(
        request: UrlRequest,
        recipe_service: RecipeService = Depends(get_recipe_service)
):
    try:
        recipe_uuid = recipe_service.optimize_recipe(request.url)
        return UuidResponse(uuid=str(recipe_uuid))
    except Exception as e:
        print(e)
        raise HTTPException(status_code=502, detail=str(e))

@router.post("/evaluation")
async def create_evaluation(
        request: UrlRequest,
        evaluation_service: EvaluationService = Depends(get_evaluation_service)
):
    result = evaluation_service.create_evaluation(request.url)
    if result is None: return "Evaluation could not be created"
    else: return result





# TODO TEST-ROUTES REMOVE LATER
@router.post("/testsimilarity", response_model=str)
async def test_similarity(
        request: TestSimilarityRequest,
        recipe_service: RecipeService = Depends(get_recipe_service)
):
    similarity = recipe_service.test_similarity(request.first_recipe_url, request.second_recipe_url)
    return f"{round(similarity * 100)}%"

@router.get("/{uuid}/testcalculation")
async def test_calculation(
        uuid: UUID,
        recipe_service: RecipeService = Depends(get_recipe_service)
):
    return recipe_service.test_calorie_calculation(uuid)
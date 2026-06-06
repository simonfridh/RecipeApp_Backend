from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks

from app.api.schemas.url_request import UrlRequest
from app.api.schemas.test_similarity_request import TestSimilarityRequest
from app.api.schemas.uuid_response import UuidResponse
from app.dependencies import get_recipe_service, get_evaluation_service
from app.api.schemas.recipe_comparison_response import RecipeComparisonResponse
from app.api.schemas.recipe_response import RecipeResponse
from app.domain.services.evaluation_service import EvaluationService
from app.domain.services.recipe_service import RecipeService

router = APIRouter(prefix="/recipe", tags=["recipe"])

@router.get("/{uuid}", response_model=RecipeResponse)
async def get_recipe(
        uuid: UUID,
        recipe_service: RecipeService = Depends(get_recipe_service)
):
    recipe, similarity = recipe_service.get_recipe(uuid)
    if recipe is None or similarity is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return RecipeResponse(
        generated_recipe=recipe,
        similarity=similarity
    )

@router.get("/{uuid}/comparison", response_model=RecipeComparisonResponse)
async def get_recipe_comparison(
        uuid: UUID,
        recipe_service: RecipeService = Depends(get_recipe_service)
):
    generated_recipe, original_recipe, similarity = recipe_service.get_recipe_comparison(uuid)
    if generated_recipe is None or original_recipe is None or similarity is None:
        raise HTTPException(status_code=404, detail="Recipe comparison could not be retrieved")
    return RecipeComparisonResponse(
        generated_recipe=generated_recipe,
        original_recipe=original_recipe,
        similarity=similarity
    )

@router.post("/optimize", response_model = UuidResponse)
async def optimize_recipe(
        request: UrlRequest,
        background_tasks: BackgroundTasks,
        recipe_service: RecipeService = Depends(get_recipe_service),
        evaluation_service: EvaluationService = Depends(get_evaluation_service)
):
    try:
        recipe_uuid = recipe_service.optimize_recipe(request.url)
        background_tasks.add_task(
            evaluation_service.create_evaluation,recipe_uuid
        )

        return UuidResponse(uuid=str(recipe_uuid))
    except Exception as e:
        print(e)
        raise HTTPException(status_code=502, detail=str(e))

@router.get("/{uuid}/evaluation")
async def create_evaluation(
        uuid: UUID,
        evaluation_service: EvaluationService = Depends(get_evaluation_service)
):
    result = evaluation_service.get_evaluation(uuid)
    if result is None: raise HTTPException(status_code=502, detail="Evaluation could not be created")
    return result

@router.post("/testsimilarity", response_model=str)
async def test_similarity(
        request: TestSimilarityRequest,
        recipe_service: RecipeService = Depends(get_recipe_service)
):
    similarity = recipe_service.test_similarity(request.first_recipe_url, request.second_recipe_url)
    return f"{round(similarity * 100)}%"
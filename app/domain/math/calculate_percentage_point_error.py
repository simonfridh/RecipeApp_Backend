from app.domain.models.evaluation.nutrition_percent_changes import NutritionPercentChanges


def calculate_percentage_point_error(recipe: NutritionPercentChanges, calculated: NutritionPercentChanges) -> NutritionPercentChanges:
    return NutritionPercentChanges(
        calories=_calculate_error(recipe.calories, calculated.calories),
        carbohydrates = _calculate_error(recipe.carbohydrates, calculated.carbohydrates),
        cholesterol = _calculate_error(recipe.cholesterol, calculated.cholesterol),
        fat = _calculate_error(recipe.fat, calculated.fat),
        fiber = _calculate_error(recipe.fiber, calculated.fiber),
        protein = _calculate_error(recipe.protein, calculated.protein),
        saturated_fat = _calculate_error(recipe.saturated_fat, calculated.saturated_fat),
        sodium = _calculate_error(recipe.sodium, calculated.sodium),
        sugar = _calculate_error(recipe.sugar, calculated.sugar),
        trans_fat = _calculate_error(recipe.trans_fat, calculated.trans_fat),
        unsaturated_fat = _calculate_error(recipe.unsaturated_fat, calculated.unsaturated_fat)
    )

def _calculate_error(recipe: float | None, calculated: float | None) -> float | None:
    if recipe is None or calculated is None: return None
    return abs(recipe - calculated)
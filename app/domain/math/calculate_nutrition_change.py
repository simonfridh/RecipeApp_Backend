import re

from app.domain.models.evaluation.nutrition_percent_changes import NutritionPercentChanges
from app.domain.models.recipe.nutrition import Nutrition


def calculate_nutrition_change(new: Nutrition, old: Nutrition) -> NutritionPercentChanges:
    return NutritionPercentChanges(
        calories=_calculate_percentage(new.calories, old.calories),
        carbohydrates = _calculate_percentage(new.carbohydrates, old.carbohydrates),
        cholesterol = _calculate_percentage(new.cholesterol, old.cholesterol),
        fat = _calculate_percentage(new.fat, old.fat),
        fiber = _calculate_percentage(new.fiber, old.fiber),
        protein = _calculate_percentage(new.protein, old.protein),
        saturated_fat = _calculate_percentage(new.saturated_fat, old.saturated_fat),
        sodium = _calculate_percentage(new.sodium, old.sodium),
        sugar = _calculate_percentage(new.sugar, old.sugar),
        trans_fat = _calculate_percentage(new.trans_fat, old.trans_fat),
        unsaturated_fat = _calculate_percentage(new.unsaturated_fat, old.unsaturated_fat)
    )

def _calculate_percentage(new: str|None, old: str|None) -> float|None:
    new_float = _parse_number(new)
    old_float = _parse_number(old)
    if new_float is None or old_float is None: return None
    if old_float == 0: return None
    return round(((new_float - old_float) / old_float * 100), 2)

def _parse_number(value: str | None) -> float | None:
    if value is None: return None
    match = re.search(r"\d+(\.\d+)?", value)
    if match is None: return None
    return float(match.group())
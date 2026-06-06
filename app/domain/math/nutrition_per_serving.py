import re
from app.domain.models.recipe.nutrition import Nutrition


def nutrition_per_serving(nutrition_list: list[Nutrition], recipe_yield: str | None) -> Nutrition:
        if recipe_yield is None:
            servings = 1
        else:
            servings = _parse_number(recipe_yield) or 1

        total_calories: float = 0
        total_carbohydrates: float = 0
        total_cholesterol: float = 0
        total_fat: float = 0
        total_fiber: float = 0
        total_protein: float = 0
        total_saturated_fat: float = 0
        total_sodium: float = 0
        total_sugar: float = 0
        total_trans_fat: float = 0
        total_unsaturated_fat: float = 0

        for nutrition in nutrition_list:
            total_calories += _parse_number(nutrition.calories)
            total_carbohydrates += _parse_number(nutrition.carbohydrates)
            total_cholesterol += _parse_number(nutrition.cholesterol)
            total_fat += _parse_number(nutrition.fat)
            total_fiber += _parse_number(nutrition.fiber)
            total_protein += _parse_number(nutrition.protein)
            total_saturated_fat += _parse_number(nutrition.saturated_fat)
            total_sodium += _parse_number(nutrition.sodium)
            total_sugar += _parse_number(nutrition.sugar)
            total_trans_fat += _parse_number(nutrition.trans_fat)
            total_unsaturated_fat += _parse_number(nutrition.unsaturated_fat)

        return Nutrition(
            calories=_format_nutrient(total_calories / servings, "kcal"),
            carbohydrates=_format_nutrient(total_carbohydrates / servings, "g"),
            cholesterol=_format_nutrient(total_cholesterol / servings, "mg"),
            fat=_format_nutrient(total_fat / servings, "g"),
            fiber=_format_nutrient(total_fiber / servings, "g"),
            protein=_format_nutrient(total_protein / servings, "g"),
            saturated_fat=_format_nutrient(total_saturated_fat / servings, "g"),
            sodium=_format_nutrient(total_sodium / servings, "mg"),
            sugar=_format_nutrient(total_sugar / servings, "g"),
            trans_fat=_format_nutrient(total_trans_fat / servings, "g"),
            unsaturated_fat=_format_nutrient(total_unsaturated_fat / servings, "g")
        )


def _parse_number(value:str | None) -> float:
    if value is None: return 0
    match = re.search(r"\d+(\.\d+)?", value)
    if match is None: return 0
    return float(match.group())

def _format_nutrient(value: float, unit: str) -> str | None:
    if value == 0: return None
    else: return f"{round(value, 1)} {unit}"
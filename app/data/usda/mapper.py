import re
from typing import Any

from app.domain.models.evaluation.ingredient_query_info import IngredientQueryInfo
from app.domain.models.recipe.ingredient import Ingredient
from app.domain.models.recipe.nutrition import Nutrition

def usda_mapper(data: dict[str, Any], ingredient: Ingredient) -> tuple[Nutrition, IngredientQueryInfo]:
    if ingredient.name is None: raise ValueError("Ingredient name is required")
    if ingredient.grams_estimate is None: raise ValueError("grams_estimate is required")
    ingredient_words = re.findall(r"[a-z]+", ingredient.name.lower())

    foods = data.get("foods")
    if isinstance(foods, list):
        for food in foods:
            description = food.get("description")
            if not all(word in description.lower() for word in ingredient_words): continue
            try:
                nutrition = _extract_nutrition(food, ingredient.grams_estimate)
                if nutrition.calories is not None:
                    return nutrition, IngredientQueryInfo(search_query=ingredient.name, result_description=description)
            except ValueError:
                continue
    raise ValueError("Nutrition could not be found")


def _extract_nutrition(ingredient_data: dict[str, Any], grams_estimate: float) -> Nutrition:
    nutrients = ingredient_data.get("foodNutrients")
    if not isinstance(nutrients, list): raise ValueError("Nutrient list could not be found")

    nutrient_map = {
        "208": "calories",
        "203": "protein",
        "204": "fat",
        "205": "carbohydrates",
        "269": "sugar",
        "291": "fiber",
        "307": "sodium",
        "601": "cholesterol",
        "605": "trans_fat",
        "606": "saturated_fat",
        "645": "monounsaturated_fat",
        "646": "polyunsaturated_fat",
    }
    values: dict[str, float] = {}

    for item in nutrients:
        nutrient_number = item.get("nutrientNumber")
        value = item.get("value")

        mapped_name = nutrient_map.get(nutrient_number)
        if mapped_name is not None and isinstance(value, (int, float)):
            values[mapped_name] = float(value) * (grams_estimate / 100)

    #unsaturated fat is split into two categories
    unsaturated_fat: float | None = None
    if values.get("monounsaturated_fat") is not None or values.get("polyunsaturated_fat") is not None:
        unsaturated_fat = values.get("monounsaturated_fat", 0) + values.get("polyunsaturated_fat",0)

    return Nutrition(
        calories = _format_nutrient(values.get("calories"), "kcal"),
        carbohydrates = _format_nutrient(values.get("carbohydrates"), "g"),
        cholesterol= _format_nutrient(values.get("cholesterol"), "mg"),
        fat = _format_nutrient(values.get("fat"), "g"),
        fiber = _format_nutrient(values.get("fiber"), "g"),
        protein = _format_nutrient(values.get("protein"), "g"),
        saturated_fat= _format_nutrient(values.get("saturated_fat"), "g"),
        sodium= _format_nutrient(values.get("sodium"), "mg"),
        sugar = _format_nutrient(values.get("sugar"), "g"),
        trans_fat= _format_nutrient(values.get("trans_fat"), "g"),
        unsaturated_fat=_format_nutrient(unsaturated_fat, "g")
    )

def _format_nutrient(value: float | None, unit: str) -> str | None:
    if value is None: return None
    else: return f"{round(value, 1)} {unit}"
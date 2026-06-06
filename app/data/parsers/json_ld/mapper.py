from typing import Any

from app.domain.models.recipe.ingredient import Ingredient
from app.domain.models.recipe.instruction import Instruction
from app.domain.models.recipe.nutrition import Nutrition
from app.domain.models.recipe.recipe import Recipe

#this code is a bit messy since some websites use lists for fields where there should only be one string
def schema_org_recipe_mapper(json_ld: dict[str, Any], url: str) -> Recipe:
    name = first(json_ld.get("name"))
    if not isinstance(name, str):
        raise ValueError("name not found")

    url = url
    cooking_method = first(json_ld.get("cookingMethod"))
    recipe_category = first(json_ld.get("recipeCategory"))
    recipe_cuisine = first(json_ld.get("recipeCuisine"))
    recipe_yield = first(json_ld.get("recipeYield"))

    total_time = first(json_ld.get("totalTime"))
    if total_time is None: total_time = first(json_ld.get("cookTime"))

    ingredients_raw = json_ld.get("recipeIngredient", [])
    ingredients: list[Ingredient] = []
    for item in ingredients_raw:
        if isinstance(item, str):
            ingredients.append(Ingredient(raw_string=item))

        elif isinstance(item, dict):
            ingredient_name = first(item.get("name", None))
            ingredient_quantity = first(item.get("value", None))
            ingredient_unit = first(item.get("unitCode", None))

            raw_string = ""
            if ingredient_name is not None: raw_string += ingredient_name
            if ingredient_quantity is not None: raw_string += ingredient_quantity
            if ingredient_unit is not None: raw_string += ingredient_unit

            ingredients.append(
                Ingredient(
                    raw_string= raw_string,
                    name = ingredient_name if ingredient_name is not None else None,
                    quantity = ingredient_quantity if ingredient_quantity is not None else None,
                    unit = ingredient_unit if ingredient_unit is not None else None,
                )
            )

    instructions_raw = json_ld.get("recipeInstructions", [])
    instructions: list[Instruction] = []
    for i, item in enumerate(instructions_raw, start=1):
        if isinstance(item, str):
            instructions.append(
                Instruction(
                    step = i,
                    text = item,
                )
            )
        if isinstance(item, dict) and item.get("@type") == "HowToStep":
            instruction_text = first(item.get("text"))
            if isinstance(instruction_text, str):
                instructions.append(
                    Instruction(
                        step = i,
                        text = instruction_text,
                    )
                )

    nutrition_raw = first(json_ld.get("nutrition"))
    nutrition: Nutrition | None = None
    if isinstance(nutrition_raw, dict) and nutrition_raw.get("@type") == "NutritionInformation":
        nutrition = Nutrition(
            calories= first(nutrition_raw.get("calories")),
            carbohydrates= first(nutrition_raw.get("carbohydrateContent")),
            cholesterol= first(nutrition_raw.get("cholesterolContent")),
            fat= first(nutrition_raw.get("fatContent")),
            fiber= first(nutrition_raw.get("fiberContent")),
            protein= first(nutrition_raw.get("proteinContent")),
            saturated_fat= first(nutrition_raw.get("saturatedFatContent")),
            sodium= first(nutrition_raw.get("sodiumContent")),
            sugar= first(nutrition_raw.get("sugarContent")),
            trans_fat= first(nutrition_raw.get("tranFatContent")),
            unsaturated_fat= first(nutrition_raw.get("unsaturatedFatContent"))
        )
    return Recipe(
        name = name,
        url = url,
        total_time = total_time,
        cooking_method = cooking_method,
        recipe_category = recipe_category,
        recipe_cuisine = recipe_cuisine,
        recipe_yield = recipe_yield,
        ingredients = ingredients,
        instructions = instructions,
        nutrition = nutrition,
    )

#If the value is in a list, return the first value. If not in a list return the value
def first(value: Any) -> Any | None:
    if isinstance(value, list):
        if value: #is not empty
            return value[0]
        else: return None
    else: return value
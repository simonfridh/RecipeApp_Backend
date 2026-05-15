from typing import Any

from app.domain.models.ingredient import Ingredient
from app.domain.models.instruction import Instruction
from app.domain.models.nutrition import Nutrition
from app.domain.models.recipe import Recipe


def schema_org_recipe_mapper(json_ld: dict[str, Any]) -> Recipe:
    if json_ld.get("@type") != "Recipe":
        raise Exception("json ld")

    name = json_ld.get("name")
    if not isinstance(name, str):
        raise Exception("name not found")

    description = json_ld.get("description")
    url = json_ld.get("url")
    cooking_method = json_ld.get("cookingMethod")
    recipe_category = json_ld.get("recipeCategory")
    recipe_cuisine = json_ld.get("recipeCuisine")
    recipe_yield = json_ld.get("recipeYield")

    total_time = json_ld.get("totalTime")
    if total_time is None: total_time = json_ld.get("cookTime")

    ingredients_raw = json_ld.get("recipeIngredient", [])
    ingredients: list[Ingredient] = []
    for item in ingredients_raw:
        if isinstance(item, str):
            ingredients.append(Ingredient(raw_string=item))

        elif isinstance(item, dict):
            ingredient_name = item.get("name", None)
            ingredient_quantity = item.get("value", None)
            ingredient_unit = item.get("unitCode", None)

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
            instruction_text = item.get("text")
            if isinstance(instruction_text, str):
                instructions.append(
                    Instruction(
                        step = i,
                        text = instruction_text,
                    )
                )

    nutrition_raw = json_ld.get("nutrition", [])
    nutrition: Nutrition | None = None
    if isinstance(nutrition_raw, dict) and nutrition_raw.get("@type") == "NutritionInformation":
        nutrition = Nutrition(
            calories= nutrition_raw.get("calories"),
            carbohydrates= nutrition_raw.get("carbohydrateContent"),
            cholesterol= nutrition_raw.get("cholesterolContent"),
            fat= nutrition_raw.get("fatContent"),
            fiber= nutrition_raw.get("fiberContent"),
            protein= nutrition_raw.get("proteinContent"),
            saturated_fat= nutrition_raw.get("saturatedFatContent"),
            sodium= nutrition_raw.get("sodiumContent"),
            sugar= nutrition_raw.get("sugarContent"),
            trans_fat= nutrition_raw.get("tranFatContent"),
            unsaturated_fat= nutrition_raw.get("unsaturatedFatContent")
        )

    return Recipe(
        name = name,
        description = description,
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
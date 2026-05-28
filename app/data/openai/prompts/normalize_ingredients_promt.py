from textwrap import dedent
from openai.types.responses import EasyInputMessageParam

from app.data.openai.schemas.IngredientList import IngredientList


def normalize_ingredients_prompt(ingredients: IngredientList) -> list[EasyInputMessageParam]:
    return [
        {
            "role": "developer",
            "content": dedent(
                """
                Normalize this ingredient list for nutrition database lookup.

                Rules for "raw_string":
                    - Preserve "raw_string" exactly.

                Rules for "name":
                    - "name" must be optimized for USDA FoodData Central lookup accuracy.
                    - Translate to English.
                    - Use lowercase USDA-friendly search names, not display names.
                    - Prefer generic whole foods over prepared/branded foods.
                    - Remove units, counts, package words, shape words, prep words, and size words.
                    - Remove words like: clove, piece, slice, can, package, bunch, cup, tbsp, tsp, gram, ml, chopped, minced, diced, sliced, grated, large, small, medium, optional, divided.
                    
                    Food state rule: 
                    - For fresh whole produce, ALWAYS append ", raw". 
                    - For cooked ingredients, append ", cooked". 
                    - For canned ingredients, append ", canned". 
                    - For dried ingredients, append ", dry" or ", dried". 
                    - For crushed canned tomatoes, use "tomatoes, crushed, canned". 
                    - Do not add raw/cooked/canned/dried to oils, spices, condiments, dairy, or branded/processed foods.
                    
                    Produce naming rule:
                    - Use USDA-style plural names for simple produce:
                      onion -> onions, raw
                      tomato -> tomatoes, raw
                      potato -> potatoes, raw
                      carrot -> carrots, raw
                      mushroom -> mushrooms, raw
                      strawberry -> strawberries, raw
                    
                    Keep meaningful descriptors that affect nutrition/matching:
                    olive oil, coconut milk, chicken breast, ground beef, cream cheese,
                    greek yogurt, brown rice, black beans, peanut butter.
                    
                    name examples:
                    - "2 garlic cloves, minced" -> "garlic, raw"
                    - "1 large onion, diced" -> "onions, raw"
                    - "2 carrots, chopped" -> "carrots, raw"
                    - "400g canned tomatoes" -> "tomatoes, canned"
                    - "400g crushed canned tomatoes" -> "tomatoes, crushed, canned"
                    - "1 cup cooked rice" -> "rice, cooked"
                    - "2 chicken breasts" -> "chicken breast"
                    - "1 tbsp olive oil" -> "olive oil"
                    - "½ bunch fresh parsley" -> "parsley, raw"
                    - "1 can black beans, drained" -> "black beans, canned"

                Rules for "quantity":
                    - Keep existing "quantity" unless clearly wrong.
                    - If missing, extract it from "raw_string".
                    - Normalize number words and fractions to numeric values when possible.

                Rules for "unit":
                    - Keep existing "unit" unless clearly wrong.
                    - If missing, extract it from "raw_string".
                    - Standardize to common English units such as:
                      g, kg, ml, l, dl, tsp, tbsp, cup, clove, slice, can, bunch
                    - If the ingredient has no clear unit the field should be set to null.

                Rules for "grams_estimate":
                    - Estimate the total edible ingredient weight in grams.
                    - Use realistic cooking estimates.
                    - If highly uncertain, approximate the amount based on recipe context.
                """
            ).strip()
        },
        {
            "role": "user",
            "content": ingredients.model_dump_json(indent=2)
        }
    ]

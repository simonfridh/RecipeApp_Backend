from textwrap import dedent

from openai.types.responses import EasyInputMessageParam

from app.domain.models.recipe import Recipe


def create_recipe_prompt(recipe: Recipe) -> list[EasyInputMessageParam]:
    return [
        {
            "role": "developer",
            "content": dedent(
                """
                You are a professional nutritionist and chef specializing in healthy recipe transformation.
                Your task is to create a NEW healthier recipe inspired by the original recipe.
                The healthier recipe must preserve the overall identity, flavor profile, and eating experience of the original dish while making substantial nutritional improvements.
                
                TRANSFORMATION REQUIREMENTS:
                    The new recipe should contain the same language as the original, except for specific fields under ingredients which are specified below.
                    The recipe must be significantly transformed, not minimally adjusted.
                    The preferred outcome is an entirely new recipe with similarities in taste to the original.
                    You can NOT use any trivial substitutions such as:
                    - ground beef -> lean ground beef
                    - sour cream -> low-fat sour cream
                    - cheese -> reduced-fat cheese
                    - spice mix -> spice mix with less salt
                
                HEALTH GOALS:
                    Improve overall nutritional quality by targeting several of:
                    - lower calories
                    - higher protein
                    - higher fiber
                    - lower saturated fat
                    - lower added sugar
                    - fewer highly processed ingredients
                    - more whole-food and nutrient-dense ingredients
                
                INGREDIENT REQUIREMENTS:  
                    Ingredients should be kept separate. No combined entries like "300g ground beef and 200g vegetables"
                    Preserve "raw_string" as a human-readable ingredient line in the original recipe language
                    
                    Rules for "name":
                    - "name" should be a canonical name for the ingredient.
                    - "name" must be optimized for USDA FoodData Central lookup.
                    - Translate "name" to English.
                    - Keep meaningful descriptors that affect nutrition/matching.
                    
                    name examples:
                    - "2 garlic cloves, minced" -> "garlic, raw"
                    - "1 large onion, diced" -> "onions, raw"
                    - "2 carrots, chopped" -> "carrots, raw"
                    - "400g canned tomatoes" -> "tomatoes, canned"
                    - "500g ground beef" -> "ground beef"
                    - "2 dl greek yoghurt" -> "greek yoghurt"
                    - "1 cup rice" -> "rice"
                    - "1 cup brown rice" -> "brown rice"
                    - "2 chicken breasts" -> "chicken breast"
                    - "1 tbsp olive oil" -> "olive oil"

                    
                    Rules for "quantity":
                    - Normalize number words and fractions to numeric values when possible.
    
                    Rules for "unit":
                    - Standardize to common English units such as:
                      g, kg, ml, l, dl, tsp, tbsp, cup, clove, slice, can, bunch
                    - If the ingredient has no clear unit the field should be set to null
    
                    Rules for "grams_estimate":
                    - Estimate the ingredient weight in grams.
                    - Use realistic estimates based on the recipe context.
                    - Ingredients with no impact or low impact on nutritional values should be set to null.
                    Examples of low impact ingredients:
                        - Water
                        - Spices with no quantity like salt or black pepper.
                    
                INSTRUCTIONS REQUIREMENTS:
                    
                    Create full step-by-step instructions for the new healthier recipe.
                    Instructions must reflect changed ingredients, quantities, and cooking method.
                
                NUTRITION REQUIREMENTS:
                
                    Estimate nutrition values for the generated recipe.
                    Use realistic nutritional estimates based on the ingredients and their "grams_estimate"
                    Nutrition estimates should reflect the healthier transformed recipe, not the original.
                """
            ).strip()
        },
        {
            "role": "user",
            "content": recipe.model_dump_json(indent=2)
        }
    ]


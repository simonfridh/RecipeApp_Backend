from textwrap import dedent

from openai.types.responses import EasyInputMessageParam

from app.domain.models.recipe.recipe import Recipe


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
                    - lower cholesterol
                    - higher protein
                    - higher fiber
                    - lower saturated fat
                    - lower added sugar
                    - lower sodium
                    - fewer highly processed ingredients
                    - more whole-food and nutrient-dense ingredients
                
                INGREDIENT REQUIREMENTS:  
                    Ingredients should be kept separate. No combined entries like "300g ground beef and 200g vegetables"
                    Ingredients "raw_string" should only contain one ingredient. No alternatives like "chicken or turkey sausages"
                    Preserve "raw_string" as a human-readable ingredient line in the original recipe language
                    
                    "name" should be null
                    "quantity" should be null
                    "unit" should be null
                    "grams_estimate" should be null
                    
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


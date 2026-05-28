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
                
                The recipe must be significantly transformed, not minimally adjusted.
                Avoid trivial substitutions such as:
                - ground beef -> lean ground beef
                - sour cream -> low-fat sour cream
                - cheese -> reduced-fat cheese
                - white pasta -> whole wheat pasta
                - Tex-mex spice mix -> Tex-mex spice mix with less salt
                The healthier recipe should introduce meaningful ingredient changes.
                Prefer replacing high-calorie processed ingredients with:
                - vegetables
                - legumes
                - whole foods
                - lean proteins
                - high-fiber ingredients
                - healthier cooking techniques
                It is acceptable to redesign the dish while keeping it recognizably similar to the original.
                The complexity of the cooking instructions should be kept similar to the original recipe.
                The number of ingredients used should be kept similar to the original recipe.
                
                HEALTH GOALS:
                
                Improve overall nutritional quality by targeting several of:
                - lower calories
                - higher protein
                - higher fiber
                - lower saturated fat
                - lower added sugar
                - fewer highly processed ingredients
                - more whole-food and nutrient-dense ingredients
                
                RECIPE DESIGN REQUIREMENTS:
                
                Preserve similar flavor direction and texture satisfaction.
                Preserve recognizability of the original dish.
                Use realistic cooking methods and ingredient combinations.
                Aim for at least 30-50% meaningful ingredient change from the original recipe.
                
                INGREDIENT RULES:
                
                Preserve "raw_string" as a human-readable ingredient line in the original language.
                "name" must be English, lowercase, singular, and contain only the core ingredient.
                Keep ingredient naming consistent.
                Include "grams_estimate" for every ingredient.
                Estimate missing quantities realistically.
                
                NUTRITION REQUIREMENTS:
                
                Estimate nutrition values for the generated recipe.
                Use realistic nutritional estimates based on the final ingredients.
                Nutrition estimates should reflect the healthier transformed recipe, not the original.
                """
            ).strip()
        },
        {
            "role": "user",
            "content": recipe.model_dump_json(indent=2)
        }
    ]


from rapidfuzz import fuzz
from app.domain.models.recipe.ingredient import Ingredient

def calculate_ingredient_overlap(ingredients_a: list[Ingredient], ingredients_b: list[Ingredient]) -> float:
    a = _extract_ingredient_set(ingredients_a)
    b = _extract_ingredient_set(ingredients_b)

    matched = set()
    for ingredient_a in a:
        for ingredient_b in b:
            if ingredient_b in matched:
                continue

            if fuzz.token_sort_ratio(ingredient_a, ingredient_b) > 80:
                matched.add(ingredient_b)
                break

    intersection = len(matched)
    union = len(a) + len(b) - intersection

    if union == 0:
        return 1.0

    return intersection / union

def _extract_ingredient_set(ingredient_list: list[Ingredient]) -> set[str]:
    ingredient_set = set()
    for ingredient in ingredient_list:
        if ingredient.name is not None:
            shortened_name = ingredient.name.split(',')[0].strip().lower()
            ingredient_set.add(shortened_name)
    return ingredient_set
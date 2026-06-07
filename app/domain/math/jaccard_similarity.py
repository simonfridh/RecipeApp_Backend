from app.domain.models.recipe.ingredient import Ingredient

def jaccard_similarity(ingredients_a: list[Ingredient], ingredients_b: list[Ingredient]) -> float:
    a = set()
    for ingredient in ingredients_a:
        if ingredient.name is not None: a.add(ingredient.name)

    b = set()
    for ingredient in ingredients_b:
        if ingredient.name is not None: b.add(ingredient.name)

    union = len( a | b )            #Total number of unique ingredient names
    intersection = len( a & b )     #Number of overlapping ingredient names
    
    if union == 0:
        return 1.0

    return intersection / union

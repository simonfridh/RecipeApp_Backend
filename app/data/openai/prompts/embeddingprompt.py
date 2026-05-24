from app.domain.models.recipe import Recipe


def create_embedding_prompt(recipe: Recipe) -> str:
    ingredients = "\n".join(
        f"- {ingredient.raw_string}"
        for ingredient in recipe.ingredients
    )

    instructions = "\n".join(
        f"{step.step}. {step.text}"
        for step in recipe.instructions
    )

    #Only keeping name ingredients and instructions for embeddings
    embeddings_string = [
        f"Name: {recipe.name}",
        "Ingredients:",
        ingredients,
        "",
        "Instructions:",
        instructions,
    ]

    return "\n".join(embeddings_string)

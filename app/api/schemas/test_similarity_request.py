from pydantic import BaseModel

class TestSimilarityRequest(BaseModel):
    first_recipe_url: str
    second_recipe_url: str
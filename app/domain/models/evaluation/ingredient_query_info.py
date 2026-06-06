from pydantic import BaseModel


class IngredientQueryInfo(BaseModel):
    search_query: str
    result_description: str
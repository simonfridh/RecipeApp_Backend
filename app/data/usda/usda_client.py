from typing import Any

import requests


class UsdaClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "RecipeOptimizer/1.0",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept": "application/json",
        })

    def fetch(self, ingredient_name: str) -> dict[str, Any]:
        url = f"https://api.nal.usda.gov/fdc/v1/foods/search"
        params = {
            "api_key": self.api_key,
            "query": ingredient_name,
            "pageSize": 25,
        }

        response = self.session.get(url=url, params=params, timeout=10)
        response.raise_for_status() # throws exception if response contains any error codes

        data: dict[str, Any] = response.json()
        return data
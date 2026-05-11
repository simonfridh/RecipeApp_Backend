

class RecipeService:
    def get_recipe(self, recipe_id):
        if recipe_id == "1": return {
            "title": "hello world",
            "ingredients": [
                {
                    "name": "apple",
                    "amount": 1
                },
                {
                    "name": "orange",
                    "amount": 2
                }
            ],
            "instructions": [
                "cook food",
                "eat food",
                "???",
                "profit"
            ]
        }
        return {
            "title": "NYI",
            "ingredients": [],
            "instructions": [],
        }

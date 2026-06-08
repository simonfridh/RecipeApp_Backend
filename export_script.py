from pathlib import Path

import pandas as pd

from app.data.database.database import session_local, Base, engine
from app.data.database.tables.evaluation_db import EvaluationDb
from app.domain.models.evaluation.evaluation import Evaluation
from app.domain.models.evaluation.nutrition_search_info import NutritionSearchInfo
from app.domain.models.recipe.nutrition import Nutrition

def export():
    Base.metadata.create_all(bind=engine)
    db = session_local()
    try:
        evaldb_list = db.query(EvaluationDb).all()

        evaluation_rows = []
        nutrition_rows = []
        nutrients = list(Nutrition.model_fields.keys())  # Creates a list of all the fields in the Nutrition model
        for item in evaldb_list:
            evaluation = Evaluation.model_validate(item.evaluation)


            evaluation_rows.append({
                "uuid": item.uuid,
                "url": item.url,
                "cosine similarity": evaluation.cosine_similarity,
                "ingredient overlap": evaluation.ingredient_overlap,
                "original lookup failure (%)": _calculation_failure_rate(evaluation.original_search_info),
                "original failed ingredients": evaluation.original_search_info.failed_ingredients,
                "original skipped ingredients": evaluation.original_search_info.skipped_ingredients,
                "generated lookup failure (%)": _calculation_failure_rate(evaluation.generated_search_info),
                "generated failed ingredients": evaluation.generated_search_info.failed_ingredients,
                "generated skipped ingredients": evaluation.generated_search_info.skipped_ingredients,
            })

            for nutrient in nutrients:
                nutrition_rows.append({
                    "uuid": item.uuid,
                    "nutrient": nutrient,

                    "original recipe": getattr(evaluation.original_recipe_nutrition, nutrient, None),
                    "generated recipe": getattr(evaluation.generated_recipe_nutrition, nutrient, None),

                    "original calculated": getattr(evaluation.original_calculated_nutrition, nutrient, None),
                    "generated calculated": getattr(evaluation.generated_calculated_nutrition, nutrient, None),

                    "recipe change (%)": getattr(evaluation.recipe_nutrition_changes,nutrient, None),
                    "calculated change (%)": getattr(evaluation.calculated_nutrition_changes,nutrient, None),
                })

        evaluation_sheet = pd.DataFrame(evaluation_rows)
        nutrition_comparison_sheet = pd.DataFrame(nutrition_rows)

        output_file = Path("evaluation_export.xlsx")
        with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
            evaluation_sheet.to_excel(writer, sheet_name="Evaluations", index=False)
            nutrition_comparison_sheet.to_excel(writer, sheet_name="Nutrition", index=False)
    finally:
        db.close()

def _calculation_failure_rate(search_info: NutritionSearchInfo) -> float:
    total_ingredients = len(search_info.matched_ingredients) + len(search_info.skipped_ingredients) +len(search_info.failed_ingredients)
    failed_lookups = len(search_info.failed_ingredients)
    return round(failed_lookups / total_ingredients * 100, 1)

if __name__ == "__main__":
    export()
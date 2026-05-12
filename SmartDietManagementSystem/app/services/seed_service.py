import json
from pathlib import Path

from app import db
from app.models.nutrition import FoodItem


def seed_foods():
    if FoodItem.query.first():
        return

    data_path = Path(__file__).resolve().parent.parent / "data" / "foods.json"
    foods = json.loads(data_path.read_text(encoding="utf-8"))

    for item in foods:
        db.session.add(
            FoodItem(
                name=item["name"],
                meal_type=item["meal_type"],
                cuisine=item["cuisine"],
                calories=item["calories"],
                protein=item["protein"],
                carbs=item["carbs"],
                fats=item["fats"],
                fiber=item.get("fiber", 0),
                tags=",".join(item.get("tags", [])),
                ingredients=",".join(item.get("ingredients", [])),
            )
        )
    db.session.commit()

from app import db


class FoodItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(160), nullable=False, index=True)
    meal_type = db.Column(db.String(40), nullable=False, index=True)
    cuisine = db.Column(db.String(80), default="Global")
    calories = db.Column(db.Integer, nullable=False)
    protein = db.Column(db.Float, nullable=False)
    carbs = db.Column(db.Float, nullable=False)
    fats = db.Column(db.Float, nullable=False)
    fiber = db.Column(db.Float, default=0)
    tags = db.Column(db.String(255), default="")
    ingredients = db.Column(db.Text, default="")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "meal_type": self.meal_type,
            "cuisine": self.cuisine,
            "calories": self.calories,
            "protein": self.protein,
            "carbs": self.carbs,
            "fats": self.fats,
            "fiber": self.fiber,
            "tags": [tag.strip() for tag in self.tags.split(",") if tag.strip()],
            "ingredients": [item.strip() for item in self.ingredients.split(",") if item.strip()],
        }

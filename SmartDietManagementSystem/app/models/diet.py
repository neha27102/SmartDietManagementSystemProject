from datetime import datetime

from app import db


class DietPlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, index=True)
    target_calories = db.Column(db.Integer, nullable=False)
    target_protein = db.Column(db.Float, nullable=False)
    target_carbs = db.Column(db.Float, nullable=False)
    target_fats = db.Column(db.Float, nullable=False)
    bmi_value = db.Column(db.Float)
    goal = db.Column(db.String(50))
    dietary_preference = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", back_populates="diet_plans")
    meals = db.relationship("Meal", back_populates="diet_plan", cascade="all, delete-orphan")


class Meal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    diet_plan_id = db.Column(db.Integer, db.ForeignKey("diet_plan.id"), nullable=False, index=True)
    meal_type = db.Column(db.String(40), nullable=False)
    food_item_id = db.Column(db.Integer, db.ForeignKey("food_item.id"), nullable=False)
    calories = db.Column(db.Integer, nullable=False)
    protein = db.Column(db.Float, nullable=False)
    carbs = db.Column(db.Float, nullable=False)
    fats = db.Column(db.Float, nullable=False)

    diet_plan = db.relationship("DietPlan", back_populates="meals")
    food_item = db.relationship("FoodItem")

    def to_dict(self):
        return {
            "id": self.id,
            "meal_type": self.meal_type,
            "food": self.food_item.to_dict(),
            "calories": self.calories,
            "protein": self.protein,
            "carbs": self.carbs,
            "fats": self.fats,
        }


class FavoriteMeal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, index=True)
    food_item_id = db.Column(db.Integer, db.ForeignKey("food_item.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", back_populates="favorites")
    food_item = db.relationship("FoodItem")

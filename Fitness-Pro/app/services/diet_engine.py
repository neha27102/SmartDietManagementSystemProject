from app import db
from app.models.diet import DietPlan, Meal
from app.models.nutrition import FoodItem
from app.services.nutrition_service import DIET_TAG_RULES, MEAL_CALORIE_SPLIT, bmi_for_profile, calorie_and_macro_targets


class DietRecommendationEngine:
    def __init__(self, profile):
        self.profile = profile
        self.targets = calorie_and_macro_targets(profile)
        self.excluded = self._normalized_exclusions(profile.excluded_ingredients if profile else "")
        self.preference = profile.dietary_preference if profile else "vegetarian"
        self.cuisine = profile.preferred_cuisine if profile else "Any"

    def generate(self, user):
        plan = DietPlan(
            user=user,
            target_calories=self.targets["calories"],
            target_protein=self.targets["protein"],
            target_carbs=self.targets["carbs"],
            target_fats=self.targets["fats"],
            bmi_value=bmi_for_profile(self.profile),
            goal=self.profile.fitness_goal,
            dietary_preference=self.preference,
        )
        db.session.add(plan)
        db.session.flush()

        chosen_ids = set()
        for meal_type, calorie_ratio in MEAL_CALORIE_SPLIT.items():
            target = self._meal_target(calorie_ratio)
            item = self._best_food_for_meal(meal_type, target, chosen_ids)
            chosen_ids.add(item.id)
            db.session.add(
                Meal(
                    diet_plan=plan,
                    meal_type=meal_type,
                    food_item=item,
                    calories=item.calories,
                    protein=item.protein,
                    carbs=item.carbs,
                    fats=item.fats,
                )
            )

        db.session.commit()
        return plan

    def replace_meal(self, meal):
        target = self._meal_target(MEAL_CALORIE_SPLIT.get(meal.meal_type, 0.25))
        used_ids = {m.food_item_id for m in meal.diet_plan.meals if m.id != meal.id}
        used_ids.add(meal.food_item_id)
        item = self._best_food_for_meal(meal.meal_type, target, used_ids)
        meal.food_item = item
        meal.calories = item.calories
        meal.protein = item.protein
        meal.carbs = item.carbs
        meal.fats = item.fats
        db.session.commit()
        return meal

    def _meal_target(self, ratio):
        return {
            "calories": self.targets["calories"] * ratio,
            "protein": self.targets["protein"] * ratio,
            "carbs": self.targets["carbs"] * ratio,
            "fats": self.targets["fats"] * ratio,
        }

    def _best_food_for_meal(self, meal_type, target, blocked_ids):
        query = FoodItem.query.filter_by(meal_type=meal_type)
        if self.cuisine and self.cuisine.lower() != "any":
            query = query.filter(FoodItem.cuisine == self.cuisine)
        candidates = [food for food in query.all() if food.id not in blocked_ids and self._allowed(food)]
        if not candidates:
            candidates = [food for food in FoodItem.query.filter_by(meal_type=meal_type).all() if food.id not in blocked_ids]
        return sorted(candidates, key=lambda food: self._score(food, target))[0]

    def _allowed(self, food):
        tags = {tag.strip() for tag in food.tags.split(",") if tag.strip()}
        ingredients = {item.strip().lower() for item in food.ingredients.split(",") if item.strip()}
        rules = DIET_TAG_RULES.get(self.preference, {"required_any": set(), "blocked": set()})
        has_required = not rules["required_any"] or bool(tags & rules["required_any"])
        no_blocked_tags = not bool(tags & rules["blocked"])
        no_exclusions = not bool(ingredients & self.excluded)
        return has_required and no_blocked_tags and no_exclusions

    def _score(self, food, target):
        calorie_gap = abs(food.calories - target["calories"]) / max(target["calories"], 1)
        protein_gap = abs(food.protein - target["protein"]) / max(target["protein"], 1)
        carb_gap = abs(food.carbs - target["carbs"]) / max(target["carbs"], 1)
        fat_gap = abs(food.fats - target["fats"]) / max(target["fats"], 1)
        fiber_bonus = min(food.fiber, 12) / 80
        return calorie_gap * 2.2 + protein_gap * 1.4 + carb_gap + fat_gap - fiber_bonus

    @staticmethod
    def _normalized_exclusions(value):
        return {item.strip().lower() for item in value.split(",") if item.strip()}

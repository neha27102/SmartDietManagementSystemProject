from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app import db
from app.models.diet import DietPlan, FavoriteMeal, Meal
from app.models.nutrition import FoodItem
from app.services.diet_engine import DietRecommendationEngine
from app.services.nutrition_service import calorie_and_macro_targets
from app.utils.validation import parse_int

diet_bp = Blueprint("diet", __name__, url_prefix="/diet")


@diet_bp.route("/")
@login_required
def planner():
    plan = DietPlan.query.filter_by(user_id=current_user.id).order_by(DietPlan.created_at.desc()).first()
    foods = FoodItem.query.order_by(FoodItem.name.asc()).all()
    targets = calorie_and_macro_targets(current_user.profile)
    return render_template("diet.html", plan=plan, foods=foods, targets=targets)


@diet_bp.route("/generate", methods=["POST"])
@login_required
def generate():
    profile = current_user.profile
    profile.custom_calorie_target = parse_int(request.form.get("custom_calorie_target"), profile.custom_calorie_target)
    profile.excluded_ingredients = request.form.get("excluded_ingredients", profile.excluded_ingredients or "")
    profile.preferred_cuisine = request.form.get("preferred_cuisine", profile.preferred_cuisine or "Any")
    profile.dietary_preference = request.form.get("dietary_preference", profile.dietary_preference or "vegetarian")
    plan = DietRecommendationEngine(profile).generate(current_user)
    flash(f"Generated a {plan.target_calories} calorie plan using nutrition scoring.", "success")
    return redirect(url_for("diet.planner"))


@diet_bp.route("/api/regenerate", methods=["POST"])
@login_required
def regenerate_api():
    plan = DietRecommendationEngine(current_user.profile).generate(current_user)
    return jsonify(plan_to_dict(plan))


@diet_bp.route("/api/meals/<int:meal_id>/replace", methods=["POST"])
@login_required
def replace_meal(meal_id):
    meal = Meal.query.join(DietPlan).filter(Meal.id == meal_id, DietPlan.user_id == current_user.id).first_or_404()
    updated = DietRecommendationEngine(current_user.profile).replace_meal(meal)
    return jsonify(updated.to_dict())


@diet_bp.route("/favorites/<int:food_id>", methods=["POST"])
@login_required
def favorite(food_id):
    food = FoodItem.query.get_or_404(food_id)
    exists = FavoriteMeal.query.filter_by(user_id=current_user.id, food_item_id=food.id).first()
    if not exists:
        db.session.add(FavoriteMeal(user=current_user, food_item=food))
        db.session.commit()
        flash("Meal saved to favorites.", "success")
    return redirect(url_for("diet.planner"))


def plan_to_dict(plan):
    return {
        "id": plan.id,
        "target_calories": plan.target_calories,
        "target_protein": plan.target_protein,
        "target_carbs": plan.target_carbs,
        "target_fats": plan.target_fats,
        "meals": [meal.to_dict() for meal in plan.meals],
    }

from flask import Blueprint, jsonify, render_template
from flask_login import current_user, login_required

from app.models.tracking import BMIRecord, ProgressEntry
from app.services.nutrition_service import calorie_and_macro_targets

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")


@dashboard_bp.route("/")
@login_required
def dashboard():
    latest_bmi = BMIRecord.query.filter_by(user_id=current_user.id).order_by(BMIRecord.created_at.desc()).first()
    latest_progress = ProgressEntry.query.filter_by(user_id=current_user.id).order_by(ProgressEntry.entry_date.desc()).first()
    targets = calorie_and_macro_targets(current_user.profile)
    return render_template("dashboard.html", latest_bmi=latest_bmi, latest_progress=latest_progress, targets=targets)


@dashboard_bp.route("/api/summary")
@login_required
def summary():
    bmi_records = BMIRecord.query.filter_by(user_id=current_user.id).order_by(BMIRecord.created_at.asc()).limit(12).all()
    progress = ProgressEntry.query.filter_by(user_id=current_user.id).order_by(ProgressEntry.entry_date.asc()).limit(14).all()
    start_weight = progress[0].weight_kg if progress else (current_user.profile.weight_kg or 0)
    current_weight = progress[-1].weight_kg if progress else start_weight
    goal = current_user.profile.fitness_goal
    expected_change = {"weight_loss": -5, "muscle_gain": 3, "maintenance": 0}.get(goal, 0)
    if expected_change == 0:
        completion = 100 if abs(current_weight - start_weight) <= 1 else 70
    else:
        completion = min(100, max(0, abs(current_weight - start_weight) / abs(expected_change) * 100))
    return jsonify(
        {
            "bmi": [{"date": item.created_at.strftime("%d %b"), "value": item.bmi_value} for item in bmi_records],
            "weight": [{"date": item.entry_date.strftime("%d %b"), "value": item.weight_kg} for item in progress],
            "calories": [{"date": item.entry_date.strftime("%d %b"), "value": item.calories_consumed} for item in progress],
            "goal_completion": round(completion, 1),
        }
    )

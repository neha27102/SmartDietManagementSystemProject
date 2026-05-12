from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app import db
from app.utils.validation import parse_float, parse_int

profile_bp = Blueprint("profile", __name__, url_prefix="/profile")


@profile_bp.route("/", methods=["GET", "POST"])
@login_required
def settings():
    profile = current_user.profile
    if request.method == "POST":
        current_user.name = request.form.get("name", current_user.name).strip()
        profile.age = parse_int(request.form.get("age"), profile.age)
        profile.gender = request.form.get("gender", profile.gender)
        profile.height_cm = parse_float(request.form.get("height_cm"), profile.height_cm)
        profile.weight_kg = parse_float(request.form.get("weight_kg"), profile.weight_kg)
        profile.activity_level = request.form.get("activity_level", profile.activity_level)
        profile.fitness_goal = request.form.get("fitness_goal", profile.fitness_goal)
        profile.dietary_preference = request.form.get("dietary_preference", profile.dietary_preference)
        profile.excluded_ingredients = request.form.get("excluded_ingredients", "")
        profile.preferred_cuisine = request.form.get("preferred_cuisine", "Any")
        profile.custom_calorie_target = parse_int(request.form.get("custom_calorie_target"), None)
        db.session.commit()
        flash("Profile updated.", "success")
        return redirect(url_for("dashboard.dashboard"))
    return render_template("profile.html", profile=profile)

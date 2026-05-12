from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app import db
from app.models.tracking import BMIRecord
from app.utils.bmi import analyze_bmi
from app.utils.validation import parse_float

bmi_bp = Blueprint("bmi", __name__, url_prefix="/bmi")


@bmi_bp.route("/", methods=["GET", "POST"])
@login_required
def calculator():
    result = None
    if request.method == "POST":
        height = parse_float(request.form.get("height_cm"))
        weight = parse_float(request.form.get("weight_kg"))
        if not height or not weight or height < 60 or weight < 20:
            flash("Enter realistic height and weight values.", "danger")
            return render_template("bmi.html", result=result)
        result = analyze_bmi(height, weight)
        db.session.add(
            BMIRecord(
                user=current_user,
                height_cm=height,
                weight_kg=weight,
                bmi_value=result["bmi"],
                category=result["category"],
                interpretation=result["interpretation"],
            )
        )
        current_user.profile.height_cm = height
        current_user.profile.weight_kg = weight
        db.session.commit()
        flash("BMI record saved.", "success")
        return redirect(url_for("bmi.calculator"))
    latest = BMIRecord.query.filter_by(user_id=current_user.id).order_by(BMIRecord.created_at.desc()).first()
    return render_template("bmi.html", result=result, latest=latest)

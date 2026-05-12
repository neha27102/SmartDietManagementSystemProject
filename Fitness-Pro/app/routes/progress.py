from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app import db
from app.models.tracking import ProgressEntry
from app.utils.validation import parse_float, parse_int

progress_bp = Blueprint("progress", __name__, url_prefix="/progress")


@progress_bp.route("/", methods=["GET", "POST"])
@login_required
def tracker():
    if request.method == "POST":
        weight = parse_float(request.form.get("weight_kg"))
        if not weight:
            flash("Weight is required.", "danger")
            return redirect(url_for("progress.tracker"))
        db.session.add(
            ProgressEntry(
                user=current_user,
                weight_kg=weight,
                calories_consumed=parse_int(request.form.get("calories_consumed"), 0),
                workout_minutes=parse_int(request.form.get("workout_minutes"), 0),
                notes=request.form.get("notes", "").strip(),
            )
        )
        current_user.profile.weight_kg = weight
        db.session.commit()
        flash("Progress entry saved.", "success")
        return redirect(url_for("progress.tracker"))
    entries = ProgressEntry.query.filter_by(user_id=current_user.id).order_by(ProgressEntry.entry_date.desc()).all()
    return render_template("progress.html", entries=entries)

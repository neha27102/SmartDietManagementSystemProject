from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from app import db
from app.models.user import User, UserProfile
from app.utils.validation import is_email, required_fields

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.dashboard"))
    if request.method == "POST":
        missing = required_fields(request.form, ["name", "email", "password"])
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        if missing or not is_email(email) or len(password) < 6:
            flash("Enter a valid name, email, and password of at least 6 characters.", "danger")
            return render_template("auth/signup.html")
        if User.query.filter_by(email=email).first():
            flash("An account with this email already exists.", "warning")
            return render_template("auth/signup.html")

        user = User(name=request.form["name"].strip(), email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.flush()
        db.session.add(UserProfile(user=user))
        db.session.commit()
        login_user(user)
        flash("Welcome to Fitness Pro. Complete your profile to personalize recommendations.", "success")
        return redirect(url_for("profile.settings"))
    return render_template("auth/signup.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.dashboard"))
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(request.form.get("password", "")):
            login_user(user, remember=bool(request.form.get("remember")))
            flash("Logged in successfully.", "success")
            return redirect(url_for("dashboard.dashboard"))
        flash("Invalid email or password.", "danger")
    return render_template("auth/login.html")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("main.home"))

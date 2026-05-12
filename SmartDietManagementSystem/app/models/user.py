from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(180), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    profile = db.relationship("UserProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    bmi_records = db.relationship("BMIRecord", back_populates="user", cascade="all, delete-orphan")
    progress_entries = db.relationship("ProgressEntry", back_populates="user", cascade="all, delete-orphan")
    diet_plans = db.relationship("DietPlan", back_populates="user", cascade="all, delete-orphan")
    favorites = db.relationship("FavoriteMeal", back_populates="user", cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class UserProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, unique=True)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(30))
    height_cm = db.Column(db.Float)
    weight_kg = db.Column(db.Float)
    activity_level = db.Column(db.String(50), default="moderately_active")
    fitness_goal = db.Column(db.String(50), default="maintenance")
    dietary_preference = db.Column(db.String(50), default="vegetarian")
    excluded_ingredients = db.Column(db.Text, default="")
    preferred_cuisine = db.Column(db.String(80), default="Any")
    custom_calorie_target = db.Column(db.Integer)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship("User", back_populates="profile")

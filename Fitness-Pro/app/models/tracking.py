from datetime import date, datetime

from app import db


class BMIRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, index=True)
    height_cm = db.Column(db.Float, nullable=False)
    weight_kg = db.Column(db.Float, nullable=False)
    bmi_value = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(40), nullable=False)
    interpretation = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", back_populates="bmi_records")


class ProgressEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, index=True)
    entry_date = db.Column(db.Date, default=date.today, nullable=False)
    weight_kg = db.Column(db.Float, nullable=False)
    calories_consumed = db.Column(db.Integer, default=0)
    workout_minutes = db.Column(db.Integer, default=0)
    notes = db.Column(db.String(255), default="")

    user = db.relationship("User", back_populates="progress_entries")

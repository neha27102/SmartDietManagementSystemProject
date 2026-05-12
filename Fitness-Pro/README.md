# Fitness Pro

Fitness Pro is a full-stack Flask, SQLite, SQLAlchemy, HTML, CSS, and JavaScript project for BMI analysis, progress tracking, and data-driven diet planning.

## Features

- Secure signup, login, logout, password hashing, and session handling
- Profile setup with age, gender, height, weight, activity level, fitness goal, and dietary preference
- Scientific BMI calculation with category and interpretation
- Data-driven diet recommendation engine using a reusable JSON nutrition dataset
- Meal regeneration, replacement, favorite meals, cuisine filtering, calorie target adjustment, and ingredient exclusions
- Progress dashboard with Chart.js analytics and AJAX updates
- Modular Flask architecture with blueprints, models, services, utilities, templates, and static files

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python init_db.py
python run.py
```

Open `http://127.0.0.1:5000`.

## Demo Login

After `python init_db.py`, create your own account from the signup page.

## Project Structure

```text
fitness-pro/
  app/
    data/foods.json
    models/
    routes/
    services/
    static/
    templates/
    utils/
  instance/fitness_pro.db
  init_db.py
  run.py
```

## Viva Talking Points

- The diet engine does not use fixed `if user_type == ...` meal outputs. It loads foods from a structured dataset, filters by dietary rules, computes BMR/TDEE/calorie targets, splits calories by meal, scores foods against macro targets, and builds balanced meals dynamically.
- SQLAlchemy relationships connect users, profiles, BMI records, progress entries, generated plans, meals, and favorites.
- Chart.js and fetch APIs keep dashboard data dynamic without full page reloads.

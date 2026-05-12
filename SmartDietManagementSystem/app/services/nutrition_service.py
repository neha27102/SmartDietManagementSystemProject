from app.utils.bmi import calculate_bmi

ACTIVITY_MULTIPLIERS = {
    "sedentary": 1.2,
    "lightly_active": 1.375,
    "moderately_active": 1.55,
    "very_active": 1.725,
}

GOAL_CALORIE_ADJUSTMENTS = {
    "weight_loss": -450,
    "muscle_gain": 350,
    "maintenance": 0,
}

GOAL_MACRO_RATIOS = {
    "weight_loss": {"protein": 0.32, "carbs": 0.38, "fats": 0.30},
    "muscle_gain": {"protein": 0.30, "carbs": 0.45, "fats": 0.25},
    "maintenance": {"protein": 0.25, "carbs": 0.45, "fats": 0.30},
}

MEAL_CALORIE_SPLIT = {
    "breakfast": 0.25,
    "lunch": 0.35,
    "dinner": 0.30,
    "snack": 0.10,
}

DIET_TAG_RULES = {
    "vegetarian": {"required_any": {"vegetarian", "vegan"}, "blocked": {"non_vegetarian"}},
    "non_vegetarian": {"required_any": {"non_vegetarian"}, "blocked": set()},
    "vegan": {"required_any": {"vegan"}, "blocked": {"dairy", "egg", "meat", "fish", "non_vegetarian"}},
    "keto": {"required_any": {"keto"}, "blocked": {"high_carb"}},
    "halal": {"required_any": {"halal", "vegetarian", "vegan"}, "blocked": {"pork", "alcohol"}},
    "high_protein": {"required_any": {"high_protein"}, "blocked": set()},
    "low_carb": {"required_any": {"low_carb", "keto"}, "blocked": {"high_carb"}},
}


def calculate_bmr(profile):
    if not profile or not all([profile.age, profile.gender, profile.height_cm, profile.weight_kg]):
        return 1800
    base = 10 * profile.weight_kg + 6.25 * profile.height_cm - 5 * profile.age
    return base + (5 if profile.gender == "male" else -161)


def calorie_and_macro_targets(profile):
    bmr = calculate_bmr(profile)
    multiplier = ACTIVITY_MULTIPLIERS.get(profile.activity_level, 1.55)
    target = int(bmr * multiplier + GOAL_CALORIE_ADJUSTMENTS.get(profile.fitness_goal, 0))
    if profile.custom_calorie_target:
        target = int(profile.custom_calorie_target)
    target = max(1200, min(target, 4200))
    ratios = GOAL_MACRO_RATIOS.get(profile.fitness_goal, GOAL_MACRO_RATIOS["maintenance"])
    return {
        "calories": target,
        "protein": round((target * ratios["protein"]) / 4, 1),
        "carbs": round((target * ratios["carbs"]) / 4, 1),
        "fats": round((target * ratios["fats"]) / 9, 1),
    }


def bmi_for_profile(profile):
    if not profile or not profile.height_cm or not profile.weight_kg:
        return None
    return calculate_bmi(profile.height_cm, profile.weight_kg)

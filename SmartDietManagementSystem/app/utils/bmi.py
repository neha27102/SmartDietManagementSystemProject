def calculate_bmi(height_cm, weight_kg):
    height_m = height_cm / 100
    if height_m <= 0:
        raise ValueError("Height must be greater than zero.")
    return round(weight_kg / (height_m * height_m), 1)


def bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    if bmi < 25:
        return "Normal"
    if bmi < 30:
        return "Overweight"
    return "Obese"


def bmi_interpretation(category):
    messages = {
        "Underweight": "Your BMI is below the healthy range. Focus on nutrient-dense meals and strength training.",
        "Normal": "Your BMI is in the healthy range. Keep tracking habits and maintain a balanced routine.",
        "Overweight": "Your BMI is above the healthy range. A modest calorie deficit and consistent movement can help.",
        "Obese": "Your BMI is in a high-risk range. Consider a structured plan and professional medical guidance.",
    }
    return messages[category]


def analyze_bmi(height_cm, weight_kg):
    value = calculate_bmi(height_cm, weight_kg)
    category = bmi_category(value)
    return {
        "bmi": value,
        "category": category,
        "interpretation": bmi_interpretation(category),
    }

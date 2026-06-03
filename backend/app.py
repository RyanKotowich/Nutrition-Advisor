from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

API_KEY = "KEY"


@app.route("/")
def home():
    return "backend works"


@app.route("/api/plan", methods=["POST"])
def plan():

    data = request.get_json()

    calories = int(data.get("calories"))
    diet = data.get("diet")
    goal = data.get("goal").lower().strip()

    if goal in [
        "muscle gain",
        "bulk",
        "bulking",
        "strength"
    ]:

        protein_percent = 0.35
        carb_percent = 0.45
        fat_percent = 0.20

        recommendation = (
            "high protein and complex carbohydrates "
            "for muscle growth and recovery"
        )

    elif goal in [
        "weight loss",
        "cut",
        "cutting",
        "fat loss"
    ]:

        protein_percent = 0.40
        carb_percent = 0.30
        fat_percent = 0.30

        recommendation = (
            "high satiety foods and increased fiber "
            "for appetite control"
        )

    elif goal in [
        "athlete",
        "sports",
        "performance"
    ]:

        protein_percent = 0.30
        carb_percent = 0.50
        fat_percent = 0.20

        recommendation = (
            "higher carbohydrates and hydration "
            "for athletic performance"
        )

    else:

        protein_percent = 0.30
        carb_percent = 0.40
        fat_percent = 0.30

        recommendation = "balanced nutrition"

    protein_grams = int(
        (calories * protein_percent) / 4
    )

    carb_grams = int(
        (calories * carb_percent) / 4
    )

    fat_grams = int(
        (calories * fat_percent) / 9
    )

    prompt = f"""
    Create a healthy meal plan that fits these requirements:

    Calories: {calories}
    Diet type: {diet}
    Goal: {goal}

    Nutritional targets:
    - Protein: {protein_grams}g
    - Carbohydrates: {carb_grams}g
    - Fat: {fat_grams}g

    Research-informed recommendation:
    {recommendation}

    Include:
    - Breakfast
    - Lunch
    - Dinner

    Keep it realistic and practical.
    """

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",

        headers={
            "Authorization":
                f"Bearer {OPENROUTER_API_KEY}",

            "Content-Type":
                "application/json",

            "HTTP-Referer":
                "http://localhost:5500",

            "X-Title":
                "AI Nutrition Advisor"
        },

        json={

            "model":
                "mistralai/mistral-7b-instruct",

            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }
    )

    result = response.json()

    try:

        ai_response = (
            result["choices"][0]
                  ["message"]
                  ["content"]
        )

        final_response = f"""
Nutrition Targets

Protein: {protein_grams}g
Carbohydrates: {carb_grams}g
Fat: {fat_grams}g

AI Meal Plan

{ai_response}
"""

        return jsonify({
            "result": final_response
        })

    except Exception:

        return jsonify({
            "result": "API ERROR",
            "details": result
        })


if __name__ == "__main__":
    app.run(debug=True)

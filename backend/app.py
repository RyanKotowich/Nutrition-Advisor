from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

USDA_API_KEY = "fgh4QUFFtgbSc0E3zjZyIv/////GsCSvzeyfuiSO6a062///"
OPENROUTER_API_KEY = "3b490466db78c64a1d99556e601cd78219315/////sk-or-v1-f949bc84f39e95c32bcb4f98eb7"


def get_macro_targets(calories, goal):
    if goal == "athletic":
        ratios = {"protein": 0.30, "carbs": 0.45, "fat": 0.25}
    elif goal == "cut":
        ratios = {"protein": 0.40, "carbs": 0.30, "fat": 0.30}
    elif goal == "bulk":
        ratios = {"protein": 0.25, "carbs": 0.50, "fat": 0.25}
    else:
        ratios = {"protein": 0.30, "carbs": 0.40, "fat": 0.30}

    protein_cal = calories * ratios["protein"]
    carbs_cal = calories * ratios["carbs"]
    fat_cal = calories * ratios["fat"]

    return {
        "protein_g": protein_cal / 4,
        "carbs_g": carbs_cal / 4,
        "fat_g": fat_cal / 9
    }


def get_food(food_name):
    url = "https://api.nal.usda.gov/fdc/v1/foods/search"

    params = {
        "query": food_name,
        "pageSize": 1,
        "api_key": USDA_API_KEY
    }

    res = requests.get(url, params=params)
    data = res.json()

    try:
        food = data["foods"][0]

        result = {
            "name": food["description"],
            "calories": 0,
            "protein": 0,
            "carbs": 0,
            "fat": 0
        }

        for n in food.get("foodNutrients", []):
            name = n.get("nutrientName", "").lower()
            value = n.get("value", 0)

            if "energy" in name:
                result["calories"] = value
            elif "protein" in name:
                result["protein"] = value
            elif "carbohydrate" in name:
                result["carbs"] = value
            elif "total lipid" in name:
                result["fat"] = value

        return result

    except:
        return None


@app.route("/")
def home():
    return "API running"


@app.route("/api/plan", methods=["POST"])
def plan():
    try:
        data = request.get_json()

        calories = int(data.get("calories", 2000))
        diet = data.get("diet", "")
        goal = data.get("goal", "")

        macros = get_macro_targets(calories, goal)

        food_prompt = f"""
Return 30 real foods for a {goal} diet with {diet} preference.

Rules:
- real USDA-style foods only
- comma separated only
- no explanation
"""

        food_response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "openai/gpt-oss-120b:free",
                "messages": [{"role": "user", "content": food_prompt}]
            }
        )

        food_text = food_response.json()["choices"][0]["message"]["content"]

        foods = [f.strip() for f in food_text.split(",") if f.strip()]
        foods = list(dict.fromkeys(foods))

        nutrition = []

        for f in foods:
            item = get_food(f)
            if item:
                nutrition.append(item)

        context = "\n".join([
            f"- NAME: {i['name']}\n  CALORIES: {i['calories']}\n  PROTEIN: {i['protein']}\n  CARBS: {i['carbs']}\n  FAT: {i['fat']}"
            for i in nutrition
        ])

        prompt = f"""
You are strictly a nutrition engine, follow said instructions.

ONLY use foods from dataset.

MACRO TARGETS (grams):
Protein: {macros['protein_g']}
Carbs: {macros['carbs_g']}
Fat: {macros['fat_g']}

DATASET:
{context}

Rules:
- use only NAME values
- do not invent foods
- do not rename foods
- balance meals across day
-do not use asterisks

Output:
Breakfast: ...
Lunch: ...
Dinner: ...
Snacks: ...
"""

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "openai/gpt-oss-120b:free",
                "messages": [{"role": "user", "content": prompt}]
            }
        )

        result = response.json()["choices"][0]["message"]["content"]

        return jsonify({
            "result": result,
            "macros": macros,
            "calories": calories,
            "goal": goal
        })

    except Exception as e:
        return jsonify({
            "result": "Error generating plan",
            "error": str(e)
        })


if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

USDA_API_KEY = "62fgh4QUFFtgbSc0E3zjZyI////GsCSvzeyfuiSO6a0"
OPENROUTER_API_KEY = "fa1022e44e709ee71a6f98147100f70c96e1f85e///////sk-or-v1-6599396112fecae8de7d9f07"


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

        food_prompt = f"""
Return 12 real foods for a {goal} diet with {diet} preference.
Comma separated only. No explanation.
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
            f"{i['name']} | {i['calories']} kcal | P:{i['protein']} C:{i['carbs']} F:{i['fat']}"
            for i in nutrition
        ])

        prompt = f"""
Create a daily meal plan.

ONLY use foods from this list:
{context}

Goal: {goal}
Diet: {diet}
Calories: {calories}

Format:
Breakfast: ...
Lunch: ...
Dinner: ...
Snacks: ...

No extra text.
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

        return jsonify({"result": result})

    except Exception as e:
        return jsonify({"result": "Error generating plan", "error": str(e)})


if __name__ == "__main__":
    app.run(debug=True)

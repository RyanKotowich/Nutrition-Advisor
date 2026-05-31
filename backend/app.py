from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

OPENROUTER_API_KEY = "PASTE_YOUR_KEY_HERE"


@app.route("/")
def home():
    return "AI Nutrition Advisor backend is running!"


@app.route("/api/plan", methods=["POST"])
def plan():
    data = request.get_json()

    calories = data.get("calories")
    diet = data.get("diet")

    prompt = f"""
    You are a nutrition assistant.

    Create a simple meal plan.

    Calories: {calories}
    Diet: {diet}

    Include breakfast, lunch, and dinner.
    """

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:5500",
            "X-Title": "AI Nutrition App"
        },
        json={
            "model": "mistralai/mistral-7b-instruct",
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }
    )

    data = response.json()

    try:
        result = data["choices"][0]["message"]["content"]
        return jsonify({"result": result})

    except Exception:
        return jsonify({
            "result": "API ERROR",
            "details": data
        })


if __name__ == "__main__":
    app.run(debug=True)

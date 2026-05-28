from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

DEEPSEEK_API_KEY = "Put key locally before running"


@app.route("/")
def home():
    return "Backend is running!"


@app.route("/api/plan", methods=["POST"])
def plan():
    data = request.get_json()

    calories = data.get("calories")
    diet = data.get("diet")

    prompt = f"""
    Create a simple healthy meal plan.

    Calories: {calories}
    Diet: {diet}

    Include breakfast, lunch, dinner.
    Keep it simple and clear.
    """

    response = requests.post(
        "https://api.deepseek.com/chat/completions",
        headers={
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "deepseek-chat",
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }
    )

    result = response.json()["choices"][0]["message"]["content"]

    return jsonify({"result": result})


if __name__ == "__main__":
    app.run(debug=True)

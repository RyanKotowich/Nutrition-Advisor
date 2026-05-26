from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/api/plan", methods=["POST"])
def plan():
    data = request.json

    calories = data.get("calories")
    diet = data.get("diet")

    # temporary fake AI response (we will replace with DeepSeek later)
    result = f"AI Plan: {calories} calorie {diet} diet with balanced meals."

    return jsonify({"result": result})

if __name__ == "__main__":
    app.run(debug=True)

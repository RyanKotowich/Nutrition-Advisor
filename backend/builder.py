import requests
import json
import time

USDA_API_KEY = "fgh4QUFFtgbSc0E3zjZyIv/////GsCSvzeyfuiSO6a062"

search_terms = {
    "proteins": [
        "salmon",
        "steak",
        "chicken breast",
        "turkey",
        "shrimp",
        "greek yogurt",
        "tofu",
        "tuna"
    ],

    "carbs": [
        "jasmine rice",
        "oatmeal",
        "sweet potato",
        "quinoa",
        "whole wheat pasta",
        "bagel",
        "beans"
    ],

    "fats": [
        "avocado",
        "almonds",
        "peanut butter",
        "olive oil",
        "walnuts"
    ],

    "fruits": [
        "banana",
        "blueberries",
        "apple",
        "strawberries",
        "pineapple"
    ],

    "vegetables": [
        "broccoli",
        "asparagus",
        "spinach",
        "bell peppers",
        "zucchini"
    ]
}


def search_food(query):

    url = "https://api.nal.usda.gov/fdc/v1/foods/search"

    params = {
        "query": query,
        "pageSize": 10,
        "api_key": USDA_API_KEY
    }

    res = requests.get(url, params=params)

    return res.json().get("foods", [])


def extract_macros(food):

    item = {
        "name": food.get("description", ""),
        "calories": 0,
        "protein": 0,
        "carbs": 0,
        "fat": 0
    }

    for n in food.get("foodNutrients", []):

        name = n.get("nutrientName", "").lower()
        value = n.get("value", 0)

        if "energy" in name:
            item["calories"] = value

        elif "protein" in name:
            item["protein"] = value

        elif "carbohydrate" in name:
            item["carbs"] = value

        elif "total lipid" in name:
            item["fat"] = value

    return item


database = {
    "proteins": [],
    "carbs": [],
    "fats": [],
    "fruits": [],
    "vegetables": []
}


seen = set()

for category, queries in search_terms.items():

    for q in queries:

        foods = search_food(q)

        for food in foods:

            item = extract_macros(food)

            name = item["name"]

            if not name:
                continue

            if name in seen:
                continue

            if item["calories"] <= 0:
                continue

            seen.add(name)

            database[category].append(item)

        time.sleep(1)


with open("foods.json", "w") as f:
    json.dump(database, f, indent=2)

print("foods.json created successfully")

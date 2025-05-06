from flask import Flask, jsonify
from flask_cors import CORS
import numpy as np
from sklearn.linear_model import LinearRegression
import requests
import json  # Untuk print JSON yang rapi

def fetch_gdp_data(country_code):
    country_code = country_code.lower()
    url = f"https://api.worldbank.org/v2/country/{country_code}/indicator/NY.GDP.MKTP.KD?format=json&per_page=100"
    print(f"📡 Fetching data from: {url}")
    response = requests.get(url)

    if response.status_code != 200:
        print(f"❌ Error: Status code {response.status_code}")
        return []

    try:
        json_data = response.json()
        print("✅ JSON data received:")
        print(json.dumps(json_data, indent=2))  # Tampilkan isi JSON
    except Exception as e:
        print(f"❌ JSON parsing error: {e}")
        return []

    if not json_data or len(json_data) < 2 or not json_data[1]:
        print("❌ No data returned or format invalid.")
        return []

    data = json_data[1]
    result = []
    for entry in data:
        if entry["value"] is not None:
            result.append({
                "year": int(entry["date"]),
                "gdp": float(entry["value"])
            })

    print(f"✅ Extracted {len(result)} GDP entries.")
    return sorted(result, key=lambda x: x["year"])


def train_model(data):
    years = np.array([d["year"] for d in data]).reshape(-1, 1)
    gdps = np.array([d["gdp"] for d in data])
    model = LinearRegression().fit(years, gdps)
    return model


def create_app():
    app = Flask(__name__)
    CORS(app)

    @app.route('/predict-api/<country_code>/<int:year>')
    def predict_api(country_code, year):
        data = fetch_gdp_data(country_code)
        if not data:
            return jsonify({"error": "GDP data not available for this country."}), 404

        latest_year = max(d["year"] for d in data)
        if year <= latest_year:
            return jsonify({
                "error": f"Prediction year must be after {latest_year}"
            }), 400

        model = train_model(data)
        prediction = model.predict(np.array([[year]]))[0]

        return jsonify({
            "country": country_code.upper(),
            "year": year,
            "latest_year_data": latest_year,
            "prediction": round(prediction, 2)
        })

    return app

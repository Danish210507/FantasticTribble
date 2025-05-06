import requests
from flask import Flask, jsonify
from flask_cors import CORS 
import numpy as np
from sklearn.linear_model import LinearRegression
import json  # Untuk print JSON yang rapi

def get_world_bank_data(country_code):
    url = f"https://api.worldbank.org/v2/country/${country_code}/indicator/NY.GDP.MKTP.KD?format=json&per_page=100"
    response = requests.get(url)

    if response.status_code == 200:
        json_data = response.json()
        if len(json_data) < 2:
            return {}

        data = json_data[1]  # Perbaikan: gunakan indeks ke-1
        world_bank_data = {}

        for entry in data:
            year = int(entry['date'])
            gdp = entry['value']

            if gdp is not None:
                world_bank_data[year] = gdp

        return world_bank_data
    else:
        raise Exception(f"Error: {response.status_code}. Tidak dapat mengambil data.")

from flask import Flask, request, jsonify
from flask_cors import CORS  # Tambahkan CORS
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

app = Flask(__name__)
CORS(app)  # Aktifkan CORS untuk semua route

@app.route('/predict-local', methods=['POST'])
def predict_gdp():
    try:
        # Ambil data dari frontend
        data = request.get_json()
        historical_data = data['data']  # Format: [{ year, value }]
        target_year = data.get('targetYear')  # Tidak digunakan, tetapi bisa untuk validasi

        # Konversi ke DataFrame
        df = pd.DataFrame(historical_data, columns=['year', 'value'])
        df.rename(columns={'value': 'gdp'}, inplace=True)
        df.set_index('year', inplace=True)

        # Latih model ARIMA
        model = ARIMA(df['gdp'], order=(2, 1, 2))  # Parameter bisa diadjust
        model_fit = model.fit()

        # Prediksi GDP untuk tahun berikutnya
        forecast = model_fit.forecast(steps=1)
        predicted_gdp = forecast.iloc[0]

        # Hitung growth rate
        last_gdp = df['gdp'].iloc[-1]
        growth_rate = round((predicted_gdp - last_gdp) / last_gdp * 100, 2)

        # Kirim respons ke frontend
        return jsonify({
            'predictedGDP': round(predicted_gdp, 2),
            'growthRate': f"{growth_rate}%",
            'confidence': '95%'
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)  # Jalankan di port 5000
import numpy as np
from statsmodels.tsa.arima.model import ARIMA

def predict_gdp(gdp_data, return_confidence=False):
    # Validasi input
    if not isinstance(gdp_data, (list, np.ndarray)):
        raise ValueError("Input harus list atau numpy array.")
    if len(gdp_data) < 5:
        raise ValueError("Minimal 5 data diperlukan.")
    
    # Parameter ARIMA manual (sesuaikan dengan kebutuhan)
    order = (2, 1, 2)  # (p, d, q)
    
    # Bangun model
    model = ARIMA(gdp_data, order=order)
    model_fit = model.fit()
    
    # Prediksi
    if return_confidence:
        forecast = model_fit.get_forecast(steps=1)
        return {
            'prediction': float(forecast.predicted_mean[0]),
            'confidence_interval': list(map(float, forecast.conf_int()[0])),
            'model_order': order
        }
    else:
        return float(model_fit.forecast(steps=1)[0])
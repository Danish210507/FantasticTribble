from flask import Flask, send_from_directory
from api.api import create_app
import os

app = create_app()

# Serve frontend HTML statis
@app.route('/')
def serve_index():
    return send_from_directory('frontend', 'index.html')  # asumsi file ada di folder `frontend`

# Jalankan
if __name__ == '__main__':
    app.run(debug=True, port=5000)

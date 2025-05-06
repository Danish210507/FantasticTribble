import pandas as pd
import numpy as np

def clean_data(data):
    # Konversi list of dicts ke DataFrame
    df = pd.DataFrame(data)

    # Pastikan kolom yang dibutuhkan tersedia
    if 'year' not in df.columns or 'gdp' not in df.columns:
        raise ValueError("Data tidak mengandung kolom 'year' dan 'gdp'")

    # Hapus baris dengan nilai null
    df_cleaned = df.dropna(subset=['year', 'gdp'])

    # Pastikan tipe data benar
    df_cleaned['year'] = df_cleaned['year'].astype(int)
    df_cleaned['gdp'] = df_cleaned['gdp'].astype(float)

    return df_cleaned

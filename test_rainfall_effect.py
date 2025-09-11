"""
Csapadék hatás tesztelése
========================

Teszteli, hogy a modell hogyan reagál a csapadék változására.
"""

import pandas as pd
import numpy as np
import joblib
from datetime import datetime
import sys
import os
sys.path.insert(0, 'src')
from data_preparation import DataPreparation

# Modellek betöltése
print("📊 Csapadék Hatás Tesztelése")
print("=" * 60)

try:
    model = joblib.load('models/best_model_random_forest.joblib')
    scaler = joblib.load('models/scaler.joblib')
    print("✅ Model és scaler betöltve")
except:
    print("❌ Hiba a model/scaler betöltésekor")
    sys.exit(1)

# Feature nevek betöltése
data_prep = DataPreparation()
df = pd.read_csv('data/hackathon_data.csv')
df['datum'] = pd.to_datetime(df['datum'])
df = data_prep.create_features(df)
df = data_prep.encode_categorical(df)
feature_columns = [col for col in df.columns if col not in ['datum', 'latogatoszam']]

# Teszt dátum: átlagos hétköznap
test_date = datetime(2024, 9, 18)  # Szerda
base_features = {
    'atlaghomerseklet': 20.0,
    'csapadek': 0.0,
    'unnepnap': 0,
    'iskolai_szunet': 0,
    'marketing_kiadas': 300,
    'hetvege': 0,
    'ev': test_date.year,
    'het_szama': test_date.isocalendar()[1],
    'ev_napja': test_date.timetuple().tm_yday,
    'hideg': 0,
    'meleg': 0,
    'esik': 0,
    'alacsony_marketing': 0,
    'magas_marketing': 0,
    'hetvege_es_jo_ido': 0,
    'unnep_es_marketing': 0,
    'latogatoszam_lag1': 10974,
    'atlaghomerseklet_lag1': 20.0,
    'latogatoszam_7d_avg': 10974,
    'atlaghomerseklet_7d_avg': 20.0,
}

# One-hot encoding
for i in range(1, 8):
    base_features[f'nap_{i}'] = int(test_date.weekday() + 1 == i)
for i in range(1, 13):
    base_features[f'honap_{i}'] = int(test_date.month == i)
for i in range(1, 5):
    base_features[f'szezon_{i}'] = int(i == 4)  # Ősz

print("\n🌧️ Csapadék hatás tesztelése:")
print("-" * 40)
print("Alapadatok: Szerda, 20°C, átlagos marketing")
print()

# Különböző csapadék értékek tesztelése
rainfall_values = [0, 0.5, 1, 2, 3, 5, 7, 10, 12, 15, 20, 30, 50, 100]
predictions = []

for rain in rainfall_values:
    # Features másolása és módosítása
    features = base_features.copy()
    features['csapadek'] = rain
    features['esik'] = int(rain > 1)
    
    # DataFrame létrehozása helyes sorrendben
    df_test = pd.DataFrame([features])[feature_columns]
    
    # Skálázás
    numeric_columns = df_test.select_dtypes(include=[np.number]).columns
    df_scaled = df_test.copy()
    df_scaled[numeric_columns] = scaler.transform(df_test[numeric_columns])
    
    # Előrejelzés
    prediction = model.predict(df_scaled)[0]
    predictions.append(prediction)
    
    change = (prediction - predictions[0]) / predictions[0] * 100 if predictions[0] > 0 else 0
    
    print(f"Csapadék: {rain:6.1f} mm → Látogatók: {prediction:8,.0f} ({change:+6.1f}%)")

print("\n📈 Eredmények elemzése:")
print("-" * 40)

# Hatás számítása
base_prediction = predictions[0]
print(f"Száraz idő (0mm): {base_prediction:,.0f} látogató")
print()

# Kategóriák szerinti hatás
categories = [
    (1, "Szitálás (1mm)"),
    (5, "Enyhe eső (5mm)"),
    (10, "Közepes eső (10mm)"),
    (20, "Erős eső (20mm)"),
    (50, "Viharos eső (50mm)")
]

for rain_val, desc in categories:
    idx = rainfall_values.index(rain_val)
    pred = predictions[idx]
    change = (pred - base_prediction) / base_prediction * 100
    print(f"{desc:20s}: {change:+6.1f}% ({pred:,.0f} látogató)")

print("\n⚠️ Megjegyzés:")
print("-" * 40)
print("Az eredeti adatokban a max csapadék 12.1mm volt,")
print("ezért a modell nem tanult meg 12mm feletti értékeket kezelni.")
print("A 20mm+ értékeknél a modell extrapolál, ami pontatlan lehet.")

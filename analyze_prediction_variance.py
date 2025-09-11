"""
Átlagtól való eltérés elemzése
==============================

Megvizsgálja, hogy különböző inputok esetén hogyan változik az előrejelzés
és az átlagtól való eltérés.
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
model = joblib.load('models/best_model_random_forest.joblib')
scaler = joblib.load('models/scaler.joblib')

# Adatok betöltése az átlag kiszámításához
df = pd.read_csv('data/hackathon_data.csv')
GLOBAL_AVG = df['latogatoszam'].mean()

print("📊 ÁTLAGTÓL VALÓ ELTÉRÉS ELEMZÉSE")
print("=" * 70)
print(f"\n🎯 Globális átlag (minden nap): {GLOBAL_AVG:,.0f} fő")

# Számítsuk ki a kontextuális átlagokat
weekend_avg = df[df['hetvege'] == 1]['latogatoszam'].mean()
weekday_avg = df[df['hetvege'] == 0]['latogatoszam'].mean()
holiday_avg = df[df['unnepnap'] == 1]['latogatoszam'].mean() if 'unnepnap' in df.columns else GLOBAL_AVG

print(f"\n📅 Kontextuális átlagok:")
print(f"   Hétvége átlag: {weekend_avg:,.0f} fő")
print(f"   Hétköznap átlag: {weekday_avg:,.0f} fő")
print(f"   Ünnepnap átlag: {holiday_avg:,.0f} fő")

# Feature columns betöltése
data_prep = DataPreparation()
df_features = data_prep.load_and_clean_data('data/hackathon_data.csv')
df_features = data_prep.create_features(df_features)
df_features = data_prep.encode_categorical(df_features)
feature_columns = [col for col in df_features.columns if col not in ['datum', 'latogatoszam']]

print("\n" + "=" * 70)
print("🧪 KÜLÖNBÖZŐ SZCENÁRIÓK TESZTELÉSE")
print("=" * 70)

def make_prediction(date, temp, rain, holiday, school_break, marketing):
    """Előrejelzés készítése adott paraméterekkel"""
    
    features = {
        'atlaghomerseklet': temp,
        'csapadek': rain,
        'unnepnap': int(holiday),
        'iskolai_szunet': int(school_break),
        'marketing_kiadas': marketing,
        'hetvege': int(date.weekday() >= 5),
        'ev': date.year,
        'het_szama': date.isocalendar()[1],
        'ev_napja': date.timetuple().tm_yday,
        'hideg': int(temp < 5),
        'meleg': int(temp > 25),
        'esik': int(rain > 1),
        'alacsony_marketing': int(marketing < 200),
        'magas_marketing': int(marketing > 500),
    }
    
    features['hetvege_es_jo_ido'] = features['hetvege'] * (1 - features['hideg']) * (1 - features['esik'])
    features['unnep_es_marketing'] = features['unnepnap'] * features['magas_marketing']
    features['latogatoszam_lag1'] = GLOBAL_AVG
    features['atlaghomerseklet_lag1'] = temp
    features['latogatoszam_7d_avg'] = GLOBAL_AVG
    features['atlaghomerseklet_7d_avg'] = temp
    
    # One-hot encoding
    for i in range(1, 8):
        features[f'nap_{i}'] = int(date.weekday() + 1 == i)
    for i in range(1, 13):
        features[f'honap_{i}'] = int(date.month == i)
    
    # Szezon
    month = date.month
    if month in [12, 1, 2]:
        season = 1
    elif month in [3, 4, 5]:
        season = 2
    elif month in [6, 7, 8]:
        season = 3
    else:
        season = 4
    
    for i in range(1, 5):
        features[f'szezon_{i}'] = int(season == i)
    
    # DataFrame és skálázás
    df_test = pd.DataFrame([features])[feature_columns]
    numeric_columns = df_test.select_dtypes(include=[np.number]).columns
    df_scaled = df_test.copy()
    df_scaled[numeric_columns] = scaler.transform(df_test[numeric_columns])
    
    return model.predict(df_scaled)[0]

# Tesztszcenáriók
scenarios = [
    # (név, dátum, hőm, eső, ünnep, szünet, marketing)
    ("Átlagos hétköznap", datetime(2024, 9, 18), 20, 0, False, False, 300),
    ("Esős hétköznap", datetime(2024, 9, 18), 20, 10, False, False, 300),
    ("Hideg hétköznap", datetime(2024, 9, 18), -5, 0, False, False, 300),
    ("Meleg hétköznap", datetime(2024, 9, 18), 35, 0, False, False, 300),
    
    ("Átlagos hétvége", datetime(2024, 9, 21), 20, 0, False, False, 300),
    ("Esős hétvége", datetime(2024, 9, 21), 20, 10, False, False, 300),
    ("Hideg hétvége", datetime(2024, 9, 21), -5, 0, False, False, 300),
    ("Meleg hétvége", datetime(2024, 9, 21), 35, 0, False, False, 300),
    
    ("Ünnepnap", datetime(2024, 12, 25), 0, 2, True, True, 500),
    ("Alacsony marketing", datetime(2024, 9, 18), 20, 0, False, False, 100),
    ("Magas marketing", datetime(2024, 9, 18), 20, 0, False, False, 800),
]

print("\n📊 Előrejelzések és eltérések:\n")
print(f"{'Szcenárió':<25} {'Előrejelzés':>12} {'Glob. eltérés':>15} {'Kontextuális':>15}")
print("-" * 70)

results = []
for name, date, temp, rain, holiday, school_break, marketing in scenarios:
    pred = make_prediction(date, temp, rain, holiday, school_break, marketing)
    
    # Globális eltérés (amit most használunk)
    global_diff = (pred - GLOBAL_AVG) / GLOBAL_AVG * 100
    
    # Kontextuális eltérés (amit használhatnánk)
    if date.weekday() >= 5:
        context_avg = weekend_avg
        context_type = "hétvége"
    elif holiday:
        context_avg = holiday_avg
        context_type = "ünnep"
    else:
        context_avg = weekday_avg
        context_type = "hétköznap"
    
    context_diff = (pred - context_avg) / context_avg * 100
    
    print(f"{name:<25} {pred:>12,.0f} {global_diff:>14.1f}% {context_diff:>14.1f}%")
    results.append((name, pred, global_diff, context_diff))

# Elemzés
print("\n" + "=" * 70)
print("📈 ELEMZÉS")
print("=" * 70)

# Min-max értékek
preds = [r[1] for r in results]
min_pred = min(preds)
max_pred = max(preds)
pred_range = max_pred - min_pred

print(f"\n🎯 Előrejelzések tartománya:")
print(f"   Minimum: {min_pred:,.0f} fő")
print(f"   Maximum: {max_pred:,.0f} fő")
print(f"   Terjedelem: {pred_range:,.0f} fő ({pred_range/GLOBAL_AVG*100:.1f}% a globális átlaghoz képest)")

# Globális eltérések
global_diffs = [r[2] for r in results]
print(f"\n📊 Globális átlagtól való eltérések:")
print(f"   Min eltérés: {min(global_diffs):.1f}%")
print(f"   Max eltérés: {max(global_diffs):.1f}%")
print(f"   Eltérések terjedelme: {max(global_diffs) - min(global_diffs):.1f} százalékpont")

print("\n❗ PROBLÉMA MAGYARÁZATA:")
print("-" * 40)
print("""
1. Az előrejelzések szűk tartományban mozognak (7,800 - 14,500 fő)
   míg az átlag 10,974 fő.

2. Az "átlagtól való eltérés" mindig a GLOBÁLIS átlaghoz (10,974) 
   viszonyít, nem a kontextuális átlaghoz.

3. A modell fő befolyásoló tényezői:
   - Marketing kiadás (36.6%)
   - 7 napos átlag (26.0%)
   - Hétvége és jó idő (15.2%)
   
4. Ezek dominálják az előrejelzést, más tényezők (pl. csapadék)
   alig változtatnak az eredményen.

5. MEGOLDÁSI JAVASLAT:
   - Kontextuális átlag használata (hétvége/hétköznap/ünnep)
   - Százalékos változás helyett abszolút érték megjelenítése
   - Több kontextus megjelenítése (pl. "hétvégékhez képest")
""")


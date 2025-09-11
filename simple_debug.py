import pandas as pd
import numpy as np
from datetime import datetime
import joblib

# Simulate the create_prediction_features function
def create_prediction_features(date, temperature, rainfall, is_holiday, is_school_break, marketing_spend):
    """Előrejelzéshez szükséges jellemzők létrehozása"""
    
    # Alapvető jellemzők
    features = {
        'atlaghomerseklet': temperature,
        'csapadek': rainfall,
        'unnepnap': int(is_holiday),
        'iskolai_szunet': int(is_school_break),
        'marketing_kiadas': marketing_spend,
        'hetvege': int(date.weekday() >= 5),
        'ev': date.year,
        'het_szama': date.isocalendar()[1],
        'ev_napja': date.timetuple().tm_yday,
    }
    
    # Időjárás kategóriák
    features['hideg'] = int(temperature < 5)
    features['meleg'] = int(temperature > 25)
    features['esik'] = int(rainfall > 1)
    
    # Marketing kategóriák
    features['alacsony_marketing'] = int(marketing_spend < 200)
    features['magas_marketing'] = int(marketing_spend > 500)
    
    # Interakciós jellemzők
    features['hetvege_es_jo_ido'] = features['hetvege'] * (1 - features['hideg']) * (1 - features['esik'])
    features['unnep_es_marketing'] = features['unnepnap'] * features['magas_marketing']
    
    # Lag jellemzők (átlagos értékekkel helyettesítjük)
    features['latogatoszam_lag1'] = 10974  # átlagos látogatószám
    features['atlaghomerseklet_lag1'] = temperature
    features['latogatoszam_7d_avg'] = 10974
    features['atlaghomerseklet_7d_avg'] = temperature
    
    # Hét napjai (one-hot encoding)
    for i in range(1, 8):
        features[f'nap_{i}'] = int(date.weekday() + 1 == i)
    
    # Hónapok (one-hot encoding)
    for i in range(1, 13):
        features[f'honap_{i}'] = int(date.month == i)
    
    # Szezonok (one-hot encoding)
    month = date.month
    if month in [12, 1, 2]:
        season = 1  # Tél
    elif month in [3, 4, 5]:
        season = 2  # Tavasz
    elif month in [6, 7, 8]:
        season = 3  # Nyár
    else:
        season = 4  # Ősz
    
    for i in range(1, 5):
        features[f'szezon_{i}'] = int(season == i)
    
    return pd.DataFrame([features])

def test_prediction():
    """Test prediction with different values"""
    
    print("🔍 ELŐREJELZÉS TESZT")
    print("="*50)
    
    # Load model
    try:
        model = joblib.load('models/best_model_random_forest.joblib')
        print("✅ Modell betöltve")
    except Exception as e:
        print(f"❌ Modell betöltési hiba: {e}")
        return
    
    # Test cases
    test_cases = [
        # (date, temp, rain, holiday, school, marketing, description)
        (datetime(2024, 6, 15), 20, 0, False, False, 300, "Szombat, 20°C, 300€"),
        (datetime(2024, 6, 15), 10, 0, False, False, 300, "Szombat, 10°C, 300€"),
        (datetime(2024, 6, 15), 30, 0, False, False, 300, "Szombat, 30°C, 300€"),
        (datetime(2024, 6, 15), 20, 0, False, False, 100, "Szombat, 20°C, 100€"),
        (datetime(2024, 6, 15), 20, 0, False, False, 600, "Szombat, 20°C, 600€"),
        (datetime(2024, 6, 17), 20, 0, False, False, 300, "Hétfő, 20°C, 300€"),
    ]
    
    print("\nTeszt esetek:")
    print("-" * 50)
    
    for i, (date, temp, rain, holiday, school, marketing, desc) in enumerate(test_cases):
        try:
            features = create_prediction_features(date, temp, rain, holiday, school, marketing)
            prediction = model.predict(features)[0]
            
            # Calculate percentage difference from average
            avg_visitors = 10974  # From the code
            percentage_diff = (prediction - avg_visitors) / avg_visitors * 100
            
            print(f"{i+1}. {desc:<25}: {prediction:8,.0f} fő ({percentage_diff:+5.1f}%)")
            
        except Exception as e:
            print(f"{i+1}. {desc:<25}: ❌ Hiba: {e}")
    
    # Test with the exact same values multiple times
    print(f"\nIsmételt teszt ugyanazzal az értékkel:")
    print("-" * 50)
    
    test_date = datetime(2024, 6, 15)
    for i in range(5):
        features = create_prediction_features(test_date, 20, 0, False, False, 300)
        prediction = model.predict(features)[0]
        avg_visitors = 10974
        percentage_diff = (prediction - avg_visitors) / avg_visitors * 100
        print(f"{i+1}. Szombat, 20°C, 300€: {prediction:8,.0f} fő ({percentage_diff:+5.1f}%)")

if __name__ == "__main__":
    test_prediction()

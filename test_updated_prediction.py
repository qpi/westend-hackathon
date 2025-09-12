#!/usr/bin/env python3
"""
Test the updated prediction function
"""

import sys
import os
import pandas as pd
import numpy as np
import joblib
from datetime import datetime

# Add paths
sys.path.append('src')

def test_updated_prediction():
    """Test the updated prediction function"""
    
    print("🔍 FRISSÍTETT ELŐREJELZÉS TESZT")
    print("="*50)
    
    # 1. Load components
    print("\n1. KOMPONENSEK BETÖLTÉSE:")
    print("-" * 30)
    
    try:
        # Load model
        model = joblib.load('models/best_model_random_forest.joblib')
        print(f"✅ Modell betöltve: {type(model).__name__}")
        
        # Load training data to get scaler and feature columns
        from data_preparation import DataPreparation
        data_prep = DataPreparation()
        df = data_prep.load_and_clean_data('data/hackathon_data.csv')
        df = data_prep.create_features(df)
        df = data_prep.encode_categorical(df)
        X, y, feature_columns = data_prep.prepare_features_target(df)
        scaler = data_prep.scaler
        
        print(f"✅ Scaler létrehozva: {type(scaler).__name__}")
        print(f"✅ Jellemzők száma: {len(feature_columns)}")
        
        # Load historical data
        historical_data = pd.read_csv('data/hackathon_data.csv')
        historical_data['datum'] = pd.to_datetime(historical_data['datum'])
        print(f"✅ Historikus adatok betöltve: {len(historical_data)} sor")
        
    except Exception as e:
        print(f"❌ Hiba a komponensek betöltésekor: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # 2. Create prediction function (simplified version)
    def create_prediction_features_simple(date, temperature, rainfall, is_holiday,
                                        is_school_break, marketing_spend, scaler,
                                        feature_columns, historical_data=None):
        """Simplified version of the prediction function"""
        
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
        
        # Lag jellemzők - VALÓDI historikus adatokból számítása
        if historical_data is not None and not historical_data.empty:
            # Előző napi érték keresése
            prev_date = pd.Timestamp(date) - pd.Timedelta(days=1)
            prev_day_data = historical_data[historical_data['datum'] == prev_date]

            if not prev_day_data.empty:
                # Valódi előző napi értékek használata
                features['latogatoszam_lag1'] = prev_day_data['latogatoszam'].values[0]
                features['atlaghomerseklet_lag1'] = prev_day_data['atlaghomerseklet'].values[0]
                print(f"📊 Valódi előző napi érték: {features['latogatoszam_lag1']:.0f} fő ({prev_date.strftime('%Y-%m-%d')})")
            else:
                # Ha nincs adat az előző napra, használjuk az átlagot
                features['latogatoszam_lag1'] = historical_data['latogatoszam'].mean()
                features['atlaghomerseklet_lag1'] = historical_data['atlaghomerseklet'].mean()
                print(f"⚠️ Nincs adat az előző napra, átlag használata: {features['latogatoszam_lag1']:.0f} fő")

            # 7 napos átlag számítása
            week_start = pd.Timestamp(date) - pd.Timedelta(days=7)
            week_end = pd.Timestamp(date)
            week_data = historical_data[
                (historical_data['datum'] >= week_start) &
                (historical_data['datum'] < week_end)
            ]

            if not week_data.empty and len(week_data) >= 3:
                # Valódi 7 napos átlag használata
                features['latogatoszam_7d_avg'] = week_data['latogatoszam'].mean()
                features['atlaghomerseklet_7d_avg'] = week_data['atlaghomerseklet'].mean()
                print(f"📊 Valódi 7 napos átlag: {features['latogatoszam_7d_avg']:.0f} fő ({len(week_data)} nap adata alapján)")
            else:
                # Ha nincs elég adat, használjuk az átlagot
                features['latogatoszam_7d_avg'] = historical_data['latogatoszam'].mean()
                features['atlaghomerseklet_7d_avg'] = historical_data['atlaghomerseklet'].mean()
                print(f"⚠️ Nincs elég 7 napos adat, átlag használata: {features['latogatoszam_7d_avg']:.0f} fő")
        else:
            # Fallback to estimated values
            base_visitors = 10974
            estimated_visitors = base_visitors
            
            # Apply multipliers based on conditions
            if temperature < 0:
                estimated_visitors *= 0.3
            elif temperature < 5:
                estimated_visitors *= 0.5
            elif temperature > 35:
                estimated_visitors *= 0.4
            elif temperature > 30:
                estimated_visitors *= 0.6
            elif 15 <= temperature <= 25:
                estimated_visitors *= 1.3
            
            if rainfall > 20:
                estimated_visitors *= 0.2
            elif rainfall > 5:
                estimated_visitors *= 0.4
            
            if is_holiday:
                estimated_visitors *= 2.5
            if is_school_break:
                estimated_visitors *= 1.8
            if date.weekday() >= 5:
                estimated_visitors *= 2.0
            
            if marketing_spend > 800:
                estimated_visitors *= 2.0
            elif marketing_spend > 500:
                estimated_visitors *= 1.5
            elif marketing_spend < 100:
                estimated_visitors *= 0.5
            
            features['latogatoszam_lag1'] = estimated_visitors * 0.8
            features['atlaghomerseklet_lag1'] = temperature
            features['latogatoszam_7d_avg'] = estimated_visitors * 1.2
            features['atlaghomerseklet_7d_avg'] = temperature
            print("⚠️ Lag jellemzők ERŐSÍTETT becsléssel")
        
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
        
        # DataFrame létrehozása helyes oszlop sorrenddel
        df = pd.DataFrame([features])
        df = df[feature_columns]  # Helyes sorrend biztosítása
        
        # Numerikus oszlopok skálázása
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        df_scaled = df.copy()
        df_scaled[numeric_columns] = scaler.transform(df[numeric_columns])
        
        return df_scaled
    
    # 3. Test predictions
    print(f"\n2. ELŐREJELZÉSEK TESZTELÉSE:")
    print("-" * 40)
    
    test_cases = [
        # (date, temp, rain, holiday, school, marketing, description)
        (datetime(2024, 1, 15), 20, 0, False, False, 300, "Hétköznap, 20°C, 300€"),
        (datetime(2024, 1, 15), 5, 0, False, False, 300, "Hétköznap, 5°C, 300€"),
        (datetime(2024, 1, 15), 35, 0, False, False, 300, "Hétköznap, 35°C, 300€"),
        (datetime(2024, 1, 15), 20, 0, False, False, 100, "Hétköznap, 20°C, 100€"),
        (datetime(2024, 1, 15), 20, 0, False, False, 800, "Hétköznap, 20°C, 800€"),
        (datetime(2024, 1, 13), 20, 0, False, False, 300, "Szombat, 20°C, 300€"),
        (datetime(2024, 1, 15), 20, 0, True, False, 300, "Ünnepnap, 20°C, 300€"),
    ]
    
    avg_visitors = historical_data['latogatoszam'].mean()
    
    for i, (date, temp, rain, holiday, school, marketing, desc) in enumerate(test_cases):
        try:
            print(f"\n{i+1}. {desc}:")
            features = create_prediction_features_simple(
                date, temp, rain, holiday, school, marketing, 
                scaler, feature_columns, historical_data
            )
            prediction = model.predict(features)[0]
            percentage_diff = (prediction - avg_visitors) / avg_visitors * 100
            
            print(f"   Előrejelzés: {prediction:8,.0f} fő ({percentage_diff:+5.1f}%)")
            
        except Exception as e:
            print(f"   ❌ Hiba: {e}")
    
    print(f"\n✅ TESZT BEFEJEZVE!")
    print(f"Átlagos látogatószám: {avg_visitors:,.0f} fő")

if __name__ == "__main__":
    test_updated_prediction()

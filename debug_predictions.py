#!/usr/bin/env python3
"""
Debug Prediction Values
=======================

Check why predictions are always around 7,800-8,000.
"""

import pandas as pd
import numpy as np
import joblib
import sys
import os
from datetime import datetime

# Add src to path
sys.path.insert(0, 'src')
from data_preparation import DataPreparation

def debug_predictions():
    """Debug prediction values"""
    print("🔍 ELŐREJELZÉS DEBUGGOLÁS")
    print("="*50)
    
    # Load model and data
    try:
        model = joblib.load('models/best_model_random_forest.joblib')
        print("✅ Modell betöltve")
        
        # Load data
        data_prep = DataPreparation()
        df = data_prep.load_and_clean_data('data/hackathon_data.csv')
        df = data_prep.create_features(df)
        df = data_prep.encode_categorical(df)
        X, y, feature_columns = data_prep.prepare_features_target(df)
        
        print(f"✅ Adatok betöltve: {len(df)} sor")
        print(f"📊 Jellemzők száma: {len(feature_columns)}")
        print(f"🎯 Célváltozó átlag: {y.mean():.2f}")
        print(f"🎯 Célváltozó min: {y.min():.2f}")
        print(f"🎯 Célváltozó max: {y.max():.2f}")
        
    except Exception as e:
        print(f"❌ Hiba: {e}")
        return
    
    # Test different scenarios
    test_scenarios = [
        {"name": "Átlagos hétköznap", "temp": 15, "rain": 0, "marketing": 300, "holiday": False, "school": False, "date": datetime(2025, 9, 12)},
        {"name": "Jó idő hétvége", "temp": 25, "rain": 0, "marketing": 500, "holiday": False, "school": False, "date": datetime(2025, 9, 13)},
        {"name": "Rossz idő", "temp": 5, "rain": 20, "marketing": 200, "holiday": False, "school": False, "date": datetime(2025, 9, 12)},
        {"name": "Ünnepnap", "temp": 20, "rain": 0, "marketing": 800, "holiday": True, "school": False, "date": datetime(2025, 9, 12)},
        {"name": "Nyári hétvége", "temp": 30, "rain": 0, "marketing": 600, "holiday": False, "school": True, "date": datetime(2025, 7, 15)},
    ]
    
    print(f"\n🧪 TESZT SZCENÁRIÓK:")
    print("-" * 80)
    
    for scenario in test_scenarios:
        # Create features manually (simplified version)
        features = {
            'atlaghomerseklet': scenario['temp'],
            'csapadek': scenario['rain'],
            'unnepnap': int(scenario['holiday']),
            'iskolai_szunet': int(scenario['school']),
            'marketing_kiadas': scenario['marketing'],
            'hetvege': int(scenario['date'].weekday() >= 5),
            'ev': scenario['date'].year,
            'het_szama': scenario['date'].isocalendar()[1],
            'ev_napja': scenario['date'].timetuple().tm_yday,
        }
        
        # Weather categories
        features['hideg'] = int(scenario['temp'] < 5)
        features['meleg'] = int(scenario['temp'] > 25)
        features['esik'] = int(scenario['rain'] > 1)
        
        # Marketing categories
        features['alacsony_marketing'] = int(scenario['marketing'] < 200)
        features['magas_marketing'] = int(scenario['marketing'] > 500)
        
        # Interaction features
        features['hetvege_es_jo_ido'] = features['hetvege'] * (1 - features['hideg']) * (1 - features['esik'])
        features['unnep_es_marketing'] = features['unnepnap'] * features['magas_marketing']
        
        # Lag features (use averages for now)
        features['latogatoszam_lag1'] = y.mean() * 0.95
        features['atlaghomerseklet_lag1'] = scenario['temp']
        features['latogatoszam_7d_avg'] = y.mean() * 1.05
        features['atlaghomerseklet_7d_avg'] = scenario['temp']
        
        # Day of week encoding
        for i in range(1, 8):
            features[f'nap_{i}'] = int(scenario['date'].weekday() + 1 == i)
        
        # Month encoding
        for i in range(1, 13):
            features[f'honap_{i}'] = int(scenario['date'].month == i)
        
        # Season encoding
        month = scenario['date'].month
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
        
        # Create DataFrame with correct column order
        df_test = pd.DataFrame([features])
        df_test = df_test.reindex(columns=feature_columns, fill_value=0)
        
        # Scale features
        df_scaled = df_test.copy()
        numeric_columns = df_test.select_dtypes(include=[np.number]).columns
        df_scaled[numeric_columns] = data_prep.scaler.transform(df_test[numeric_columns])
        
        # Make prediction
        prediction = model.predict(df_scaled)[0]
        
        global_avg = y.mean()
        diff_pct = ((prediction - global_avg) / global_avg) * 100
        
        print(f"{scenario['name']:20} → {prediction:7.0f} fő ({diff_pct:+6.1f}%)")
    
    # Check feature importance
    print(f"\n📊 TOP 10 LEGFONTOSABB JELLEMZŐK:")
    print("-" * 50)
    if hasattr(model, 'feature_importances_'):
        feature_importance = pd.DataFrame({
            'feature': feature_columns,
            'importance': model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        for i, row in feature_importance.head(10).iterrows():
            print(f"{row['feature']:30} → {row['importance']:.4f}")

if __name__ == "__main__":
    debug_predictions()

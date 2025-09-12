#!/usr/bin/env python3
"""
Test Streamlit Prediction Logic
===============================

Test the exact same logic as Streamlit uses.
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

def test_streamlit_prediction():
    """Test the exact same prediction logic as Streamlit"""
    print("🔍 STREAMLIT ELŐREJELZÉS TESZT")
    print("="*50)
    
    # Load data exactly like Streamlit does
    try:
        data_path = 'data/hackathon_data_full.csv' if os.path.exists('data/hackathon_data_full.csv') else 'data/hackathon_data.csv'
        data = pd.read_csv(data_path)
        data['datum'] = pd.to_datetime(data['datum'])
        print(f"✅ Adatok betöltve: {data_path}")
        print(f"📊 Sorok száma: {len(data)}")
        
        # Calculate global average like Streamlit does
        global_avg = data['latogatoszam'].mean()
        print(f"🌍 Globális átlag: {global_avg:,.2f} fő")
        
    except Exception as e:
        print(f"❌ Hiba az adatok betöltésekor: {e}")
        return
    
    # Load model and scaler exactly like Streamlit does
    try:
        model = joblib.load('models/best_model_random_forest.joblib')
        
        # Recreate scaler from training data
        data_prep = DataPreparation()
        df = data_prep.load_and_clean_data('data/hackathon_data.csv')  # Note: uses original data for scaler
        df = data_prep.create_features(df)
        df = data_prep.encode_categorical(df)
        X, y, feature_columns = data_prep.prepare_features_target(df)
        
        print(f"✅ Modell és scaler betöltve")
        print(f"📊 Scaler training átlag: {y.mean():.2f} fő")
        
    except Exception as e:
        print(f"❌ Hiba a modell betöltésekor: {e}")
        return
    
    # Test with NEW default Streamlit values
    prediction_date = datetime(2025, 9, 12)  # Friday
    temperature = 20  # NEW: was 15
    rainfall = 0.0
    is_holiday = False
    is_school_break = False
    marketing_spend = 450  # NEW: was 300
    
    print(f"\n🧪 ALAPÉRTELMEZETT STREAMLIT ÉRTÉKEK:")
    print(f"📅 Dátum: {prediction_date.strftime('%Y-%m-%d')} ({prediction_date.strftime('%A')})")
    print(f"🌡️ Hőmérséklet: {temperature}°C")
    print(f"🌧️ Csapadék: {rainfall}mm")
    print(f"🎉 Ünnepnap: {is_holiday}")
    print(f"🏫 Iskolai szünet: {is_school_break}")
    print(f"💰 Marketing: {marketing_spend} EUR")
    
    # Create features exactly like Streamlit does
    from web_app.streamlit_app import create_prediction_features
    
    features_df = create_prediction_features(
        prediction_date, temperature, rainfall,
        is_holiday, is_school_break, marketing_spend,
        data_prep.scaler, feature_columns, data
    )
    
    # Make prediction
    prediction = model.predict(features_df)[0]
    
    # Calculate differences exactly like Streamlit does
    difference_from_global = prediction - global_avg
    percentage_diff_global = (difference_from_global / global_avg) * 100
    
    print(f"\n📈 EREDMÉNYEK:")
    print(f"🎯 Előrejelzés: {prediction:,.0f} fő")
    print(f"🌍 Globális átlag: {global_avg:,.0f} fő")
    print(f"📊 Eltérés: {difference_from_global:+,.0f} fő")
    print(f"📊 Százalékos eltérés: {percentage_diff_global:+.1f}%")
    
    # Test with different values
    print(f"\n🧪 KÜLÖNBÖZŐ ÉRTÉKEKKEL:")
    print("-" * 50)
    
    test_cases = [
        {"temp": 25, "rain": 0, "marketing": 500, "desc": "Jó idő, magas marketing"},
        {"temp": 5, "rain": 10, "marketing": 200, "desc": "Rossz idő, alacsony marketing"},
        {"temp": 20, "rain": 0, "marketing": 800, "desc": "Átlagos idő, nagyon magas marketing"},
    ]
    
    for case in test_cases:
        features_df = create_prediction_features(
            prediction_date, case['temp'], case['rain'],
            False, False, case['marketing'],
            data_prep.scaler, feature_columns, data
        )
        
        pred = model.predict(features_df)[0]
        diff_pct = ((pred - global_avg) / global_avg) * 100
        
        print(f"{case['desc']:35} → {pred:7.0f} fő ({diff_pct:+6.1f}%)")

if __name__ == "__main__":
    test_streamlit_prediction()

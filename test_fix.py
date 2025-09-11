#!/usr/bin/env python3
"""
Test the fix for the prediction issue
"""

import sys
import os
import pandas as pd
import numpy as np
import joblib
from datetime import datetime

# Add paths
sys.path.append('src')
sys.path.append('web_app')

def test_prediction_fix():
    """Test if the prediction fix works"""
    
    print("🔍 ELŐREJELZÉS JAVÍTÁS TESZT")
    print("="*50)
    
    # 1. Check if scaler exists
    print("\n1. SCALER ELLENŐRZÉS:")
    print("-" * 30)
    
    scaler_path = 'models/scaler.joblib'
    if os.path.exists(scaler_path):
        print("✅ Scaler fájl létezik")
        try:
            scaler = joblib.load(scaler_path)
            print(f"✅ Scaler betöltve: {type(scaler).__name__}")
        except Exception as e:
            print(f"❌ Scaler betöltési hiba: {e}")
            return False
    else:
        print("❌ Scaler fájl nem létezik")
        print("🔧 Futtassa: python regenerate_model.py")
        return False
    
    # 2. Load model
    print("\n2. MODELL ELLENŐRZÉS:")
    print("-" * 30)
    
    model_path = 'models/best_model_random_forest.joblib'
    if os.path.exists(model_path):
        print("✅ Modell fájl létezik")
        try:
            model = joblib.load(model_path)
            print(f"✅ Modell betöltve: {type(model).__name__}")
        except Exception as e:
            print(f"❌ Modell betöltési hiba: {e}")
            return False
    else:
        print("❌ Modell fájl nem létezik")
        print("🔧 Futtassa: python regenerate_model.py")
        return False
    
    # 3. Test prediction function
    print("\n3. ELŐREJELZÉS TESZT:")
    print("-" * 30)
    
    try:
        # Import the updated function
        from streamlit_app import create_prediction_features
        
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
        
        print("Teszt esetek:")
        print("-" * 50)
        
        for i, (date, temp, rain, holiday, school, marketing, desc) in enumerate(test_cases):
            try:
                # Create features with scaler
                features = create_prediction_features(date, temp, rain, holiday, school, marketing, scaler)
                prediction = model.predict(features)[0]
                
                # Calculate percentage difference from average
                avg_visitors = 10974  # From the code
                percentage_diff = (prediction - avg_visitors) / avg_visitors * 100
                
                print(f"{i+1}. {desc:<25}: {prediction:8,.0f} fő ({percentage_diff:+5.1f}%)")
                
            except Exception as e:
                print(f"{i+1}. {desc:<25}: ❌ Hiba: {e}")
                return False
        
        # 4. Test consistency
        print(f"\n4. KONZISZTENCIA TESZT:")
        print("-" * 30)
        
        test_date = datetime(2024, 6, 15)
        predictions = []
        
        for i in range(5):
            features = create_prediction_features(test_date, 20, 0, False, False, 300, scaler)
            prediction = model.predict(features)[0]
            predictions.append(prediction)
            avg_visitors = 10974
            percentage_diff = (prediction - avg_visitors) / avg_visitors * 100
            print(f"{i+1}. Szombat, 20°C, 300€: {prediction:8,.0f} fő ({percentage_diff:+5.1f}%)")
        
        # Check if all predictions are the same
        if len(set(predictions)) == 1:
            print("✅ Konzisztens előrejelzések")
        else:
            print("❌ Inkonzisztens előrejelzések")
            return False
        
        # 5. Check if predictions vary with input
        print(f"\n5. VARIABILITÁS TESZT:")
        print("-" * 30)
        
        base_features = create_prediction_features(test_date, 20, 0, False, False, 300, scaler)
        base_prediction = model.predict(base_features)[0]
        
        # Test with different temperature
        hot_features = create_prediction_features(test_date, 35, 0, False, False, 300, scaler)
        hot_prediction = model.predict(hot_features)[0]
        
        # Test with different marketing
        high_marketing_features = create_prediction_features(test_date, 20, 0, False, False, 800, scaler)
        high_marketing_prediction = model.predict(high_marketing_features)[0]
        
        print(f"Alap (20°C, 300€):     {base_prediction:8,.0f} fő")
        print(f"Meleg (35°C, 300€):    {hot_prediction:8,.0f} fő")
        print(f"Magas marketing (20°C, 800€): {high_marketing_prediction:8,.0f} fő")
        
        if base_prediction != hot_prediction or base_prediction != high_marketing_prediction:
            print("✅ Az előrejelzések változnak a bemeneti paraméterekkel")
            return True
        else:
            print("❌ Az előrejelzések nem változnak a bemeneti paraméterekkel")
            return False
            
    except Exception as e:
        print(f"❌ Hiba az előrejelzés tesztelése során: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_prediction_fix()
    if success:
        print("\n🎉 JAVÍTÁS SIKERES!")
        print("Az előrejelzések most már változnak a csúszkák mozgatásával.")
    else:
        print("\n❌ JAVÍTÁS SIKERTELEN!")
        print("További munkára van szükség.")
        sys.exit(1)

#!/usr/bin/env python3
"""
Részletes diagnosztika az előrejelzési problémához
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

def diagnose_prediction_issue():
    """Diagnose the prediction issue in detail"""
    
    print("🔍 RÉSZLETES ELŐREJELZÉS DIAGNOSZTIKA")
    print("="*60)
    
    # 1. Load components
    print("\n1. KOMPONENSEK BETÖLTÉSE:")
    print("-" * 40)
    
    try:
        # Load model
        model = joblib.load('models/best_model_random_forest.joblib')
        print(f"✅ Modell betöltve: {type(model).__name__}")
        
        # Load scaler
        scaler = joblib.load('models/scaler.joblib')
        print(f"✅ Scaler betöltve: {type(scaler).__name__}")
        
        # Load training data to understand feature order
        from data_preparation import DataPreparation
        data_prep = DataPreparation()
        X_train, X_test, y_train, y_test, feature_names, summary = data_prep.full_pipeline()
        print(f"✅ Betanítási adatok betöltve: {len(feature_names)} jellemző")
        
    except Exception as e:
        print(f"❌ Hiba a komponensek betöltésekor: {e}")
        return
    
    # 2. Check model expectations
    print(f"\n2. MODELL ELVÁRÁSOK:")
    print("-" * 40)
    
    if hasattr(model, 'feature_names_in_'):
        model_features = list(model.feature_names_in_)
        print(f"Modell által várt jellemzők ({len(model_features)}):")
        for i, feature in enumerate(model_features[:10]):  # First 10
            print(f"  {i+1:2d}. {feature}")
        if len(model_features) > 10:
            print(f"  ... és még {len(model_features)-10} jellemző")
    else:
        print("⚠️ Modell nem tartalmazza a jellemző neveket")
        model_features = feature_names
    
    print(f"Várt jellemzők száma: {len(model_features)}")
    
    # 3. Test prediction function
    print(f"\n3. ELŐREJELZÉSI FÜGGVÉNY TESZT:")
    print("-" * 40)
    
    try:
        from streamlit_app import create_prediction_features
        
        # Create test features
        test_date = datetime(2024, 6, 15)  # Saturday
        test_features = create_prediction_features(
            test_date, 20, 0, False, False, 300, scaler
        )
        
        print(f"Létrehozott jellemzők száma: {len(test_features.columns)}")
        print(f"Jellemzők típusa: {type(test_features)}")
        print(f"Jellemzők shape: {test_features.shape}")
        
        # Check feature order
        prediction_features = list(test_features.columns)
        
        print(f"\nJellemzők összehasonlítása:")
        if len(model_features) == len(prediction_features):
            matches = 0
            for i, (model_f, pred_f) in enumerate(zip(model_features, prediction_features)):
                match = "✅" if model_f == pred_f else "❌"
                if i < 10:  # Show first 10
                    print(f"  {i+1:2d}. {model_f:<25} | {pred_f:<25} {match}")
                if model_f == pred_f:
                    matches += 1
            
            if matches == len(model_features):
                print(f"✅ Minden jellemző megegyezik ({matches}/{len(model_features)})")
            else:
                print(f"❌ Csak {matches}/{len(model_features)} jellemző egyezik meg")
        else:
            print(f"❌ Jellemzők száma eltér: modell={len(model_features)}, előrejelzés={len(prediction_features)}")
        
    except Exception as e:
        print(f"❌ Hiba az előrejelzési függvény tesztelésénél: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # 4. Test predictions with different inputs
    print(f"\n4. ELŐREJELZÉSEK KÜLÖNBÖZŐ BEMENETEKKEL:")
    print("-" * 40)
    
    test_cases = [
        # (temp, rain, marketing, description)
        (20, 0, 300, "Alap eset"),
        (5, 0, 300, "Hideg"),
        (35, 0, 300, "Meleg"),
        (20, 10, 300, "Esős"),
        (20, 0, 100, "Alacsony marketing"),
        (20, 0, 800, "Magas marketing"),
    ]
    
    avg_visitors = 10974  # From training data
    
    for temp, rain, marketing, desc in test_cases:
        try:
            # Weekend test
            weekend_features = create_prediction_features(
                datetime(2024, 6, 15), temp, rain, False, False, marketing, scaler
            )
            
            # Reorder features to match model expectations
            if len(model_features) == len(weekend_features.columns):
                weekend_features_ordered = weekend_features[model_features]
            else:
                weekend_features_ordered = weekend_features
            
            weekend_pred = model.predict(weekend_features_ordered)[0]
            weekend_diff = (weekend_pred - avg_visitors) / avg_visitors * 100
            
            # Weekday test
            weekday_features = create_prediction_features(
                datetime(2024, 6, 17), temp, rain, False, False, marketing, scaler
            )
            
            if len(model_features) == len(weekday_features.columns):
                weekday_features_ordered = weekday_features[model_features]
            else:
                weekday_features_ordered = weekday_features
            
            weekday_pred = model.predict(weekday_features_ordered)[0]
            weekday_diff = (weekday_pred - avg_visitors) / avg_visitors * 100
            
            print(f"{desc:<20}: Hétvége {weekend_pred:6,.0f} ({weekend_diff:+5.1f}%) | Hétköznap {weekday_pred:6,.0f} ({weekday_diff:+5.1f}%)")
            
        except Exception as e:
            print(f"{desc:<20}: ❌ Hiba: {e}")
    
    # 5. Check feature values
    print(f"\n5. JELLEMZŐ ÉRTÉKEK ELLENŐRZÉSE:")
    print("-" * 40)
    
    try:
        # Create features without scaler
        raw_features = create_prediction_features(
            datetime(2024, 6, 15), 20, 0, False, False, 300, None
        )
        
        # Create features with scaler
        scaled_features = create_prediction_features(
            datetime(2024, 6, 15), 20, 0, False, False, 300, scaler
        )
        
        print("Első 10 jellemző értékei:")
        print(f"{'Jellemző':<25} {'Nyers':<12} {'Skálázott':<12}")
        print("-" * 50)
        
        for i, col in enumerate(raw_features.columns[:10]):
            raw_val = raw_features[col].iloc[0]
            scaled_val = scaled_features[col].iloc[0]
            print(f"{col:<25} {raw_val:<12.3f} {scaled_val:<12.3f}")
        
    except Exception as e:
        print(f"❌ Hiba a jellemző értékek ellenőrzésénél: {e}")
    
    # 6. Check if the issue is in lag features
    print(f"\n6. LAG JELLEMZŐK ELLENŐRZÉSE:")
    print("-" * 40)
    
    print("A lag jellemzők fix értékekkel vannak beállítva:")
    print("- latogatoszam_lag1 = 10974 (átlag)")
    print("- latogatoszam_7d_avg = 10974 (átlag)")
    print("- atlaghomerseklet_lag1 = aktuális hőmérséklet")
    print("- atlaghomerseklet_7d_avg = aktuális hőmérséklet")
    print("")
    print("Ez lehet a probléma oka! A modell túlságosan támaszkodik")
    print("a lag jellemzőkre, amelyek mindig ugyanazok.")

if __name__ == "__main__":
    diagnose_prediction_issue()

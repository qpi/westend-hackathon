import pandas as pd
import numpy as np
from datetime import datetime
import sys
import os

# Add src to path
sys.path.append('src')

from data_preparation import DataPreparation

def debug_features():
    """Debug function to see what features are created during training vs prediction"""
    
    print("🔍 JELLEMZŐK DEBUG ANALÍZIS")
    print("="*50)
    
    # 1. Betanítási jellemzők
    print("\n1. BETANÍTÁSI JELLEMZŐK:")
    print("-" * 30)
    
    try:
        data_prep = DataPreparation()
        X_train, X_test, y_train, y_test, feature_names, summary = data_prep.full_pipeline()
        
        print(f"Betanítási jellemzők száma: {len(feature_names)}")
        print("Jellemzők listája:")
        for i, feature in enumerate(feature_names):
            print(f"  {i+1:2d}. {feature}")
            
    except Exception as e:
        print(f"❌ Hiba a betanítási jellemzők betöltésekor: {e}")
        return
    
    # 2. Előrejelzési jellemzők
    print(f"\n2. ELŐREJELZÉSI JELLEMZŐK:")
    print("-" * 30)
    
    # Import the prediction function
    sys.path.append('web_app')
    from streamlit_app import create_prediction_features
    
    # Test with sample data
    test_date = datetime(2024, 6, 15)  # Saturday
    test_features = create_prediction_features(
        date=test_date,
        temperature=20,
        rainfall=0.5,
        is_holiday=False,
        is_school_break=False,
        marketing_spend=400
    )
    
    prediction_features = list(test_features.columns)
    print(f"Előrejelzési jellemzők száma: {len(prediction_features)}")
    print("Jellemzők listája:")
    for i, feature in enumerate(prediction_features):
        print(f"  {i+1:2d}. {feature}")
    
    # 3. Összehasonlítás
    print(f"\n3. ÖSSZEHASONLÍTÁS:")
    print("-" * 30)
    
    training_set = set(feature_names)
    prediction_set = set(prediction_features)
    
    missing_in_prediction = training_set - prediction_set
    extra_in_prediction = prediction_set - training_set
    
    if missing_in_prediction:
        print(f"❌ Hiányzó jellemzők az előrejelzésből ({len(missing_in_prediction)}):")
        for feature in sorted(missing_in_prediction):
            print(f"  - {feature}")
    
    if extra_in_prediction:
        print(f"⚠️ Extra jellemzők az előrejelzésben ({len(extra_in_prediction)}):")
        for feature in sorted(extra_in_prediction):
            print(f"  + {feature}")
    
    if not missing_in_prediction and not extra_in_prediction:
        print("✅ Minden jellemző megegyezik!")
    
    # 4. Jellemzők sorrendje
    print(f"\n4. JELLEMZŐK SORRENDJE:")
    print("-" * 30)
    
    if len(feature_names) == len(prediction_features):
        order_matches = all(f1 == f2 for f1, f2 in zip(feature_names, prediction_features))
        if order_matches:
            print("✅ A jellemzők sorrendje megegyezik!")
        else:
            print("❌ A jellemzők sorrendje eltér!")
            print("Betanítási sorrend vs Előrejelzési sorrend:")
            for i, (train_f, pred_f) in enumerate(zip(feature_names, prediction_features)):
                match = "✅" if train_f == pred_f else "❌"
                print(f"  {i+1:2d}. {train_f:<25} | {pred_f:<25} {match}")
    
    # 5. Sample prediction test
    print(f"\n5. TESZT ELŐREJELZÉS:")
    print("-" * 30)
    
    try:
        import joblib
        model = joblib.load('models/best_model_random_forest.joblib')
        
        # Reorder features to match training order
        if len(feature_names) == len(prediction_features):
            test_features_ordered = test_features[feature_names]
            prediction = model.predict(test_features_ordered)[0]
            print(f"✅ Teszt előrejelzés: {prediction:,.0f} fő")
            
            # Test with different values
            print("\nTeszt különböző értékekkel:")
            
            test_cases = [
                (datetime(2024, 6, 15), 10, 0, False, False, 200),  # Cold weekend
                (datetime(2024, 6, 15), 25, 0, False, False, 600),  # Warm weekend, high marketing
                (datetime(2024, 6, 17), 20, 0, False, False, 400),  # Monday
            ]
            
            for i, (date, temp, rain, holiday, school, marketing) in enumerate(test_cases):
                features = create_prediction_features(date, temp, rain, holiday, school, marketing)
                features_ordered = features[feature_names]
                pred = model.predict(features_ordered)[0]
                day_name = date.strftime("%A")
                print(f"  {i+1}. {day_name}, {temp}°C, {marketing}€ marketing: {pred:,.0f} fő")
        else:
            print("❌ Nem lehet előrejelzést készíteni, a jellemzők száma eltér!")
            
    except Exception as e:
        print(f"❌ Hiba az előrejelzés tesztelésekor: {e}")

if __name__ == "__main__":
    debug_features()

import joblib
import pandas as pd
import numpy as np

def inspect_model():
    """Inspect the trained model to understand its expected features"""
    
    print("🔍 MODELL VIZSGÁLAT")
    print("="*50)
    
    try:
        # Load the model
        model = joblib.load('models/best_model_random_forest.joblib')
        print("✅ Modell betöltve")
        print(f"Modell típus: {type(model).__name__}")
        
        # Check if model has feature names
        if hasattr(model, 'feature_names_in_'):
            print(f"\n📋 Modell által várt jellemzők ({len(model.feature_names_in_)}):")
            for i, feature in enumerate(model.feature_names_in_):
                print(f"  {i+1:2d}. {feature}")
        else:
            print("\n⚠️ A modell nem tartalmazza a jellemző neveket")
            
        # Check number of features expected
        if hasattr(model, 'n_features_in_'):
            print(f"\n📊 Várt jellemzők száma: {model.n_features_in_}")
        
        # Try to get feature importances
        if hasattr(model, 'feature_importances_'):
            print(f"\n🎯 Top 10 legfontosabb jellemző:")
            if hasattr(model, 'feature_names_in_'):
                feature_importance = list(zip(model.feature_names_in_, model.feature_importances_))
                feature_importance.sort(key=lambda x: x[1], reverse=True)
                for i, (feature, importance) in enumerate(feature_importance[:10]):
                    print(f"  {i+1:2d}. {feature:<25}: {importance:.4f}")
            else:
                importances = model.feature_importances_
                sorted_indices = np.argsort(importances)[::-1]
                for i in range(min(10, len(importances))):
                    idx = sorted_indices[i]
                    print(f"  {i+1:2d}. Feature_{idx:<20}: {importances[idx]:.4f}")
        
    except Exception as e:
        print(f"❌ Hiba a modell betöltésekor: {e}")
        return
    
    # Load training data to see original features
    print(f"\n📊 EREDETI ADATOK VIZSGÁLATA")
    print("-" * 50)
    
    try:
        df = pd.read_csv('data/hackathon_data.csv')
        print(f"✅ Adatok betöltve: {len(df)} sor, {len(df.columns)} oszlop")
        print(f"Eredeti oszlopok:")
        for i, col in enumerate(df.columns):
            print(f"  {i+1:2d}. {col}")
            
        # Show sample data
        print(f"\nMinta adatok (első 3 sor):")
        print(df.head(3).to_string())
        
    except Exception as e:
        print(f"❌ Hiba az adatok betöltésekor: {e}")

if __name__ == "__main__":
    inspect_model()

#!/usr/bin/env python3
"""
Modell újragenerálása a scaler mentésével
"""

import sys
import os

# Add src to path
sys.path.append('src')

from data_preparation import DataPreparation
from machine_learning_models import MLModels

def regenerate_model():
    """Regenerate model with scaler saving"""
    
    print("🔄 MODELL ÚJRAGENERÁLÁSA")
    print("="*50)
    
    try:
        # 1. Adat előkészítés
        print("\n📊 1. LÉPÉS: ADAT ELŐKÉSZÍTÉS")
        print("-" * 40)
        
        data_prep = DataPreparation()
        X_train, X_test, y_train, y_test, feature_names, summary = data_prep.full_pipeline()
        
        print(f"✅ Adat előkészítés befejezve")
        print(f"   - Train minták: {len(X_train):,}")
        print(f"   - Test minták: {len(X_test):,}")
        print(f"   - Jellemzők: {len(feature_names)}")
        
        # 2. Modell betanítás
        print(f"\n🤖 2. LÉPÉS: MODELL BETANÍTÁS")
        print("-" * 40)
        
        ml_models = MLModels()
        ml_models.initialize_models()
        ml_models.train_models(X_train, y_train)
        
        print(f"✅ {len(ml_models.trained_models)} modell betanítva")
        
        # 3. Modell értékelés
        print(f"\n📊 3. LÉPÉS: MODELL ÉRTÉKELÉS")
        print("-" * 40)
        
        ml_models.evaluate_models(X_train, y_train, X_test, y_test)
        ml_models.get_feature_importance(feature_names)
        
        # 4. Eredmények és legjobb modell
        print(f"\n🏆 4. LÉPÉS: EREDMÉNYEK")
        print("-" * 40)
        
        best_model_name = ml_models.print_results_summary()
        
        # 5. Modellek mentése (scaler-rel együtt)
        print(f"\n💾 5. LÉPÉS: MODELLEK MENTÉSE")
        print("-" * 40)
        
        ml_models.save_models(best_model_name, data_prep)
        
        # 6. Összefoglaló
        print(f"\n🎯 MODELL ÚJRAGENERÁLÁS BEFEJEZVE!")
        print("=" * 60)
        print(f"🏆 Legjobb modell: {best_model_name}")
        print(f"📁 Modell fájl: models/best_model_{best_model_name.replace(' ', '_').lower()}.joblib")
        print(f"🔧 Scaler fájl: models/scaler.joblib")
        print(f"📊 Eredmények: outputs/model_results.csv")
        
        return True
        
    except Exception as e:
        print(f"❌ Hiba a modell újragenerálása során: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = regenerate_model()
    if success:
        print("\n✅ Sikeres befejezés!")
    else:
        print("\n❌ Hiba történt!")
        sys.exit(1)

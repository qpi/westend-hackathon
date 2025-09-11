"""
Westend Hackathon - Modell Létrehozó Script
==========================================

Ez a script felelős a bevásárlóközpont látogatószám előrejelző modell
teljes létrehozásáért, betanításáért és mentéséért.

Használat:
    python create_model.py

Kimenet:
    - models/best_model_random_forest.joblib
    - outputs/model_results.csv
    - outputs/*.png (vizualizációk)
"""

import sys
import os
from datetime import datetime

# Saját modulok importálása
sys.path.append('src')
from data_preparation import DataPreparation
from machine_learning_models import MLModels

def main():
    """
    Fő modell létrehozási folyamat
    """
    print("🚀 WESTEND HACKATHON - MODELL LÉTREHOZÁS")
    print("=" * 60)
    print(f"⏰ Indítás: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    try:
        # 1. Adat előkészítés
        print("📊 1. LÉPÉS: ADAT ELŐKÉSZÍTÉS")
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
        
        # 5. Vizualizációk
        print(f"\n📈 5. LÉPÉS: VIZUALIZÁCIÓK")
        print("-" * 40)
        
        ml_models.create_visualizations(y_test, feature_names)
        
        # 6. Modellek mentése
        print(f"\n💾 6. LÉPÉS: MODELLEK MENTÉSE")
        print("-" * 40)
        
        ml_models.save_models(best_model_name)
        
        # 7. Összefoglaló
        print(f"\n🎯 MODELL LÉTREHOZÁS BEFEJEZVE!")
        print("=" * 60)
        print(f"🏆 Legjobb modell: {best_model_name}")
        print(f"📁 Modell fájl: models/best_model_{best_model_name.replace(' ', '_').lower()}.joblib")
        print(f"📊 Eredmények: outputs/model_results.csv")
        print(f"📈 Vizualizációk: outputs/*.png")
        print(f"⏰ Befejezés: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # 8. Gyors validáció
        print(f"\n✅ GYORS VALIDÁCIÓ")
        print("-" * 30)
        
        best_results = ml_models.results[best_model_name]
        print(f"Test R²: {best_results['test_r2']:.4f}")
        print(f"Test RMSE: {best_results['test_rmse']:.0f} fő")
        print(f"Test MAPE: {best_results['test_mape']:.2f}%")
        
        if best_results['test_r2'] > 0.8:
            print("🎉 Kiváló modell teljesítmény!")
        elif best_results['test_r2'] > 0.7:
            print("✅ Jó modell teljesítmény!")
        else:
            print("⚠️ Modell teljesítmény javítható!")
            
        return True
        
    except Exception as e:
        print(f"\n❌ HIBA A MODELL LÉTREHOZÁS SORÁN:")
        print(f"   {str(e)}")
        print(f"\n🔧 JAVASOLT MEGOLDÁSOK:")
        print("   1. Ellenőrizze a data/hackathon_data.csv fájl létezését")
        print("   2. Futtassa: python src/data_preparation.py")
        print("   3. Ellenőrizze a szükséges könyvtárak telepítését")
        return False

def quick_demo():
    """
    Gyors demo az elkészült modellel
    """
    print(f"\n🔮 GYORS DEMO - ELŐREJELZÉS")
    print("-" * 40)
    
    try:
        # Modell betöltése
        import joblib
        model = joblib.load('models/best_model_random_forest.joblib')
        
        # Demo előrejelzés (egyszerűsített)
        # Normál hétköznap: 15°C, 0mm eső, 300 EUR marketing
        demo_features = np.zeros(43)  # 43 jellemző (a tényleges modellből)
        demo_features[0] = 15  # hőmérséklet
        demo_features[1] = 0   # csapadék
        demo_features[4] = 300 # marketing
        
        prediction = model.predict([demo_features])[0]
        print(f"Demo előrejelzés: {prediction:,.0f} fő")
        print("✅ Modell működik!")
        
    except Exception as e:
        print(f"⚠️ Demo nem futtatható: {str(e)}")

if __name__ == "__main__":
    print("🎯 Westend Hackathon - Modell Létrehozás")
    print("Futtassa ezt a scriptet a teljes modell pipeline létrehozásához!\n")
    
    success = main()
    
    if success:
        print(f"\n🚀 KÖVETKEZŐ LÉPÉSEK:")
        print("   1. Streamlit app indítása: streamlit run web_app/streamlit_app_standalone.py")
        print("   2. Jupyter notebook megnyitása: notebooks/hackathon_demo.ipynb")
        print("   3. Prezentáció előkészítése a demo script alapján")
        
        # Gyors demo futtatása
        quick_demo()
    else:
        print(f"\n🔧 Kérjük javítsa a hibákat és próbálja újra!")

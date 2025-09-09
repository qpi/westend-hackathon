"""
Westend Hackathon - Gyors Teszt
===============================

Teszteli, hogy minden modul és fájl megfelelően működik-e.
"""

import os
import sys
import pandas as pd

def test_project():
    print("🧪 WESTEND HACKATHON PROJEKT TESZT")
    print("="*50)
    
    # 1. Fájlok ellenőrzése
    print("\n📁 Fájlok ellenőrzése...")
    required_files = [
        'data/hackathon_data.csv',
        'models/best_model_random_forest.joblib',
        'src/data_preparation.py',
        'src/machine_learning_models.py',
        'web_app/streamlit_app.py',
        'outputs/model_results.csv'
    ]
    
    all_files_exist = True
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - HIÁNYZIK!")
            all_files_exist = False
    
    # 2. Adatok ellenőrzése
    print("\n📊 Adatok ellenőrzése...")
    try:
        df = pd.read_csv('data/hackathon_data.csv')
        print(f"✅ hackathon_data.csv betöltve: {len(df)} sor, {len(df.columns)} oszlop")
        print(f"   Dátum tartomány: {df['datum'].min()} - {df['datum'].max()}")
        print(f"   Átlagos látogatószám: {df['latogatoszam'].mean():,.0f}")
    except Exception as e:
        print(f"❌ Adatbetöltési hiba: {e}")
        all_files_exist = False
    
    # 3. Modell ellenőrzése
    print("\n🤖 Modell ellenőrzése...")
    try:
        import joblib
        model = joblib.load('models/best_model_random_forest.joblib')
        print("✅ Random Forest modell betöltve")
    except Exception as e:
        print(f"❌ Modell betöltési hiba: {e}")
        all_files_exist = False
    
    # 4. Modulok ellenőrzése
    print("\n🔧 Python modulok ellenőrzése...")
    try:
        sys.path.insert(0, 'src')
        import data_preparation
        import machine_learning_models
        print("✅ data_preparation.py modul")
        print("✅ machine_learning_models.py modul")
    except Exception as e:
        print(f"❌ Modul import hiba: {e}")
        all_files_exist = False
    
    # 5. Eredmények ellenőrzése
    print("\n📈 Eredmények ellenőrzése...")
    try:
        results = pd.read_csv('outputs/model_results.csv')
        print(f"✅ model_results.csv: {len(results)} modell eredmény")
        
        # Legjobb modell keresése
        best_model_idx = results['test_r2'].idxmax()
        best_model = results.loc[best_model_idx]
        print(f"🏆 Legjobb modell: {best_model.iloc[0]}")
        print(f"   R² score: {best_model['test_r2']:.4f}")
        print(f"   MAE: {best_model['test_mae']:.0f}")
        
    except Exception as e:
        print(f"❌ Eredmények betöltési hiba: {e}")
        all_files_exist = False
    
    # Összefoglaló
    print("\n" + "="*50)
    if all_files_exist:
        print("🎉 PROJEKT TESZT SIKERES!")
        print("✅ Minden komponens működőképes")
        print("🚀 A Streamlit alkalmazás indítható")
        print("\n📝 Indítási parancsok:")
        print("   python -m streamlit run web_app/streamlit_app.py")
        print("   vagy")
        print("   python run_app.py")
    else:
        print("❌ PROJEKT TESZT SIKERTELEN!")
        print("🔧 Javítsa ki a hibákat és futtassa újra a tesztet")
    
    print("="*50)
    return all_files_exist

if __name__ == "__main__":
    test_project()

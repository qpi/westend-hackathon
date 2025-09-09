"""
Westend Hackathon - Web App Launcher
===================================

Egyszerű launcher script a Streamlit alkalmazás indításához.
"""

import subprocess
import sys
import os

def main():
    print("🚀 Westend Látogatószám Előrejelző Web App indítása...")
    print("="*50)
    
    # Ellenőrizzük, hogy minden szükséges fájl létezik
    required_files = [
        'data/hackathon_data.csv',
        'models/best_model_random_forest.joblib',
        'web_app/streamlit_app.py'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print("❌ Hiányzó fájlok:")
        for file_path in missing_files:
            print(f"   - {file_path}")
        print("\n🔧 Futtassa előbb a következő scripteket:")
        print("   1. python src/data_preparation.py")
        print("   2. python src/machine_learning_models.py")
        return
    
    print("✅ Minden szükséges fájl megvan!")
    print("\n🌐 Streamlit alkalmazás indítása...")
    print("📍 URL: http://localhost:8501")
    print("\n⚠️  A böngésző automatikusan megnyílik.")
    print("🛑 Az alkalmazás leállításához nyomja meg a Ctrl+C billentyűkombinációt.")
    print("="*50)
    
    try:
        # Streamlit alkalmazás indítása
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            "web_app/streamlit_app_standalone.py",
            "--server.address", "localhost",
            "--server.port", "8501",
            "--browser.gatherUsageStats", "false"
        ])
    except KeyboardInterrupt:
        print("\n\n🛑 Alkalmazás leállítva.")
    except Exception as e:
        print(f"\n❌ Hiba történt: {e}")

if __name__ == "__main__":
    main()

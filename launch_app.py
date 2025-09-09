"""
Westend Hackathon - Automatikus App Launcher
============================================

Automatikusan telepíti a szükséges csomagokat és elindítja az alkalmazást.
"""

import subprocess
import sys
import os
import time

def install_package(package):
    """Csomag telepítése pip-pel"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        return True
    except subprocess.CalledProcessError:
        return False

def check_and_install_requirements():
    """Szükséges csomagok ellenőrzése és telepítése"""
    print("🔧 Szükséges csomagok ellenőrzése...")
    
    required_packages = {
        'pandas': 'pandas>=1.3.0',
        'sklearn': 'scikit-learn>=1.0.0',
        'matplotlib': 'matplotlib>=3.3.0',
        'seaborn': 'seaborn>=0.11.0',
        'numpy': 'numpy>=1.20.0',
        'joblib': 'joblib>=1.0.0',
        'openpyxl': 'openpyxl>=3.0.0',
        'streamlit': 'streamlit>=1.0.0',
        'plotly': 'plotly>=5.0.0',
        'statsmodels': 'statsmodels>=0.14.0'
    }
    
    missing_packages = []
    
    for package_name, package_spec in required_packages.items():
        try:
            __import__(package_name)
            print(f"✅ {package_name}")
        except ImportError:
            print(f"❌ {package_name} - hiányzik")
            missing_packages.append(package_spec)
    
    if missing_packages:
        print(f"\n📦 {len(missing_packages)} csomag telepítése...")
        for package in missing_packages:
            print(f"🔄 Telepítés: {package}")
            if install_package(package):
                print(f"✅ Telepítve: {package}")
            else:
                print(f"❌ Hiba: {package}")
                return False
    
    return True

def find_available_port(start_port=8501, max_attempts=10):
    """Szabad port keresése"""
    import socket
    
    for port in range(start_port, start_port + max_attempts):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('localhost', port))
                return port
        except OSError:
            continue
    return None

def main():
    print("🚀 WESTEND HACKATHON APP LAUNCHER")
    print("="*50)
    
    # 1. Csomagok ellenőrzése
    if not check_and_install_requirements():
        print("❌ Csomag telepítési hiba!")
        return
    
    # 2. Fájlok ellenőrzése
    print("\n📁 Fájlok ellenőrzése...")
    required_files = [
        'data/hackathon_data.csv',
        'models/best_model_random_forest.joblib',
        'web_app/streamlit_app_standalone.py'
    ]
    
    missing_files = []
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path}")
            missing_files.append(file_path)
    
    if missing_files:
        print("❌ Hiányzó fájlok! Futtassa előbb:")
        print("   python src/data_preparation.py")
        print("   python src/machine_learning_models.py")
        return
    
    # 3. Port keresése
    port = find_available_port()
    if not port:
        print("❌ Nem található szabad port!")
        return
    
    print(f"\n🌐 Streamlit alkalmazás indítása porton: {port}")
    print(f"📍 URL: http://localhost:{port}")
    print("\n⚠️  A böngésző automatikusan megnyílik.")
    print("🛑 Leállításhoz: Ctrl+C")
    print("="*50)
    
    try:
        # Streamlit alkalmazás indítása
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            "web_app/streamlit_app_standalone.py",
            "--server.address", "localhost",
            "--server.port", str(port),
            "--browser.gatherUsageStats", "false",
            "--server.headless", "false"
        ])
    except KeyboardInterrupt:
        print("\n\n🛑 Alkalmazás leállítva.")
    except Exception as e:
        print(f"\n❌ Hiba: {e}")
        print("\nPróbálja manuálisan:")
        print(f"python -m streamlit run web_app/streamlit_app_standalone.py --server.port {port}")

if __name__ == "__main__":
    main()

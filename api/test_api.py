"""
API Tesztelő Script
==================

Egyszerű tesztek az API működésének ellenőrzésére.
"""

import requests
import json
from datetime import datetime, timedelta

def test_prediction():
    """Teszteli az előrejelzés endpointot"""
    
    url = "http://localhost:5000/api/predict"
    
    # Teszt esetek
    test_cases = [
        {
            "name": "Átlagos hétköznap",
            "data": {
                "date": "2024-09-18",  # Szerda
                "temperature": 18.0,
                "rainfall": 0.0,
                "is_holiday": False,
                "is_school_break": False,
                "marketing_spend": 300
            }
        },
        {
            "name": "Esős hétvége",
            "data": {
                "date": "2024-09-21",  # Szombat
                "temperature": 15.0,
                "rainfall": 8.0,
                "is_holiday": False,
                "is_school_break": False,
                "marketing_spend": 400
            }
        },
        {
            "name": "Karácsonyi ünnep",
            "data": {
                "date": "2024-12-25",  # Karácsony
                "temperature": -2.0,
                "rainfall": 2.0,
                "is_holiday": True,
                "is_school_break": True,
                "marketing_spend": 800
            }
        },
        {
            "name": "Nyári szünet, meleg nap",
            "data": {
                "date": "2024-07-15",  # Nyári szünet
                "temperature": 32.0,
                "rainfall": 0.0,
                "is_holiday": False,
                "is_school_break": True,
                "marketing_spend": 500
            }
        }
    ]
    
    print("=" * 80)
    print("🧪 API TESZTELÉS")
    print("=" * 80)
    
    for test in test_cases:
        print(f"\n📍 Teszt: {test['name']}")
        print("-" * 40)
        
        try:
            # API hívás
            response = requests.post(url, json=test['data'])
            
            if response.status_code == 200:
                result = response.json()
                
                print(f"✅ Sikeres előrejelzés!")
                print(f"   📅 Dátum: {test['data']['date']}")
                print(f"   🌡️  Hőmérséklet: {test['data']['temperature']}°C")
                print(f"   🌧️  Csapadék: {test['data']['rainfall']}mm")
                print(f"   👥 Előrejelzés: {result['prediction']:,} látogató")
                print(f"   📊 Változás az átlaghoz képest: {result['explanation']['percentage_change']:+.1f}%")
                print(f"   📝 Fő tényezők:")
                for factor in result['explanation']['main_factors'][:3]:
                    print(f"      • {factor}")
                    
                # Részletes hatások
                print(f"   💡 Hatások részletesen:")
                for name, impact in result['explanation']['impacts'].items():
                    if impact['impact_percent'] != 0:
                        print(f"      {name}: {impact['impact_percent']:+d}% - {impact['description']}")
                
            else:
                print(f"❌ Hiba: HTTP {response.status_code}")
                print(f"   {response.text}")
                
        except requests.exceptions.ConnectionError:
            print("❌ Nem lehet csatlakozni az API-hoz.")
            print("   Indítsa el az API-t: python api/prediction_api.py")
            return
        except Exception as e:
            print(f"❌ Hiba: {str(e)}")
    
    print("\n" + "=" * 80)
    print("✅ Tesztelés befejezve!")
    print("=" * 80)

def test_health():
    """Teszteli a health check endpointot"""
    
    try:
        response = requests.get("http://localhost:5000/api/health")
        if response.status_code == 200:
            result = response.json()
            print("\n🏥 Health Check:")
            print(f"   Status: {result['status']}")
            print(f"   Model loaded: {result['model_loaded']}")
            print(f"   Scaler loaded: {result['scaler_loaded']}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except:
        print("❌ API nem elérhető")

def test_features():
    """Teszteli a features endpointot"""
    
    try:
        response = requests.get("http://localhost:5000/api/features")
        if response.status_code == 200:
            result = response.json()
            print("\n📋 Használt jellemzők:")
            print(f"   Összes jellemző: {result['total_features']}")
            print(f"   Első 5 jellemző: {result['features'][:5]}")
        else:
            print(f"❌ Features endpoint failed: {response.status_code}")
    except:
        print("❌ API nem elérhető")

if __name__ == "__main__":
    print("\n🚀 Westend API Tesztelő\n")
    
    # Health check
    test_health()
    
    # Features check
    test_features()
    
    # Prediction tests
    test_prediction()

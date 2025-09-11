"""
Egyszerű példa az API használatára
===================================

Ez a script bemutatja, hogy hogyan lehet megtudni, miért annyi a látogatószám.
"""

import json

def explain_prediction_example():
    """
    Példa arra, hogy az API hogyan magyarázza meg a látogatószámot
    """
    
    # Példa API válasz (ezt adná vissza az API)
    api_response = {
        "prediction": 15234,
        "explanation": {
            "base_visitors": 10974,
            "difference": 4260,
            "percentage_change": 38.8,
            "impacts": {
                "Nap típusa": {
                    "description": "Hétvége (szombat)",
                    "impact_percent": 40,
                    "impact_visitors": 4389
                },
                "Ünnepnap": {
                    "description": "Karácsonyi ünnep",
                    "impact_percent": 60,
                    "impact_visitors": 6584
                },
                "Hőmérséklet": {
                    "description": "Hideg idő (2°C)",
                    "impact_percent": -30,
                    "impact_visitors": -3292
                },
                "Csapadék": {
                    "description": "Enyhe havazás (3mm)",
                    "impact_percent": -15,
                    "impact_visitors": -1646
                },
                "Marketing": {
                    "description": "Magas marketing költés (800 EUR)",
                    "impact_percent": 15,
                    "impact_visitors": 1646
                }
            },
            "main_factors": [
                "Karácsonyi ünnep (+60%)",
                "Hétvége (+40%)",
                "Hideg idő (-30%)"
            ],
            "detailed_explanation": """
            A december 24-re (szenteste) előrejelzett látogatószám 15,234 fő.
            
            Ez 38.8%-kal magasabb az átlagos 10,974 főnél.
            
            MIÉRT ENNYI?
            
            Pozitív hatások:
            • Karácsonyi ünnep: +60% (utolsó pillanatos ajándékvásárlás)
            • Hétvége: +40% (több szabadidő)
            • Magas marketing: +15% (ünnepi kampányok)
            
            Negatív hatások:
            • Hideg idő (2°C): -30% (kényelmetlen közlekedés)
            • Enyhe havazás: -15% (csúszós utak)
            
            Összességében a pozitív hatások erősebbek, ezért várhatóan 
            átlag feletti lesz a látogatottság a rossz idő ellenére is.
            """
        }
    }
    
    print("=" * 80)
    print("🎯 MIÉRT ANNYI A LÁTOGATÓSZÁM? - API MAGYARÁZAT")
    print("=" * 80)
    
    # Alapinformációk
    print(f"\n📅 Dátum: 2024-12-24 (Szenteste)")
    print(f"👥 Előrejelzett látogatószám: {api_response['prediction']:,} fő")
    print(f"📊 Átlaghoz képest: {api_response['explanation']['percentage_change']:+.1f}%")
    
    # Részletes magyarázat
    print("\n🔍 RÉSZLETES MAGYARÁZAT:")
    print("-" * 40)
    
    print("\n📈 Pozitív tényezők (növelik a látogatószámot):")
    for factor, details in api_response['explanation']['impacts'].items():
        if details['impact_percent'] > 0:
            print(f"   ✅ {factor}: {details['impact_percent']:+d}%")
            print(f"      → {details['description']}")
            print(f"      → Hatás: {details['impact_visitors']:+,} látogató")
    
    print("\n📉 Negatív tényezők (csökkentik a látogatószámot):")
    for factor, details in api_response['explanation']['impacts'].items():
        if details['impact_percent'] < 0:
            print(f"   ⚠️ {factor}: {details['impact_percent']:+d}%")
            print(f"      → {details['description']}")
            print(f"      → Hatás: {details['impact_visitors']:+,} látogató")
    
    print("\n💡 ÖSSZEFOGLALÁS:")
    print("-" * 40)
    print(api_response['explanation']['detailed_explanation'])
    
    # Döntési javaslatok
    print("\n🎯 INTÉZKEDÉSI JAVASLATOK:")
    print("-" * 40)
    
    if api_response['prediction'] > api_response['explanation']['base_visitors'] * 1.3:
        print("⚡ MAGAS FORGALOM VÁRHATÓ!")
        print("   • Növelje a személyzet létszámát")
        print("   • Készítsen fel extra készleteket")
        print("   • Nyisson meg minden pénztárat")
        print("   • Fokozott biztonsági készültség")
    elif api_response['prediction'] < api_response['explanation']['base_visitors'] * 0.7:
        print("📉 ALACSONY FORGALOM VÁRHATÓ")
        print("   • Csökkentett létszám elegendő")
        print("   • Energiatakarékos üzemmód")
        print("   • Promóciók a forgalom növelésére")
    else:
        print("📊 ÁTLAGOS FORGALOM VÁRHATÓ")
        print("   • Normál működési rend")
        print("   • Szokásos személyzet")
    
    print("\n" + "=" * 80)
    print("✅ Ez így működik az API - pontosan megmondja, miért annyi a látogatószám!")
    print("=" * 80)

if __name__ == "__main__":
    explain_prediction_example()
    
    print("\n📌 HASZNÁLAT MISI SZÁMÁRA:")
    print("-" * 40)
    print("""
    1. Indítsd el az API-t:
       python api/prediction_api.py
    
    2. Hívd meg az endpointot:
       POST http://localhost:5000/api/predict
       {
           "date": "2024-12-24",
           "temperature": 2.0,
           "rainfall": 3.0,
           "is_holiday": true,
           "is_school_break": true,
           "marketing_spend": 800
       }
    
    3. Az API visszaadja:
       - A várható látogatószámot
       - Minden tényező hatását részletesen
       - Teljes magyarázatot, hogy miért annyi
    
    4. A magyarázat tartalmazza:
       - Mely tényezők növelik/csökkentik a forgalmat
       - Mennyivel térít el az átlagtól
       - Mi a fő ok a változásra
       - Konkrét százalékos hatásokat
    """)

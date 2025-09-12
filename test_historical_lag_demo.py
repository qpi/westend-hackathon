"""
🎯 DEMO: Valódi Historikus Lag Értékek Tesztelése
===============================================

Ez a script bemutatja, hogyan működik az új funkció:
valódi historikus adatokból számított lag értékek.
"""

import pandas as pd
import sys
sys.path.insert(0, 'src')
from data_preparation import DataPreparation

# Adatok betöltése
print("🎯 VALÓDI HISTORIKUS LAG ÉRTÉKEK DEMO")
print("=" * 60)

try:
    # Adatok betöltése
    data_prep = DataPreparation()
    df = data_prep.load_and_clean_data('data/hackathon_data.csv')
    df = data_prep.create_features(df)

    print(f"✅ Adatok betöltve: {len(df)} sor")
    print(f"   Időszak: {df['datum'].min()} - {df['datum'].max()}")

    # Példa dátum: 2024. január 1-je
    test_date = pd.Timestamp('2024-01-01')
    print(f"\n📅 Teszt dátum: {test_date.strftime('%Y-%m-%d')}")

    # Előző napi érték keresése
    prev_date = test_date - pd.Timedelta(days=1)
    print(f"📊 Előző nap: {prev_date.strftime('%Y-%m-%d')}")

    prev_day_data = df[df['datum'] == prev_date]
    if not prev_day_data.empty:
        prev_visitors = prev_day_data['latogatoszam'].values[0]
        prev_temp = prev_day_data['atlaghomerseklet'].values[0]
        print(f"   ✅ Talált adat: {prev_visitors:.0f} fő, {prev_temp:.1f}°C")
    else:
        print("   ⚠️ Nincs adat az előző napra")

    # 7 napos átlag számítása
    week_start = test_date - pd.Timedelta(days=7)
    week_data = df[
        (df['datum'] >= week_start) &
        (df['datum'] < test_date)
    ]

    print(f"📈 7 napos időszak: {week_start.strftime('%Y-%m-%d')} - {(test_date - pd.Timedelta(days=1)).strftime('%Y-%m-%d')}")
    print(f"   Adatok száma: {len(week_data)} nap")

    if len(week_data) > 0:
        week_avg_visitors = week_data['latogatoszam'].mean()
        week_avg_temp = week_data['atlaghomerseklet'].mean()
        print(f"   ✅ 7 napos átlag: {week_avg_visitors:.0f} fő, {week_avg_temp:.1f}°C")

        # Egyéni napok megjelenítése
        print("   📋 Napi bontás:")
        for _, row in week_data.iterrows():
            print(f"      {row['datum'].strftime('%Y-%m-%d')}: {row['latogatoszam']:.0f} fő")
    else:
        print("   ⚠️ Nincs adat a 7 napos időszakban")

    print("\n" + "=" * 60)
    print("🎉 DEMO ÖSSZEFOGLALÓ")
    print("=" * 60)

    if not prev_day_data.empty and len(week_data) > 0:
        print("✅ SIKERES IMPLEMENTÁCIÓ!")
        print(f"   - Előző napi érték: {prev_visitors:.0f} fő (nem 10,974!)")
        print(f"   - 7 napos átlag: {week_avg_visitors:.0f} fő (nem 10,974!)")
        print("   - Dinamikus, valódi adatok alapján!")
    else:
        print("⚠️ NEM TELJES AZ ADAT")
        print("   - Hiányzó adatok miatt átlagokat használunk")

    print("\n📋 MŰKÖDÉS:")
    print("   1. Minden predikciókor ki keresi a valódi előző napi értékeket")
    print("   2. Számítja a valódi 7 napos átlagokat")
    print("   3. Ezeket használja a modell bemeneteként")
    print("   4. Így sokkal realisztikusabb eredményeket kapunk!")

except Exception as e:
    print(f"❌ Hiba: {str(e)}")
    print("Ellenőrizd, hogy létezik-e a data/hackathon_data.csv fájl!")

print("\n" + "=" * 60)
print("🚀 PRÓBÁLD KI: streamlit run web_app/streamlit_app.py")
print("=" * 60)

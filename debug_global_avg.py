#!/usr/bin/env python3
"""
Debug Global Average Calculation
================================

Check what the global average actually is.
"""

import pandas as pd
import numpy as np

def debug_global_avg():
    """Debug the global average calculation"""
    print("🔍 GLOBÁLIS ÁTLAG DEBUGGOLÁS")
    print("="*50)
    
    # Load data
    try:
        data_path = 'data/hackathon_data_full.csv' if pd.io.common.file_exists('data/hackathon_data_full.csv') else 'data/hackathon_data.csv'
        data = pd.read_csv(data_path)
        data['datum'] = pd.to_datetime(data['datum'])
        print(f"✅ Adatok betöltve: {data_path}")
        print(f"📊 Sorok száma: {len(data)}")
    except Exception as e:
        print(f"❌ Hiba az adatok betöltésekor: {e}")
        return
    
    # Calculate global average
    global_avg = data['latogatoszam'].mean()
    print(f"\n🌍 Globális átlag: {global_avg:,.2f} fő")
    
    # Show some statistics
    print(f"📈 Maximum: {data['latogatoszam'].max():,.0f} fő")
    print(f"📉 Minimum: {data['latogatoszam'].min():,.0f} fő")
    print(f"📊 Medián: {data['latogatoszam'].median():,.2f} fő")
    print(f"📏 Szórás: {data['latogatoszam'].std():,.2f} fő")
    
    # Test some predictions
    test_predictions = [7000, 8000, 9000, 10000, 11000, 12000, 13000, 14000, 15000]
    
    print(f"\n🧪 TESZT ELŐREJELZÉSEK:")
    print("-" * 50)
    for pred in test_predictions:
        diff = pred - global_avg
        percentage = (diff / global_avg) * 100
        print(f"Előrejelzés: {pred:,} fő → Globális eltérés: {percentage:+.1f}%")
    
    # Check if there's a pattern
    print(f"\n🔍 ADATOK ELLENŐRZÉSE:")
    print(f"Első 5 sor látogatószám:")
    print(data['latogatoszam'].head())
    print(f"\nUtolsó 5 sor látogatószám:")
    print(data['latogatoszam'].tail())
    
    # Check for any weird values
    print(f"\n⚠️ OUTLIER ELLENŐRZÉS:")
    q1 = data['latogatoszam'].quantile(0.25)
    q3 = data['latogatoszam'].quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    
    outliers = data[(data['latogatoszam'] < lower_bound) | (data['latogatoszam'] > upper_bound)]
    print(f"Outlier-ek száma: {len(outliers)}")
    if len(outliers) > 0:
        print("Outlier értékek:")
        print(outliers['latogatoszam'].values)

if __name__ == "__main__":
    debug_global_avg()

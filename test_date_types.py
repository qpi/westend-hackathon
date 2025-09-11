"""
Dátum típusok tesztelése
========================

Ellenőrzi, hogy a dátum típusok helyesen működnek-e.
"""

import pandas as pd
from datetime import datetime

# Szimuláljuk a streamlit dátumot
streamlit_date = datetime(2024, 1, 1).date()
print(f"Streamlit dátum típusa: {type(streamlit_date)}")
print(f"Streamlit dátum: {streamlit_date}")

# Szimuláljuk a pandas dátumot
pandas_date = pd.Timestamp('2023-12-31')
print(f"Pandas dátum típusa: {type(pandas_date)}")
print(f"Pandas dátum: {pandas_date}")

# Konvertálás
streamlit_to_pandas = pd.Timestamp(streamlit_date)
print(f"Konvertált streamlit -> pandas: {streamlit_to_pandas}")
print(f"Konvertált típusa: {type(streamlit_to_pandas)}")

# Összehasonlítás
print(f"Összehasonlítás működik: {pandas_date < streamlit_to_pandas}")

# Teszteljük a timedelta műveleteket
prev_date = streamlit_to_pandas - pd.Timedelta(days=1)
week_start = streamlit_to_pandas - pd.Timedelta(days=7)
print(f"Előző nap: {prev_date}")
print(f"Hét kezdete: {week_start}")

print("\n✅ Dátum típusok helyesen működnek!")

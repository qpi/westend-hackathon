"""
Feature Importance ellenőrzése
==============================

Megnézi, hogy a csapadék mennyire fontos a modell számára.
"""

import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt

# Model betöltése
model = joblib.load('models/best_model_random_forest.joblib')

# Feature nevek betöltése
import sys
sys.path.insert(0, 'src')
from data_preparation import DataPreparation

data_prep = DataPreparation()
df = pd.read_csv('data/hackathon_data.csv')
df['datum'] = pd.to_datetime(df['datum'])
df = data_prep.create_features(df)
df = data_prep.encode_categorical(df)
feature_columns = [col for col in df.columns if col not in ['datum', 'latogatoszam']]

# Feature importance
importances = model.feature_importances_
indices = np.argsort(importances)[::-1]

print("🔍 Feature Importance Elemzés")
print("=" * 60)
print("\nTop 20 legfontosabb jellemző:")
print("-" * 40)

for i in range(min(20, len(indices))):
    idx = indices[i]
    print(f"{i+1:2d}. {feature_columns[idx]:30s}: {importances[idx]*100:6.2f}%")

# Csapadék feature keresése
print("\n🌧️ Csapadék-kapcsolatos jellemzők:")
print("-" * 40)

rain_features = []
for i, feature in enumerate(feature_columns):
    if 'csapadek' in feature.lower() or 'esik' in feature.lower():
        rain_features.append((feature, importances[i]))
        print(f"{feature:30s}: {importances[i]*100:6.2f}% (rang: {list(indices).index(i)+1})")

if not rain_features:
    print("Nincs találat csapadék jellemzőre!")

# Időjárás jellemzők
print("\n🌡️ Időjárás-kapcsolatos jellemzők:")
print("-" * 40)

weather_features = []
for i, feature in enumerate(feature_columns):
    if any(word in feature.lower() for word in ['homerseklet', 'hideg', 'meleg', 'csapadek', 'esik']):
        weather_features.append((feature, importances[i]))
        rank = list(indices).index(i) + 1
        print(f"{feature:30s}: {importances[i]*100:6.2f}% (rang: {rank})")

# Összesített fontosság
total_weather_importance = sum(imp for _, imp in weather_features)
print(f"\nÖsszes időjárás fontosság: {total_weather_importance*100:.2f}%")

# Vizualizáció
plt.figure(figsize=(12, 8))
top_n = 15
top_indices = indices[:top_n]
top_features = [feature_columns[i] for i in top_indices]
top_importances = [importances[i] for i in top_indices]

# Színek - csapadék piros, többi kék
colors = ['red' if 'csapadek' in f.lower() or 'esik' in f.lower() else 'blue' 
          for f in top_features]

plt.barh(range(top_n), top_importances, color=colors)
plt.yticks(range(top_n), top_features)
plt.xlabel('Fontosság (%)')
plt.title('Top 15 Feature Importance (piros = csapadék-kapcsolatos)')
plt.gca().invert_yaxis()

for i, v in enumerate(top_importances):
    plt.text(v + 0.001, i, f'{v*100:.2f}%', va='center')

plt.tight_layout()
plt.savefig('feature_importance_analysis.png', dpi=150, bbox_inches='tight')
plt.show()

print("\n📊 Grafikon mentve: feature_importance_analysis.png")

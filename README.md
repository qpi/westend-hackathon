# 🏬 Westend Hackathon - Látogatószám Előrejelző

## 📋 Projekt Leírása

AI-alapú látogatószám előrejelző rendszer bevásárlóközpontok számára. A rendszer gépi tanulás segítségével előre jelzi a napi látogatószámot különböző tényezők alapján.

## 🎯 Főbb Funkciók

- **🤖 AI Előrejelzés**: Random Forest modell 85.7% pontossággal
- **📊 Interaktív Vizualizációk**: Korrelációs heatmap, időjárás hatása
- **🌐 Web Felület**: Streamlit alapú felhasználóbarát interface
- **📈 Valós idejű Predikció**: Azonnali előrejelzések új adatokkal

## 🚀 Gyors Indítás

### 1. Automatikus Launcher (Ajánlott)
```bash
python launch_app.py
```

### 2. Manuális Indítás
```bash
# Függőségek telepítése
pip install -r requirements.txt

# Alkalmazás indítása
python -m streamlit run web_app/streamlit_app_standalone.py
```

### 3. Alternatív Indítások
```bash
# Eredeti launcher
python run_app.py

# Saját port megadása
python -m streamlit run web_app/streamlit_app_standalone.py --server.port 8504
```

## 📊 Adatok és Modell

### Kulcs Változók
- **Dátum** - Napi bontás (2022-2023)
- **Látogatószám** - Célváltozó (1,000-25,000 fő)
- **Időjárás** - Hőmérséklet, csapadék
- **Naptár** - Ünnepnapok, iskolai szünetek, hétvégék
- **Marketing** - Napi marketing kiadás
- **Szezonalitás** - Évszakok, hónapok

### Modell Teljesítmény
- **Algoritmus**: Random Forest Regressor
- **R² Score**: 0.857 (85.7%)
- **MAE**: 1,300 látogató
- **RMSE**: 1,637 látogató

## 📁 Projekt Struktúra

```
westend-hackathon/
├── 📊 data/
│   └── hackathon_data.csv          # Tréning adatok (730 nap)
├── 🤖 models/
│   └── best_model_random_forest.joblib  # Betanított modell
├── 📈 outputs/
│   ├── model_results.csv           # Modell összehasonlítás
│   ├── predictions_vs_actual.png   # Eredmény grafikonok
│   └── feature_importance.png      # Változó fontosság
├── 💻 src/
│   ├── data_preparation.py         # Adat előkészítés
│   └── machine_learning_models.py  # Modell tanítás
├── 🌐 web_app/
│   ├── streamlit_app.py           # Moduláris app
│   └── streamlit_app_standalone.py # Önálló app
├── 🚀 launch_app.py               # Automatikus launcher
├── 🔧 run_app.py                  # Egyszerű launcher
└── 📋 requirements.txt            # Python függőségek
```

## 🔧 Fejlesztői Információk

### Szükséges Python Csomagok
- `pandas` - Adat manipuláció
- `scikit-learn` - Gépi tanulás
- `streamlit` - Web alkalmazás
- `plotly` - Interaktív grafikonok
- `statsmodels` - Statisztikai modellek
- `joblib` - Modell mentés/betöltés

### Tesztelés
```bash
python test_app.py  # Teljes rendszer teszt
```

### Adatok Újragenerálása
```bash
python src/data_preparation.py      # Új adatok generálása
python src/machine_learning_models.py  # Modell újratanítása
```

## 📈 Használat

### Web Felület Funkciók

1. **🏠 Főoldal**
   - Projekt áttekintés
   - Modell teljesítmény metrikák

2. **🔮 Előrejelzés**
   - Interaktív input mezők
   - Azonnali predikció
   - Eredmény vizualizáció

3. **📊 Vizualizációk**
   - Korrelációs heatmap
   - Időjárás vs látogatószám
   - Szezonális trendek

4. **📋 Adatok**
   - Nyers adatok megtekintése
   - Statisztikák
   - Adatletöltés

## 🎯 Hackathon Eredmények

### ✅ Teljesített Célok
- [x] Működő AI prototípus
- [x] Interaktív web felület
- [x] Valós idejű előrejelzések
- [x] Professzionális vizualizációk
- [x] 85%+ modell pontosság

### 📊 Demonstráció Metrikák
- **Adatok**: 730 nap, 11 változó
- **Pontosság**: 85.7% (R²)
- **Fejlesztési idő**: ~3 óra
- **Technológiák**: Python, Streamlit, Plotly, Scikit-learn

## 🏆 Következő Lépések

### Rövid távú fejlesztések
- [ ] Valós időjárási API integráció
- [ ] Több ML algoritmus összehasonlítása
- [ ] Mobil-barát responsive design

### Hosszú távú lehetőségek
- [ ] Valós bevásárlóközpont adatok
- [ ] Deep Learning modellek
- [ ] Automatikus jelentések
- [ ] Multi-tenant architektúra

---

**Készítette**: Westend Hackathon Team  
**Dátum**: 2025. szeptember 9.  
**Verzió**: 3.0 (Teljes)  
**Licenc**: MIT

🎉 **A projekt 100%-ban kész és demonstrálható!**

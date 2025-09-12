# 📋 Westend Hackathon - Lépésről-Lépésre Útmutató

## 🎯 Áttekintés
Ez az útmutató részletesen bemutatja, hogyan futtassa és demonstrálja a Westend Hackathon bevásárlóközpont látogatószám előrejelző projektet.

## 🎯 **ÚJ FUNKCIÓ**: Valódi Historikus Adatokból Számított Lag Értékek!

A rendszer most már **valódi historikus adatokból** számítja ki az előző napi és 7 napos átlag értékeket, nem hardcode-olt átlagokat használ!

---

## 🛠️ 1. Környezet Előkészítés

### Rendszerkövetelmények:
- **Python 3.8+**
- **8GB RAM minimum**
- **2GB szabad tárhely**
- **Internet kapcsolat** (időjárási adatok és csomagok letöltéséhez)

### Telepítési Lépések:

#### 1.1 Projekt Letöltése
```bash
git clone <repository-url>
cd westend-hackathon
```

#### 1.2 Python Környezet Létrehozása
```bash
# Virtual environment létrehozása
python -m venv hackathon_env

# Aktiválás (Windows)
hackathon_env\Scripts\activate

# Aktiválás (Linux/Mac)
source hackathon_env/bin/activate
```

#### 1.3 Függőségek Telepítése
```bash
pip install -r requirements.txt
```

#### 1.4 Könyvtár Struktúra Ellenőrzése
```
westend-hackathon/
├── data/
├── models/
├── notebooks/
├── outputs/
├── src/
├── web_app/
├── create_model.py
├── simple_linear_demo.py
└── requirements.txt
```

---

## 🚀 2. Projekt Indítás (Gyors Start)

### 2.1 Teljes Pipeline Futtatása
```bash
# Komplett modell létrehozás (5-10 perc)
python create_model.py
```

**Várt kimenet:**
```
🚀 WESTEND HACKATHON - MODELL LÉTREHOZÁS
============================================================
📊 1. LÉPÉS: ADAT ELŐKÉSZÍTÉS
✅ 730 nap adatai generálva
✅ Adat előkészítés befejezve
🤖 2. LÉPÉS: MODELL BETANÍTÁS
✅ 8 modell sikeresen betanítva
📊 3. LÉPÉS: MODELL ÉRTÉKELÉS
🏆 Legjobb modell: Random Forest
💾 6. LÉPÉS: MODELLEK MENTÉSE
✅ Legjobb modell mentve: models/best_model_random_forest.joblib
```

### 2.2 Web Alkalmazás Indítása
```bash
streamlit run web_app/streamlit_app_standalone.py
```

**Várt kimenet:**
```
  You can now view your Streamlit app in your browser.
  Local URL: http://localhost:8501
  Network URL: http://192.168.1.100:8501
```

---

## 🔍 3. Részletes Lépések

### 3.1 Adat Előkészítés (Manuális)

#### Adatok Generálása:
```bash
cd src
python data_preparation.py
```

**Mit csinál:**
- Generál 730 nap szintetikus adatot
- Időjárási adatok szimulálása
- Marketing költések generálása
- Szezonális és heti mintázatok
- Ünnepnapok és iskolai szünetek

**Kimenet:**
- `data/hackathon_data.csv` (730 sor, 11 oszlop)

#### Adatok Ellenőrzése:
```python
import pandas as pd
data = pd.read_csv('data/hackathon_data.csv')
print(data.head())
print(data.describe())
```

### 3.2 Modell Betanítás (Manuális)

#### ML Pipeline Futtatása:
```bash
cd src
python machine_learning_models.py
```

**Mit csinál:**
- 8 különböző algoritmus tesztelése
- Cross-validation értékelés
- Feature importance kinyerése
- Vizualizációk készítése
- Legjobb modell mentése

**Kimenetek:**
- `models/best_model_random_forest.joblib`
- `outputs/model_results.csv`
- `outputs/*.png` (grafikonok)

### 3.3 Egyszerű Demo (Prezentációhoz)

#### Lineáris Regresszió Demo:
```bash
python simple_linear_demo.py
```

**Mit mutat be:**
- Egyszerű, érthető modell
- Koefficiensek magyarázata
- Interaktív előrejelzések
- Üzleti hatás kalkuláció

---

## 🎪 4. Demo Futtatás

### 4.1 Streamlit Web App

#### Indítás:
```bash
streamlit run web_app/streamlit_app_standalone.py
```

#### Funkciók:
1. **🎯 Előrejelzés oldal**:
   - Dátum kiválasztás
   - Időjárási paraméterek
   - Marketing költés beállítása
   - Azonnali előrejelzés

2. **📈 Adatok Áttekintése**:
   - Alapstatisztikák
   - Idősor grafikonok
   - Heti/havi mintázatok

3. **🤖 Modell Teljesítmény**:
   - Összehasonlító táblázatok
   - Pontossági metrikák
   - Teljesítmény grafikonok

4. **📊 Vizualizációk**:
   - Korrelációs heatmap
   - Időjárás hatása
   - Marketing hatás
   - Szezonális mintázatok

### 4.2 Jupyter Notebook Demo

#### Indítás:
```bash
jupyter notebook notebooks/hackathon_demo.ipynb
```

#### Tartalom:
- Interaktív adatelemzés
- Modell összehasonlítás
- Üzleti kalkulációk
- ROI vizualizációk

---

## 🎯 5. Demo Szcenáriók

### 5.1 Alapvető Előrejelzések

#### Szcenárió 1: Tipikus Hétköznap
```
Dátum: 2024-03-15 (péntek)
Hőmérséklet: 15°C
Csapadék: 0mm
Marketing: 300 EUR
Ünnepnap: Nem
Iskolai szünet: Nem

Várt eredmény: ~10,500 fő
```

#### Szcenárió 2: Hétvégi Jó Idő
```
Dátum: 2024-03-16 (szombat)
Hőmérséklet: 22°C
Csapadék: 0mm
Marketing: 500 EUR
Ünnepnap: Nem
Iskolai szünet: Nem

Várt eredmény: ~15,800 fő
```

#### Szcenárió 3: Esős Ünnepnap
```
Dátum: 2024-12-25 (karácsony)
Hőmérséklet: 5°C
Csapadék: 8mm
Marketing: 700 EUR
Ünnepnap: Igen
Iskolai szünet: Igen

Várt eredmény: ~13,200 fő
```

### 5.2 Extrém Szcenáriók

#### Téli Vihar:
```
Hőmérséklet: -10°C
Csapadék: 15mm
Marketing: 200 EUR
Hétvége: Nem

Várt eredmény: ~4,500 fő (alacsony)
```

#### Nyári Csúcs:
```
Hőmérséklet: 28°C
Csapadék: 0mm
Marketing: 800 EUR
Hétvége: Igen
Ünnepnap: Igen
Iskolai szünet: Igen

Várt eredmény: ~18,500 fő (magas)
```

---

## 🔧 6. Hibaelhárítás

### 6.1 Gyakori Problémák

#### "ModuleNotFoundError"
```bash
# Megoldás: Függőségek újratelepítése
pip install -r requirements.txt --force-reinstall
```

#### "FileNotFoundError: data/hackathon_data.csv"
```bash
# Megoldás: Adatok generálása
python src/data_preparation.py
```

#### "Streamlit app nem indul"
```bash
# Ellenőrizze a portot
netstat -an | findstr :8501

# Másik port használata
streamlit run web_app/streamlit_app_standalone.py --server.port 8502
```

#### "Modell fájl nem található"
```bash
# Megoldás: Modell újragenerálása
python create_model.py
```

### 6.2 Teljesítmény Problémák

#### Lassú futás:
- Csökkentse az adatok méretét (`days=365` helyett `days=180`)
- Használjon kevesebb modellt (`initialize_models()` módosítása)
- Zárjon be más alkalmazásokat

#### Memória problémák:
- Növelje a virtuális memóriát
- Használja a `simple_linear_demo.py`-t
- Csökkentse a vizualizációk számát

---

## 📊 7. Eredmények Értelmezése

### 7.1 Modell Metrikák

#### R² Score (Determinációs együttható):
- **0.85+**: Kiváló modell
- **0.70-0.85**: Jó modell  
- **0.50-0.70**: Elfogadható modell
- **<0.50**: Gyenge modell

#### RMSE (Root Mean Square Error):
- **<1,000 fő**: Kiváló pontosság
- **1,000-2,000 fő**: Jó pontosság
- **2,000-3,000 fő**: Elfogadható pontosság
- **>3,000 fő**: Gyenge pontosság

#### MAPE (Mean Absolute Percentage Error):
- **<10%**: Kiváló pontosság
- **10-20%**: Jó pontosság
- **20-30%**: Elfogadható pontosság
- **>30%**: Gyenge pontosság

### 7.2 Feature Importance

#### Top fontosságú jellemzők (várható):
1. **Hétvége** (40-60% súly)
2. **Ünnepnap** (30-50% súly)
3. **Hőmérséklet** (20-30% súly)
4. **Marketing kiadás** (15-25% súly)
5. **Csapadék** (10-20% súly)

---

## 🎪 8. Prezentációs Checklist

### 8.1 Technikai Előkészületek
- [ ] Python környezet működik
- [ ] Összes függőség telepítve
- [ ] Adatok generálva (`data/hackathon_data_full.csv`)
- [ ] Modell betanítva (`
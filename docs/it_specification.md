# 💻 Westend Hackathon - IT Specifikáció

## 🎯 **RENDSZER ÁTTEKINTÉS**

### Projekt Név
**Westend Mall - AI-alapú Látogatószám Előrejelző Rendszer**

### Verzió
**v3.0 (Production Ready)**

### Fejlesztési Időkeret
**Hackathon: 2 nap (Szeptember 11-12, 2025)**

---

## 🏗️ **RENDSZERARCHITEKTÚRA**

### Architektúra Típus
**Layered Architecture Pattern (Rétegelt Architektúra)**

### Fő Komponensek
1. **Presentation Layer** - Streamlit Web Interface
2. **Business Logic Layer** - Python Application Logic
3. **Data Access Layer** - Pandas/CSV Data Processing
4. **ML Engine Layer** - Scikit-learn Models
5. **Infrastructure Layer** - Python Runtime Environment

---

## 🛠️ **TECHNOLÓGIAI STACK**

### Backend Technológiák
| Komponens | Technológia | Verzió | Cél |
|-----------|-------------|---------|-----|
| **Runtime** | Python | 3.11+ | Fő programozási nyelv |
| **Web Framework** | Streamlit | 1.49+ | Webes felület |
| **ML Library** | Scikit-learn | 1.7+ | Gépi tanulás |
| **Data Processing** | Pandas | 2.3+ | Adatmanipuláció |
| **Numerical Computing** | NumPy | 2.3+ | Numerikus számítások |
| **Visualization** | Plotly | 6.3+ | Interaktív grafikonok |
| **Static Plots** | Matplotlib | 3.10+ | Statikus vizualizációk |
| **Statistical Plots** | Seaborn | 0.13+ | Statisztikai grafikonok |
| **Model Persistence** | Joblib | 1.5+ | Modell mentés/betöltés |
| **Excel Support** | OpenPyXL | 3.1+ | Excel fájlok kezelése |
| **Statistical Models** | StatsModels | 0.14+ | Statisztikai modellek |

### Frontend Technológiák
| Komponens | Technológia | Leírás |
|-----------|-------------|---------|
| **UI Framework** | Streamlit | Reaktív web komponensek |
| **Visualization** | Plotly.js | Interaktív JavaScript grafikonok |
| **Styling** | CSS/HTML | Egyedi stílusok |
| **Icons** | Unicode Emojis | Vizuális elemek |

---

## 📊 **ADATBÁZIS SPECIFIKÁCIÓ**

### Adattárolás Típus
**File-based Storage (CSV formátum)**

### Fő Adatstruktúra
```csv
datum,latogatoszam,atlaghomerseklet,csapadek,unnepnap,iskolai_szunet,marketing_kiadas,het_napja,honap,szezon,hetvege
2022-01-01,15432,2.5,0.0,1,1,450.0,6,1,1,1
```

### Adattáblák
| Tábla | Fájl | Rekordok | Oszlopok | Méret |
|-------|------|----------|----------|-------|
| **Tréning Adatok** | hackathon_data.csv | 730 | 11 | ~50KB |
| **Modell Eredmények** | model_results.csv | 3 | 12 | ~2KB |
| **Előrejelzések** | predictions.csv | Változó | 5 | Változó |

### Adat Típusok
```python
datum: datetime64[ns]          # Dátum
latogatoszam: int64           # Célváltozó (1000-25000)
atlaghomerseklet: float64     # Celsius (-10 to 40)
csapadek: float64            # mm (0-50)
unnepnap: int64              # Binary (0/1)
iskolai_szunet: int64        # Binary (0/1)
marketing_kiadas: float64    # HUF (100-1000)
het_napja: int64             # 1-7 (Hétfő-Vasárnap)
honap: int64                 # 1-12
szezon: int64                # 1-4 (Tél-Ősz)
hetvege: int64               # Binary (0/1)
```

---

## 🤖 **GÉPI TANULÁSI SPECIFIKÁCIÓ**

### Fő Algoritmus
**Random Forest Regressor**

### Modell Paraméterek
```python
RandomForestRegressor(
    n_estimators=100,         # Fák száma
    max_depth=10,             # Maximális mélység
    min_samples_split=5,      # Min. minták osztáshoz
    min_samples_leaf=2,       # Min. minták levélben
    random_state=42,          # Reprodukálhatóság
    n_jobs=-1                 # Párhuzamos feldolgozás
)
```

### Teljesítmény Metrikák
| Metrika | Érték | Cél |
|---------|-------|-----|
| **R² Score** | 0.857 | >0.8 |
| **MAE** | 1,300 | <1,500 |
| **RMSE** | 1,637 | <2,000 |
| **MAPE** | 14.0% | <15% |

### Alternatív Modellek
1. **Linear Regression** - Baseline modell
2. **XGBoost Regressor** - Gradient boosting
3. **Decision Tree** - Egyszerű fa modell

---

## 🔧 **RENDSZER KÖVETELMÉNYEK**

### Minimális Rendszerkövetelmények
| Komponens | Minimális | Ajánlott |
|-----------|-----------|----------|
| **Operációs Rendszer** | Windows 10, macOS 10.15, Ubuntu 18.04 | Windows 11, macOS 12+, Ubuntu 20.04+ |
| **Python Verzió** | 3.8+ | 3.11+ |
| **RAM** | 4 GB | 8 GB+ |
| **Szabad Lemezterület** | 500 MB | 1 GB+ |
| **Processzor** | Dual-core 2GHz | Quad-core 2.5GHz+ |
| **Internetkapcsolat** | Opcionális | Ajánlott (csomagok telepítéséhez) |

### Szoftver Függőségek
```bash
# Core Dependencies
pandas>=1.3.0
scikit-learn>=1.0.0
streamlit>=1.0.0
plotly>=5.0.0
numpy>=1.20.0

# Supporting Libraries
matplotlib>=3.3.0
seaborn>=0.11.0
joblib>=1.0.0
openpyxl>=3.0.0
statsmodels>=0.14.0
```

---

## 🚀 **DEPLOYMENT SPECIFIKÁCIÓ**

### Deployment Típus
**Standalone Desktop Application**

### Indítási Módok
1. **Automatikus Launcher**: `python launch_app.py`
2. **Streamlit Közvetlen**: `streamlit run web_app/streamlit_app_standalone.py`
3. **Egyszerű Launcher**: `python run_app.py`

### Port Konfiguráció
- **Default Port**: 8501
- **Alternatív Portok**: 8502, 8503, 8504, 8505
- **Automatikus Port Detection**: Igen

### Környezeti Változók
```bash
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=localhost
STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
PYTHONPATH=./src
```

---

## 📁 **PROJEKT STRUKTÚRA**

```
westend-hackathon/
├── 📊 data/                           # Adatfájlok
│   └── hackathon_data.csv            # Tréning adatok (730 sor)
├── 📋 docs/                          # Dokumentáció
│   ├── dataflow_diagram.py           # Adatáramlási diagram
│   ├── software_architecture.py      # Szoftver architektúra
│   ├── function_list.md             # Funkció lista
│   └── it_specification.md          # IT specifikáció
├── 🤖 models/                        # ML modellek
│   └── best_model_random_forest.joblib # Betanított modell
├── 📈 outputs/                       # Kimeneti fájlok
│   ├── model_results.csv            # Modell összehasonlítás
│   ├── predictions_vs_actual.png    # Eredmény grafikonok
│   ├── feature_importance.png       # Változó fontosság
│   ├── model_comparison.png         # Modell összehasonlítás
│   └── residual_analysis.png        # Residual analízis
├── 💻 src/                          # Forráskód
│   ├── __pycache__/                 # Python cache
│   ├── data_preparation.py          # Adat előkészítés
│   └── machine_learning_models.py   # ML modellek
├── 🌐 web_app/                      # Web alkalmazás
│   ├── streamlit_app.py            # Moduláris app
│   └── streamlit_app_standalone.py  # Önálló app
├── 🚀 launch_app.py                 # Automatikus launcher
├── 🔧 run_app.py                    # Egyszerű launcher
├── 🧪 test_app.py                   # Teszt script
├── 📋 requirements.txt              # Python függőségek
├── 📖 README.md                     # Projekt dokumentáció
├── 🔧 SETUP_GUIDE.md               # Telepítési útmutató
└── 📊 Figure_*.png                  # Generált grafikonok
```

---

## 🔒 **BIZTONSÁGI SPECIFIKÁCIÓ**

### Adatbiztonság
- **Helyi Tárolás**: Minden adat lokálisan tárolva
- **Nincs Külső API**: Nincs érzékeny adat továbbítás
- **Input Validáció**: Felhasználói input ellenőrzése
- **Error Handling**: Biztonságos hibaüzenet megjelenítés

### Hozzáférés Kontroll
- **Localhost Only**: Csak helyi hozzáférés engedélyezett
- **No Authentication**: Egyszerű desktop alkalmazás
- **File System Access**: Csak projekt könyvtár hozzáférés

---

## ⚡ **TELJESÍTMÉNY SPECIFIKÁCIÓ**

### Válaszidők
| Funkció | Cél Válaszidő | Mért Érték |
|---------|---------------|-------------|
| **Alkalmazás Indítás** | <10 sec | ~5 sec |
| **Adatok Betöltése** | <2 sec | ~1 sec |
| **Modell Betöltés** | <3 sec | ~1.5 sec |
| **Előrejelzés Számítás** | <1 sec | ~0.3 sec |
| **Grafikon Generálás** | <2 sec | ~1 sec |

### Erőforrás Használat
| Erőforrás | Várható Használat | Maximális |
|-----------|-------------------|-----------|
| **RAM** | 200-400 MB | 800 MB |
| **CPU** | 5-15% | 50% (tanítás alatt) |
| **Lemezterület** | 50 MB | 200 MB |
| **Hálózat** | 0 MB/s | 0 MB/s (offline) |

---

## 🧪 **TESZTELÉSI SPECIFIKÁCIÓ**

### Tesztelési Szintek
1. **Unit Testing**: Egyedi funkciók tesztelése
2. **Integration Testing**: Komponensek közötti kapcsolatok
3. **System Testing**: Teljes rendszer tesztelése
4. **User Acceptance Testing**: Felhasználói élmény tesztelése

### Teszt Esetek
```python
# Automatikus teszt futtatása
python test_app.py

# Tesztelendő funkciók:
✅ Adatok betöltése
✅ Modell betöltése
✅ Előrejelzés számítása
✅ Grafikon generálása
✅ Web felület indítása
```

### Teszt Adatok
- **Tréning Set**: 584 rekord (80%)
- **Test Set**: 146 rekord (20%)
- **Validációs Set**: Cross-validation (5-fold)

---

## 📊 **MONITOROZÁS ÉS LOGGING**

### Logging Szintek
```python
import logging

# Konfiguráció
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Naplózott események:
- Alkalmazás indítás/leállás
- Adatok betöltése
- Modell műveletek
- Hibák és kivételek
- Teljesítmény metrikák
```

### Metrikák Gyűjtése
- **Válaszidő mérés**: Minden fő funkció
- **Memória használat**: Folyamatos monitorozás
- **Hiba gyakoriság**: Exception tracking
- **Felhasználói interakciók**: Streamlit események

---

## 🔄 **VERZIÓKEZELÉS ÉS KARBANTARTÁS**

### Verziókezelés
```bash
# Git repository struktúra
git init
git add .
git commit -m "Westend Hackathon v3.0 - Production Ready"
git tag v3.0
```

### Karbantartási Feladatok
1. **Havi**: Függőségek frissítése
2. **Negyedéves**: Modell újratanítása
3. **Éves**: Teljes kód audit
4. **Szükség szerint**: Hibajavítások

### Backup Stratégia
- **Adatok**: Napi CSV backup
- **Modellek**: Verzióval ellátott mentés
- **Kód**: Git repository
- **Konfigurációk**: Dokumentált beállítások

---

## 📈 **SKÁLÁZHATÓSÁGI TERVEK**

### Rövid Távú (3 hónap)
- [ ] Valós időjárási API integráció
- [ ] Többféle ML algoritmus támogatása
- [ ] Mobil-barát responsive design
- [ ] Automatikus adatfrissítés

### Közép Távú (6-12 hónap)
- [ ] Valós bevásárlóközpont adatok
- [ ] Deep Learning modellek
- [ ] Multi-tenant architektúra
- [ ] REST API fejlesztés

### Hosszú Távú (1+ év)
- [ ] Cloud deployment (AWS/Azure)
- [ ] Real-time streaming data
- [ ] Advanced analytics dashboard
- [ ] Mobile alkalmazás fejlesztés

---

## 🎯 **ÖSSZEFOGLALÓ**

### Technikai Jellemzők
- **🏗️ Architektúra**: Layered Pattern
- **💻 Platform**: Cross-platform Python
- **🤖 AI Engine**: Random Forest (85.7% pontosság)
- **🌐 Interface**: Streamlit Web App
- **📊 Visualization**: Plotly + Matplotlib
- **⚡ Performance**: <1sec válaszidő
- **🔒 Security**: Localhost only, input validation
- **📦 Deployment**: Standalone executable

### Üzleti Értékek
- **🎯 Pontosság**: 85.7% R² score
- **⚡ Sebesség**: Azonnali előrejelzések
- **💰 Költséghatékonyság**: Ingyenes open-source stack
- **🔧 Karbantarthatóság**: Jól dokumentált, moduláris kód
- **📈 Skálázhatóság**: Könnyen bővíthető architektúra

**✅ A rendszer teljes mértékben megfelelő a hackathon követelményeinek és készen áll a bemutatásra!** 🏆

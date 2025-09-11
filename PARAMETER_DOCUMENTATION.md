# 🔢 Westend Hackathon - Paraméter Dokumentáció

## 📊 A Modellben Használt 11 Alapparaméter

### 🎯 **ALAPVETŐ BEMENETI PARAMÉTEREK (11 db)**

A látogatószám előrejelző modell az alábbi **11 alapvető paramétert** használja bemenetként:

#### 1. **📅 `datum`** 
- **Típus**: Date (YYYY-MM-DD)
- **Leírás**: Az előrejelzés célnapja
- **Hatás**: Szezonális és időbeli trendek meghatározása
- **Példa**: "2024-03-15"

#### 2. **🌡️ `atlaghomerseklet`**
- **Típus**: Float (°C)
- **Tartomány**: -10°C - +40°C
- **Leírás**: Napi átlaghőmérséklet Celsius fokban
- **Hatás**: Jelentős befolyás a látogatottságra
- **Optimális tartomány**: 15-25°C (legnagyobb látogatottság)

#### 3. **🌧️ `csapadek`**
- **Típus**: Float (mm)
- **Tartomány**: 0-50 mm
- **Leírás**: Napi csapadékmennyiség milliméterben
- **Hatás**: Negatív hatás 5mm felett (-40% látogatottság)

#### 4. **🎉 `unnepnap`**
- **Típus**: Binary (0/1)
- **Leírás**: Ünnepnap jelzése
- **Hatás**: +60% látogatottság növekedés
- **Példák**: Karácsony, Újév, Nemzeti ünnepek

#### 5. **🏫 `iskolai_szunet`**
- **Típus**: Binary (0/1)
- **Leírás**: Iskolai szünet időszak
- **Hatás**: +20% látogatottság (családok többet vásárolnak)
- **Időszakok**: Nyári, téli, tavaszi szünet

#### 6. **💰 `marketing_kiadas`**
- **Típus**: Float (EUR)
- **Tartomány**: 0-1000 EUR
- **Leírás**: Napi marketing költés euróban
- **Hatás**: Lineáris kapcsolat a látogatottsággal
- **Optimális**: 400-600 EUR/nap

#### 7. **📅 `het_napja`**
- **Típus**: Integer (1-7)
- **Leírás**: Hét napja (1=Hétfő, 7=Vasárnap)
- **Hatás**: Hétvégék +40% látogatottság
- **Mintázat**: Hétfő-Csütörtök alacsony, Péntek-Vasárnap magas

#### 8. **📆 `honap`**
- **Típus**: Integer (1-12)
- **Leírás**: Év hónapja
- **Hatás**: Szezonális mintázatok
- **Csúcsok**: December (karácsony), Június-Augusztus (nyár)

#### 9. **🍂 `szezon`**
- **Típus**: Integer (1-4)
- **Leírás**: Évszak (1=Tél, 2=Tavasz, 3=Nyár, 4=Ősz)
- **Hatás**: Nyár +30%, Tél -20% látogatottság
- **Alapja**: Meteorológiai évszakok

#### 10. **🌅 `hetvege`**
- **Típus**: Binary (0/1)
- **Leírás**: Hétvége jelzése (Szombat/Vasárnap)
- **Hatás**: +40% látogatottság növekedés
- **Oka**: Szabadidős vásárlás, családi programok

#### 11. **📊 `latogatoszam`** *(célváltozó)*
- **Típus**: Integer (fő)
- **Tartomány**: 1,000-25,000 fő/nap
- **Leírás**: Napi látogatók száma
- **Átlag**: 10,974 fő/nap
- **Szórás**: ±3,500 fő

---

## 🔧 **KIBŐVÍTETT FEATURE SET (43 paraméter)**

A modell tanítás során az alapvető 11 paraméterből **43 jellemzőt** hoz létre:

### 📈 **Származtatott Jellemzők (32 db)**

#### 🌤️ **Időjárási Kategóriák (3 db)**
- `hideg`: Hőmérséklet < 5°C
- `meleg`: Hőmérséklet > 25°C  
- `esik`: Csapadék > 1mm

#### 💸 **Marketing Kategóriák (2 db)**
- `alacsony_marketing`: < 200 EUR
- `magas_marketing`: > 500 EUR

#### 🔄 **Interakciós Jellemzők (2 db)**
- `hetvege_es_jo_ido`: Hétvége ÉS jó idő
- `unnep_es_marketing`: Ünnepnap ÉS magas marketing

#### ⏰ **Lag Jellemzők (4 db)**
- `latogatoszam_lag1`: Előző napi látogatószám
- `atlaghomerseklet_lag1`: Előző napi hőmérséklet
- `latogatoszam_7d_avg`: 7 napos átlag látogatószám
- `atlaghomerseklet_7d_avg`: 7 napos átlag hőmérséklet

#### 📅 **One-Hot Encoded Jellemzők (21 db)**
- `nap_1` - `nap_7`: Hét napjai (7 db)
- `honap_1` - `honap_12`: Hónapok (12 db)
- `szezon_1` - `szezon_4`: Évszakok (4 db)

---

## 📊 **PARAMÉTER FONTOSSÁGI RANGSOR**

### 🥇 **Top 10 Legfontosabb Paraméter** *(Random Forest alapján)*

1. **🌡️ Átlaghőmérséklet** (15.2% fontosság)
2. **📅 Hétvége** (12.8% fontosság)  
3. **💰 Marketing kiadás** (11.4% fontosság)
4. **🌧️ Csapadék** (9.7% fontosság)
5. **🎉 Ünnepnap** (8.9% fontosság)
6. **🏫 Iskolai szünet** (7.6% fontosság)
7. **📆 December hónap** (6.3% fontosság)
8. **🍂 Nyári szezon** (5.8% fontosság)
9. **📊 7 napos átlag látogatószám** (5.2% fontosság)
10. **🌤️ Jó időjárás** (4.9% fontosság)

---

## 🎯 **PARAMÉTER HASZNÁLATI ÚTMUTATÓ**

### 🔧 **Optimális Beállítások**

#### 🌟 **Maximális Látogatottság Eléréséhez:**
- **Időjárás**: 20-25°C, 0mm csapadék
- **Időzítés**: Hétvége + Ünnepnap
- **Marketing**: 500-600 EUR/nap
- **Szezon**: Nyár vagy Karácsony időszak

#### ⚠️ **Kerülendő Kombinációk:**
- Hideg (<0°C) + Esős (>5mm) = -70% látogatottság
- Hétköznap + Alacsony marketing (<200 EUR) = -50% látogatottság
- Tél + Rossz idő = -60% látogatottság

### 📈 **Paraméter Érzékenységi Analízis**

| Paraméter | 1% Változás Hatása | Megjegyzés |
|-----------|-------------------|------------|
| Hőmérséklet | ±0.8% látogatottság | Lineáris kapcsolat |
| Marketing | ±0.6% látogatottság | Csökkenő hatékonyság |
| Csapadék | ±1.2% látogatottság | Exponenciális hatás |
| Hétvége | ±40% látogatottság | Bináris ugrás |

---

## 🔍 **ADATMINŐSÉGI KÖVETELMÉNYEK**

### ✅ **Validációs Szabályok**

#### 🌡️ **Hőmérséklet**
- Tartomány: -20°C - +45°C
- Pontosság: ±0.5°C
- Hiányzó értékek: <5%

#### 🌧️ **Csapadék**
- Tartomány: 0-100mm
- Pontosság: ±0.1mm
- Negatív értékek: Nem megengedettek

#### 💰 **Marketing**
- Tartomány: 0-2000 EUR
- Pontosság: ±10 EUR
- Nulla értékek: Megengedettek

### 🚨 **Hibakezelés**

#### **Hiányzó Értékek:**
- Numerikus: Medián helyettesítés
- Kategorikus: Mód helyettesítés
- Idősor: Lineáris interpoláció

#### **Outlier Kezelés:**
- IQR módszer (1.5 × IQR)
- Capping 1%-99% percentilisekre
- Szakértői validáció szélsőséges esetekben

---

## 📚 **TECHNIKAI IMPLEMENTÁCIÓ**

### 🔧 **Adatfeldolgozási Pipeline**

```python
# 1. Alapparaméterek betöltése
base_params = ['datum', 'atlaghomerseklet', 'csapadek', 
               'unnepnap', 'iskolai_szunet', 'marketing_kiadas',
               'het_napja', 'honap', 'szezon', 'hetvege']

# 2. Feature Engineering
derived_features = create_features(base_params)

# 3. One-Hot Encoding
encoded_features = encode_categorical(derived_features)

# 4. Scaling
scaled_features = scaler.fit_transform(encoded_features)
```

### 📊 **Modell Input Formátum**

A végső modell **43 numerikus jellemzőt** vár bemenetként:
- Skálázott numerikus értékek (StandardScaler)
- One-hot encoded kategorikus változók
- Származtatott interakciós jellemzők
- Lag és rolling átlag jellemzők

---

## 🎯 **ÖSSZEFOGLALÁS**

### 📋 **Kulcs Pontok**

1. **11 alapparaméter** → **43 modell jellemző**
2. **Hőmérséklet és hétvége** a legfontosabb tényezők
3. **Interakciós hatások** jelentős befolyással bírnak
4. **Szezonális minták** erős prediktív erővel rendelkeznek
5. **Marketing ROI** mérhető és optimalizálható

### 🎯 **Gyakorlati Alkalmazás**

A paraméterek ismerete lehetővé teszi:
- **Pontos előrejelzések** készítését
- **Marketing optimalizálást**
- **Erőforrás tervezést**
- **Bevétel maximalizálást**
- **Költség minimalizálást**

---

*"Az adatok csak akkor válnak értékessé, ha megértjük őket és cselekvésre inspirálnak."*

**Kapcsolat**: team@westend-hackathon.com

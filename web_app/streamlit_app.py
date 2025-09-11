"""
Westend Hackathon - Streamlit Web Application
============================================

Interaktív web alkalmazás a bevásárlóközpont látogatószám előrejelzéshez.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
# import plotly.graph_objects as go
# from plotly.subplots import make_subplots
import joblib
import os
import sys
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Projekt útvonal hozzáadása
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

try:
    # Import módosítása a helyes útvonal használatához
    sys.path.insert(0, os.path.join(parent_dir, 'src'))
    from data_preparation import DataPreparation
except ImportError as e:
    st.error(f"Modul importálási hiba: {e}")
    st.error("📁 Ellenőrizze, hogy a src könyvtárban vannak-e a szükséges Python fájlok:")
    st.error("   - src/data_preparation.py")
    st.stop()

# Oldal konfiguráció
st.set_page_config(
    page_title="🏬 Westend Látogatószám Előrejelző",
    page_icon="🏬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS stílus
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .prediction-result {
        background-color: #e8f4fd;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border: 2px solid #1f77b4;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Adatok betöltése cache-elve"""
    try:
        df = pd.read_csv('data/hackathon_data.csv')
        df['datum'] = pd.to_datetime(df['datum'])
        return df
    except FileNotFoundError:
        st.error("Adatfájl nem található! Futtassa előbb a data_preparation.py scriptet.")
        return None

@st.cache_resource
def load_model_and_scaler():
    """Modell és scaler betöltése cache-elve"""
    try:
        model = joblib.load('models/best_model_random_forest.joblib')
        
        # Scaler újra létrehozása a training adatokból
        data_prep = DataPreparation()
        df = data_prep.load_and_clean_data('data/hackathon_data.csv')
        df = data_prep.create_features(df)
        df = data_prep.encode_categorical(df)
        X, y, feature_columns = data_prep.prepare_features_target(df)
        
        return model, data_prep.scaler, feature_columns
    except FileNotFoundError:
        st.error("Modell fájl nem található! Futtassa előbb a machine_learning_models.py scriptet.")
        return None, None, None

@st.cache_data
def load_results():
    """Modell eredmények betöltése"""
    try:
        results = pd.read_csv('outputs/model_results.csv', index_col=0)
        return results
    except FileNotFoundError:
        return None

def create_prediction_features(date, temperature, rainfall, is_holiday, 
                             is_school_break, marketing_spend, scaler, 
                             feature_columns):
    """Előrejelzéshez szükséges jellemzők létrehozása és skálázása"""
    
    # Alapvető jellemzők
    features = {
        'atlaghomerseklet': temperature,
        'csapadek': rainfall,
        'unnepnap': int(is_holiday),
        'iskolai_szunet': int(is_school_break),
        'marketing_kiadas': marketing_spend,
        'hetvege': int(date.weekday() >= 5),
        'ev': date.year,
        'het_szama': date.isocalendar()[1],
        'ev_napja': date.timetuple().tm_yday,
    }
    
    # Időjárás kategóriák
    features['hideg'] = int(temperature < 5)
    features['meleg'] = int(temperature > 25)
    features['esik'] = int(rainfall > 1)
    
    # Marketing kategóriák
    features['alacsony_marketing'] = int(marketing_spend < 200)
    features['magas_marketing'] = int(marketing_spend > 500)
    
    # Interakciós jellemzők
    features['hetvege_es_jo_ido'] = features['hetvege'] * (1 - features['hideg']) * (1 - features['esik'])
    features['unnep_es_marketing'] = features['unnepnap'] * features['magas_marketing']
    
    # Lag jellemzők (átlagos értékekkel helyettesítjük)
    features['latogatoszam_lag1'] = 10974  # átlagos látogatószám
    features['atlaghomerseklet_lag1'] = temperature
    features['latogatoszam_7d_avg'] = 10974
    features['atlaghomerseklet_7d_avg'] = temperature
    
    # Hét napjai (one-hot encoding)
    for i in range(1, 8):
        features[f'nap_{i}'] = int(date.weekday() + 1 == i)
    
    # Hónapok (one-hot encoding)
    for i in range(1, 13):
        features[f'honap_{i}'] = int(date.month == i)
    
    # Szezonok (one-hot encoding)
    month = date.month
    if month in [12, 1, 2]:
        season = 1  # Tél
    elif month in [3, 4, 5]:
        season = 2  # Tavasz
    elif month in [6, 7, 8]:
        season = 3  # Nyár
    else:
        season = 4  # Ősz
    
    for i in range(1, 5):
        features[f'szezon_{i}'] = int(season == i)
    
    # DataFrame létrehozása helyes oszlop sorrenddel
    df = pd.DataFrame([features])
    df = df[feature_columns]  # Helyes sorrend biztosítása
    
    # Numerikus oszlopok skálázása
    numeric_columns = df.select_dtypes(include=[np.number]).columns
    df_scaled = df.copy()
    df_scaled[numeric_columns] = scaler.transform(df[numeric_columns])
    
    return df_scaled

def main():
    # Főcím
    st.markdown('<h1 class="main-header">🏬 Westend Látogatószám Előrejelző</h1>', unsafe_allow_html=True)
    
    # Adatok és modell betöltése
    data = load_data()
    model, scaler, feature_columns = load_model_and_scaler()
    results = load_results()
    
    if data is None or model is None or scaler is None:
        st.stop()
    
    # Sidebar - Navigáció
    st.sidebar.title("📊 Navigáció")
    page = st.sidebar.selectbox(
        "Válasszon oldalt:",
        ["🎯 Előrejelzés", "📈 Adatok Áttekintése", "🤖 Modell Teljesítmény", "📊 Vizualizációk"]
    )
    
    if page == "🎯 Előrejelzés":
        prediction_page(model, data, scaler, feature_columns)
    elif page == "📈 Adatok Áttekintése":
        data_overview_page(data)
    elif page == "🤖 Modell Teljesítmény":
        model_performance_page(results)
    elif page == "📊 Vizualizációk":
        visualizations_page(data)

def prediction_page(model, data, scaler, feature_columns):
    """Előrejelzés oldal"""
    st.header("🎯 Látogatószám Előrejelzés")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📅 Dátum és Időjárás")
        
        # Dátum kiválasztás
        prediction_date = st.date_input(
            "Válasszon dátumot:",
            value=datetime.now().date(),
            min_value=datetime(2024, 1, 1).date(),
            max_value=datetime(2025, 12, 31).date()
        )
        
        # Időjárás paraméterek
        temperature = st.slider(
            "Átlaghőmérséklet (°C):",
            min_value=-10, max_value=40, value=15, step=1
        )
        
        rainfall = st.slider(
            "Csapadék (mm):",
            min_value=0.0, max_value=100.0, value=0.0, step=0.5,
            help="0mm = száraz idő, 5-10mm = enyhe eső, 10-20mm = közepes eső, 20-50mm = erős eső, 50mm+ = viharos idő"
        )
    
    with col2:
        st.subheader("🎪 Speciális Napok és Marketing")
        
        # Speciális napok
        is_holiday = st.checkbox("Ünnepnap")
        is_school_break = st.checkbox("Iskolai szünet")
        
        # Marketing költés
        marketing_spend = st.slider(
            "Marketing kiadás (EUR):",
            min_value=0, max_value=1000, value=300, step=10
        )
    
    # Előrejelzés gomb
    if st.button("🔮 Látogatószám Előrejelzése", type="primary"):
        
        # Jellemzők létrehozása
        features_df = create_prediction_features(
            prediction_date, temperature, rainfall, 
            is_holiday, is_school_break, marketing_spend,
            scaler, feature_columns
        )
        
        # Előrejelzés
        try:
            prediction = model.predict(features_df)[0]
            
            # Eredmény megjelenítése
            st.markdown("---")
            st.markdown('<div class="prediction-result">', unsafe_allow_html=True)
            st.markdown(f"### 🎯 Előrejelzett látogatószám: **{prediction:,.0f} fő**")
            
            # Kontextus információk
            avg_visitors = data['latogatoszam'].mean()
            difference = prediction - avg_visitors
            percentage_diff = (difference / avg_visitors) * 100
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Előrejelzés", f"{prediction:,.0f}", f"{difference:+.0f}")
            with col2:
                st.metric("Átlagtól való eltérés", f"{percentage_diff:+.1f}%")
            with col3:
                if prediction > avg_visitors:
                    st.success("🟢 Átlag feletti látogatottság")
                else:
                    st.info("🔵 Átlag alatti látogatottság")
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Tényezők hatása
            st.markdown("### 📊 Befolyásoló Tényezők")
            factors_col1, factors_col2 = st.columns(2)
            
            with factors_col1:
                st.write("**Pozitív hatások:**")
                if prediction_date.weekday() >= 5:
                    st.write("• 📅 Hétvége (+40% várható)")
                if is_holiday:
                    st.write("• 🎉 Ünnepnap (+60% várható)")
                if is_school_break:
                    st.write("• 🏫 Iskolai szünet (+20% várható)")
                if 15 <= temperature <= 25:
                    st.write("• 🌤️ Kellemes időjárás (+10% várható)")
                if marketing_spend > 400:
                    st.write("• 📢 Magas marketing kiadás")
            
            with factors_col2:
                st.write("**Negatív hatások:**")
                if temperature < 0:
                    st.write("• 🥶 Fagyos idő (-30% várható)")
                elif temperature > 30:
                    st.write("• 🔥 Túl meleg (-20% várható)")
                if rainfall > 20:
                    st.write(f"• 🌧️ Viharos eső ({rainfall:.1f}mm, -50% várható)")
                elif rainfall > 10:
                    st.write(f"• 🌧️ Erős eső ({rainfall:.1f}mm, -40% várható)")
                elif rainfall > 5:
                    st.write(f"• 🌧️ Közepes eső ({rainfall:.1f}mm, -25% várható)")
                elif rainfall > 1:
                    st.write(f"• 🌧️ Enyhe eső ({rainfall:.1f}mm, -10% várható)")
                if prediction_date.weekday() < 5 and not is_holiday:
                    st.write("• 📅 Hétköznap")
                if marketing_spend < 200:
                    st.write("• 📢 Alacsony marketing kiadás")
            
        except Exception as e:
            st.error(f"Előrejelzési hiba: {str(e)}")

def data_overview_page(data):
    """Adatok áttekintése oldal"""
    st.header("📈 Adatok Áttekintése")
    
    # Dátum tartomány kiválasztás
    st.subheader("📅 Időszak Kiválasztása")
    col1, col2 = st.columns(2)
    
    with col1:
        start_date = st.date_input(
            "Kezdő dátum:",
            value=data['datum'].min(),
            min_value=data['datum'].min(),
            max_value=data['datum'].max()
        )
    
    with col2:
        end_date = st.date_input(
            "Záró dátum:",
            value=data['datum'].max(),
            min_value=data['datum'].min(),
            max_value=data['datum'].max()
        )
    
    # Adatok szűrése a kiválasztott dátum tartományra
    filtered_data = data[
        (data['datum'] >= pd.to_datetime(start_date)) & 
        (data['datum'] <= pd.to_datetime(end_date))
    ]
    
    if len(filtered_data) == 0:
        st.warning("Nincs adat a kiválasztott időszakban!")
        return
    
    # Alapstatisztikák a szűrt adatokra
    st.subheader(f"📊 Statisztikák ({start_date} - {end_date})")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Napok száma", f"{len(filtered_data):,}")
    with col2:
        st.metric("Átlagos látogatószám", 
                 f"{filtered_data['latogatoszam'].mean():,.0f}")
    with col3:
        st.metric("Maximum látogatószám", 
                 f"{filtered_data['latogatoszam'].max():,.0f}")
    with col4:
        st.metric("Minimum látogatószám", 
                 f"{filtered_data['latogatoszam'].min():,.0f}")
    
    # Idősor grafikon
    st.subheader("📅 Látogatószám Idősor")
    
    fig = px.line(filtered_data, x='datum', y='latogatoszam', 
                  title=f'Napi Látogatószám Alakulása ({start_date} - {end_date})')
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    # Heti és havi mintázatok a szűrt adatokra
    col1, col2 = st.columns(2)
    
    with col1:
        # Heti mintázat
        if 'het_napja' in filtered_data.columns:
            weekly_data = filtered_data.groupby('het_napja')['latogatoszam'].mean().reset_index()
            days = ['Hétfő', 'Kedd', 'Szerda', 'Csütörtök', 'Péntek', 'Szombat', 'Vasárnap']
            weekly_data['nap_neve'] = [days[i-1] for i in weekly_data['het_napja']]
            
            fig_weekly = px.bar(weekly_data, x='nap_neve', y='latogatoszam',
                               title='Átlagos Látogatószám Napok Szerint (Szűrt Időszak)')
            st.plotly_chart(fig_weekly, use_container_width=True)
    
    with col2:
        # Havi mintázat
        if 'honap' in filtered_data.columns:
            monthly_data = filtered_data.groupby('honap')['latogatoszam'].mean().reset_index()
            months = ['Jan', 'Feb', 'Már', 'Ápr', 'Máj', 'Jún', 
                     'Júl', 'Aug', 'Szep', 'Okt', 'Nov', 'Dec']
            monthly_data['honap_neve'] = [months[i-1] for i in monthly_data['honap']]
            
            fig_monthly = px.bar(monthly_data, x='honap_neve', y='latogatoszam',
                                title='Átlagos Látogatószám Hónapok Szerint (Szűrt Időszak)')
            st.plotly_chart(fig_monthly, use_container_width=True)
    
    # Időjárási összefüggések a szűrt időszakra
    st.subheader("🌤️ Időjárási Összefüggések")
    col1, col2 = st.columns(2)
    
    with col1:
        # Hőmérséklet vs látogatószám
        fig_temp = px.scatter(filtered_data, x='atlaghomerseklet', y='latogatoszam',
                             title='Hőmérséklet vs Látogatószám (Szűrt Időszak)',
                             trendline="ols")
        st.plotly_chart(fig_temp, use_container_width=True)
    
    with col2:
        # Marketing vs látogatószám
        fig_marketing = px.scatter(filtered_data, x='marketing_kiadas', y='latogatoszam',
                                  title='Marketing Kiadás vs Látogatószám (Szűrt Időszak)',
                                  trendline="ols")
        st.plotly_chart(fig_marketing, use_container_width=True)
    
    # Adatok táblázat
    st.subheader("📋 Adatok Táblázat (Szűrt Időszak)")
    
    # Oszlopok kiválasztása megjelenítéshez
    display_columns = ['datum', 'latogatoszam', 'atlaghomerseklet', 'csapadek', 
                      'marketing_kiadas', 'hetvege', 'unnepnap']
    available_columns = [col for col in display_columns if col in filtered_data.columns]
    
    st.dataframe(
        filtered_data[available_columns].head(min(100, len(filtered_data))), 
        use_container_width=True
    )
    
    # Összefoglaló statisztikák
    st.subheader("📊 Részletes Statisztikák")
    numeric_columns = filtered_data.select_dtypes(include=[np.number]).columns
    if len(numeric_columns) > 0:
        st.dataframe(
            filtered_data[numeric_columns].describe().round(2), 
            use_container_width=True
        )

def model_performance_page(results):
    """Modell teljesítmény oldal"""
    st.header("🤖 Modell Teljesítmény")
    
    if results is None:
        st.warning("Modell eredmények nem elérhetők.")
        return
    
    # Teljesítmény metrikák
    st.subheader("📊 Modell Összehasonlítás")
    
    # Metrikák táblázat
    display_results = results[['test_rmse', 'test_r2', 'test_mape', 'cv_rmse']].copy()
    display_results.columns = ['Test RMSE', 'Test R²', 'Test MAPE (%)', 'CV RMSE']
    display_results = display_results.round(4)
    
    st.dataframe(display_results, use_container_width=True)
    
    # Legjobb modell kiemelése
    best_model = display_results.index[0]
    st.success(f"🏆 Legjobb modell: **{best_model}**")
    
    # Teljesítmény vizualizációk
    col1, col2 = st.columns(2)
    
    with col1:
        # RMSE összehasonlítás
        fig_rmse = px.bar(
            x=display_results.index, 
            y=display_results['Test RMSE'],
            title='Test RMSE Összehasonlítás',
            labels={'x': 'Modell', 'y': 'RMSE'}
        )
        st.plotly_chart(fig_rmse, use_container_width=True)
    
    with col2:
        # R² összehasonlítás
        fig_r2 = px.bar(
            x=display_results.index, 
            y=display_results['Test R²'],
            title='Test R² Összehasonlítás',
            labels={'x': 'Modell', 'y': 'R²'}
        )
        st.plotly_chart(fig_r2, use_container_width=True)
    
    # Modell interpretálás
    st.subheader("🔍 Modell Interpretálás")
    st.write("""
    **RMSE (Root Mean Square Error)**: Az előrejelzési hiba mértéke. Minél kisebb, annál jobb.
    
    **R² (Determinációs együttható)**: A modell által magyarázott variancia aránya (0-1 között). Minél közelebb van 1-hez, annál jobb.
    
    **MAPE (Mean Absolute Percentage Error)**: Az átlagos százalékos hiba. Üzleti szempontból könnyen értelmezhető.
    
    **CV RMSE (Cross-Validation RMSE)**: Cross-validation alapú RMSE, ami a modell általánosítási képességét mutatja.
    """)

def visualizations_page(data):
    """Vizualizációk oldal"""
    st.header("📊 Részletes Vizualizációk")
    
    # Dátum tartomány kiválasztás
    st.subheader("📅 Időszak Kiválasztása a Vizualizációkhoz")
    col1, col2 = st.columns(2)
    
    with col1:
        start_date = st.date_input(
            "Kezdő dátum:",
            value=data['datum'].min(),
            min_value=data['datum'].min(),
            max_value=data['datum'].max(),
            key="viz_start_date"
        )
    
    with col2:
        end_date = st.date_input(
            "Záró dátum:",
            value=data['datum'].max(),
            min_value=data['datum'].min(),
            max_value=data['datum'].max(),
            key="viz_end_date"
        )
    
    # Adatok szűrése
    filtered_data = data[
        (data['datum'] >= pd.to_datetime(start_date)) & 
        (data['datum'] <= pd.to_datetime(end_date))
    ]
    
    if len(filtered_data) == 0:
        st.warning("Nincs adat a kiválasztott időszakban!")
        return
    
    st.info(f"📊 Vizualizációk {len(filtered_data)} napra ({start_date} - {end_date})")
    
    # Korrelációs heatmap
    st.subheader("🔥 Korrelációs Heatmap")
    
    numeric_cols = ['latogatoszam', 'atlaghomerseklet', 'csapadek', 'marketing_kiadas']
    available_numeric_cols = [col for col in numeric_cols if col in filtered_data.columns]
    
    if len(available_numeric_cols) > 1:
        corr_matrix = filtered_data[available_numeric_cols].corr()
        
        fig_heatmap = px.imshow(corr_matrix, 
                               text_auto=True, 
                               aspect="auto",
                               title=f"Változók Közötti Korreláció ({start_date} - {end_date})")
        st.plotly_chart(fig_heatmap, use_container_width=True)
    
    # Időjárás hatása
    st.subheader("🌤️ Időjárás Hatása")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Hőmérséklet vs látogatószám
        if 'atlaghomerseklet' in filtered_data.columns:
            fig_temp = px.scatter(filtered_data, x='atlaghomerseklet', y='latogatoszam',
                                 title=f'Hőmérséklet vs Látogatószám ({start_date} - {end_date})',
                                 trendline="ols")
            st.plotly_chart(fig_temp, use_container_width=True)
    
    with col2:
        # Csapadék hatása
        if 'csapadek' in filtered_data.columns:
            filtered_data_copy = filtered_data.copy()
            filtered_data_copy['esik'] = filtered_data_copy['csapadek'] > 1
            rain_effect = filtered_data_copy.groupby('esik')['latogatoszam'].mean().reset_index()
            rain_effect['esik'] = rain_effect['esik'].map({True: 'Esős', False: 'Száraz'})
            
            fig_rain = px.bar(rain_effect, x='esik', y='latogatoszam',
                             title=f'Csapadék Hatása a Látogatószámra ({start_date} - {end_date})')
            st.plotly_chart(fig_rain, use_container_width=True)
    
    # Marketing hatás
    st.subheader("📢 Marketing Hatás")
    
    if 'marketing_kiadas' in filtered_data.columns:
        # Marketing költés vs látogatószám
        fig_marketing = px.scatter(filtered_data, x='marketing_kiadas', y='latogatoszam',
                                  title=f'Marketing Kiadás vs Látogatószám ({start_date} - {end_date})',
                                  trendline="ols")
        st.plotly_chart(fig_marketing, use_container_width=True)
    
    # Szezonális mintázatok
    st.subheader("🍂 Szezonális Mintázatok")
    
    if 'szezon' in filtered_data.columns:
        seasonal_data = filtered_data.groupby('szezon')['latogatoszam'].mean().reset_index()
        seasons = {1: 'Tél', 2: 'Tavasz', 3: 'Nyár', 4: 'Ősz'}
        seasonal_data['szezon_neve'] = seasonal_data['szezon'].map(seasons)
        
        fig_seasonal = px.bar(seasonal_data, x='szezon_neve', y='latogatoszam',
                             title=f'Átlagos Látogatószám Évszakok Szerint ({start_date} - {end_date})')
        st.plotly_chart(fig_seasonal, use_container_width=True)
    
    # Hétvége vs hétköznap összehasonlítás
    st.subheader("📅 Hétvége vs Hétköznap")
    
    if 'hetvege' in filtered_data.columns:
        weekend_data = filtered_data.groupby('hetvege')['latogatoszam'].mean().reset_index()
        weekend_data['nap_tipus'] = weekend_data['hetvege'].map({0: 'Hétköznap', 1: 'Hétvége'})
        
        fig_weekend = px.bar(weekend_data, x='nap_tipus', y='latogatoszam',
                            title=f'Hétvége vs Hétköznap Látogatottság ({start_date} - {end_date})')
        st.plotly_chart(fig_weekend, use_container_width=True)
    
    # Időszakos trendek
    st.subheader("📈 Időszakos Trendek")
    
    if len(filtered_data) > 30:  # Csak ha elegendő adat van
        # Havi trend
        filtered_data_copy = filtered_data.copy()
        filtered_data_copy['year_month'] = filtered_data_copy['datum'].dt.to_period('M').astype(str)
        monthly_trend = filtered_data_copy.groupby('year_month')['latogatoszam'].mean().reset_index()
        
        fig_trend = px.line(monthly_trend, x='year_month', y='latogatoszam',
                           title=f'Havi Átlagos Látogatottság Trend ({start_date} - {end_date})')
        fig_trend.update_xaxes(tickangle=45)
        st.plotly_chart(fig_trend, use_container_width=True)

if __name__ == "__main__":
    main()

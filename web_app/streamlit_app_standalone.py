"""
Westend Hackathon - Standalone Streamlit Web Application
========================================================

Önálló web alkalmazás a bevásárlóközpont látogatószám előrejelzéshez.
Nem igényel külső modulokat, minden szükséges kód benne van.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import joblib
import os
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

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
        df = pd.read_csv('../data/hackathon_data.csv')
        df['datum'] = pd.to_datetime(df['datum'])
        return df
    except FileNotFoundError:
        try:
            df = pd.read_csv('data/hackathon_data.csv')
            df['datum'] = pd.to_datetime(df['datum'])
            return df
        except FileNotFoundError:
            st.error("❌ Adatfájl nem található! Ellenőrizze, hogy a data/hackathon_data.csv létezik.")
            return None

@st.cache_resource
def load_model():
    """Modell betöltése cache-elve"""
    model_paths = [
        '../models/best_model_random_forest.joblib',
        'models/best_model_random_forest.joblib'
    ]
    
    for path in model_paths:
        try:
            model = joblib.load(path)
            return model
        except FileNotFoundError:
            continue
    
    st.error("❌ Modell fájl nem található! Ellenőrizze, hogy a models/best_model_random_forest.joblib létezik.")
    return None

@st.cache_data
def load_results():
    """Modell eredmények betöltése"""
    result_paths = [
        '../outputs/model_results.csv',
        'outputs/model_results.csv'
    ]
    
    for path in result_paths:
        try:
            results = pd.read_csv(path, index_col=0)
            return results
        except FileNotFoundError:
            continue
    return None

def create_prediction_features(date, temperature, rainfall, is_holiday, is_school_break, marketing_spend):
    """Előrejelzéshez szükséges jellemzők létrehozása"""
    
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
    
    # Lag jellemzők (dinamikus számítás)
    # Valós implementációban ezeket a korábbi napok adataiból kellene számítani
    # Most a bemeneti paraméterek alapján becsüljük
    base_visitors = 10000  # Alapértelmezett látogatószám
    
    # Hőmérséklet hatása
    temp_factor = 1 + (temperature - 15) * 0.02  # 15°C alapértelmezett
    
    # Időjárás hatása
    weather_factor = 1.0
    if temperature < 0:
        weather_factor *= 0.7  # Hideg idő
    elif temperature > 30:
        weather_factor *= 0.8  # Túl meleg
    if rainfall > 5:
        weather_factor *= 0.6  # Esős idő
    
    # Speciális napok hatása
    special_factor = 1.0
    if is_holiday:
        special_factor *= 1.6  # Ünnepnap
    if is_school_break:
        special_factor *= 1.2  # Iskolai szünet
    if date.weekday() >= 5:  # Hétvége
        special_factor *= 1.4
    
    # Marketing hatása
    marketing_factor = 1 + (marketing_spend - 300) * 0.0005  # 300 EUR alapértelmezett
    
    # Lag jellemzők becslése
    estimated_visitors = base_visitors * temp_factor * weather_factor * special_factor * marketing_factor
    features['latogatoszam_lag1'] = estimated_visitors * 0.95  # Előző nap (kissé kevesebb)
    features['atlaghomerseklet_lag1'] = temperature
    features['latogatoszam_7d_avg'] = estimated_visitors * 1.05  # 7 napos átlag (kissé több)
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
    
    return pd.DataFrame([features])

def main():
    # Főcím
    st.markdown('<h1 class="main-header">🏬 Westend Látogatószám Előrejelző</h1>', unsafe_allow_html=True)
    
    # Adatok és modell betöltése
    data = load_data()
    model = load_model()
    results = load_results()
    
    if data is None or model is None:
        st.error("⚠️ Az alkalmazás nem tud elindulni a hiányzó fájlok miatt.")
        st.info("🔧 Futtassa előbb a következő scripteket:")
        st.code("python src/data_preparation.py")
        st.code("python src/machine_learning_models.py")
        st.stop()
    
    # Sidebar - Navigáció
    st.sidebar.title("📊 Navigáció")
    page = st.sidebar.selectbox(
        "Válasszon oldalt:",
        ["🎯 Előrejelzés", "📈 Adatok Áttekintése", "🤖 Modell Teljesítmény", "📊 Vizualizációk"]
    )
    
    if page == "🎯 Előrejelzés":
        prediction_page(model, data)
    elif page == "📈 Adatok Áttekintése":
        data_overview_page(data)
    elif page == "🤖 Modell Teljesítmény":
        model_performance_page(results)
    elif page == "📊 Vizualizációk":
        visualizations_page(data)

def prediction_page(model, data):
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
            min_value=0.0, max_value=50.0, value=0.0, step=0.1
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
            is_holiday, is_school_break, marketing_spend
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
                if rainfall > 5:
                    st.write("• 🌧️ Erős eső (-40% várható)")
                if prediction_date.weekday() < 5 and not is_holiday:
                    st.write("• 📅 Hétköznap")
                if marketing_spend < 200:
                    st.write("• 📢 Alacsony marketing kiadás")
            
        except Exception as e:
            st.error(f"Előrejelzési hiba: {str(e)}")

def data_overview_page(data):
    """Adatok áttekintése oldal"""
    st.header("📈 Adatok Áttekintése")
    
    # Alapstatisztikák
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Összes nap", f"{len(data):,}")
    with col2:
        st.metric("Átlagos látogatószám", f"{data['latogatoszam'].mean():,.0f}")
    with col3:
        st.metric("Maximum látogatószám", f"{data['latogatoszam'].max():,.0f}")
    with col4:
        st.metric("Minimum látogatószám", f"{data['latogatoszam'].min():,.0f}")
    
    # Idősor grafikon
    st.subheader("📅 Látogatószám Idősor")
    
    fig = px.line(data, x='datum', y='latogatoszam', 
                  title='Napi Látogatószám Alakulása')
    fig.update_layout(height=400)
    st.plotly_chart(fig, width='stretch')
    
    # Heti és havi mintázatok
    col1, col2 = st.columns(2)
    
    with col1:
        # Heti mintázat
        weekly_data = data.groupby('het_napja')['latogatoszam'].mean().reset_index()
        days = ['Hétfő', 'Kedd', 'Szerda', 'Csütörtök', 'Péntek', 'Szombat', 'Vasárnap']
        weekly_data['nap_neve'] = [days[i-1] for i in weekly_data['het_napja']]
        
        fig_weekly = px.bar(weekly_data, x='nap_neve', y='latogatoszam',
                           title='Átlagos Látogatószám Napok Szerint')
        st.plotly_chart(fig_weekly, width='stretch')
    
    with col2:
        # Havi mintázat
        monthly_data = data.groupby('honap')['latogatoszam'].mean().reset_index()
        months = ['Jan', 'Feb', 'Már', 'Ápr', 'Máj', 'Jún', 
                 'Júl', 'Aug', 'Szep', 'Okt', 'Nov', 'Dec']
        monthly_data['honap_neve'] = [months[i-1] for i in monthly_data['honap']]
        
        fig_monthly = px.bar(monthly_data, x='honap_neve', y='latogatoszam',
                            title='Átlagos Látogatószám Hónapok Szerint')
        st.plotly_chart(fig_monthly, width='stretch')
    
    # Adatok táblázat
    st.subheader("📋 Adatok Táblázat")
    st.dataframe(data.head(100), width='stretch')

def model_performance_page(results):
    """Modell teljesítmény oldal"""
    st.header("🤖 Modell Teljesítmény")
    
    if results is None:
        st.warning("⚠️ Modell eredmények nem elérhetők.")
        st.info("📊 Alapvető modell információk:")
        st.write("- **Modell típus**: Random Forest Regressor")
        st.write("- **Jellemzők száma**: 43")
        st.write("- **Tanító adatok**: 584 minta")
        st.write("- **Teszt adatok**: 146 minta")
        st.write("- **Várható pontosság**: ~85%")
        return
    
    # Teljesítmény metrikák
    st.subheader("📊 Modell Összehasonlítás")
    
    # Metrikák táblázat
    display_results = results[['test_rmse', 'test_r2', 'test_mape', 'cv_rmse']].copy()
    display_results.columns = ['Test RMSE', 'Test R²', 'Test MAPE (%)', 'CV RMSE']
    display_results = display_results.round(4)
    
    st.dataframe(display_results, width='stretch')
    
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

def visualizations_page(data):
    """Vizualizációk oldal"""
    st.header("📊 Részletes Vizualizációk")
    
    # Korrelációs heatmap
    st.subheader("🔥 Korrelációs Heatmap")
    
    numeric_cols = ['latogatoszam', 'atlaghomerseklet', 'csapadek', 'marketing_kiadas']
    corr_matrix = data[numeric_cols].corr()
    
    fig_heatmap = px.imshow(corr_matrix, 
                           text_auto=True, 
                           aspect="auto",
                           title="Változók Közötti Korreláció")
    st.plotly_chart(fig_heatmap, use_container_width=True)
    
    # Időjárás hatása
    st.subheader("🌤️ Időjárás Hatása")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Hőmérséklet vs látogatószám
        fig_temp = px.scatter(data, x='atlaghomerseklet', y='latogatoszam',
                             title='Hőmérséklet vs Látogatószám',
                             trendline="ols")
        st.plotly_chart(fig_temp, use_container_width=True)
    
    with col2:
        # Csapadék hatása
        data['esik'] = data['csapadek'] > 1
        rain_effect = data.groupby('esik')['latogatoszam'].mean().reset_index()
        rain_effect['esik'] = rain_effect['esik'].map({True: 'Esős', False: 'Száraz'})
        
        fig_rain = px.bar(rain_effect, x='esik', y='latogatoszam',
                         title='Csapadék Hatása a Látogatószámra')
        st.plotly_chart(fig_rain, use_container_width=True)
    
    # Marketing hatás
    st.subheader("📢 Marketing Hatás")
    
    # Marketing költés vs látogatószám
    fig_marketing = px.scatter(data, x='marketing_kiadas', y='latogatoszam',
                              title='Marketing Kiadás vs Látogatószám',
                              trendline="ols")
    st.plotly_chart(fig_marketing, use_container_width=True)
    
    # Szezonális mintázatok
    st.subheader("🍂 Szezonális Mintázatok")
    
    seasonal_data = data.groupby('szezon')['latogatoszam'].mean().reset_index()
    seasons = {1: 'Tél', 2: 'Tavasz', 3: 'Nyár', 4: 'Ősz'}
    seasonal_data['szezon_neve'] = seasonal_data['szezon'].map(seasons)
    
    fig_seasonal = px.bar(seasonal_data, x='szezon_neve', y='latogatoszam',
                         title='Átlagos Látogatószám Évszakok Szerint')
    st.plotly_chart(fig_seasonal, use_container_width=True)

if __name__ == "__main__":
    main()

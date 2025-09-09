"""
Westend Hackathon - Adat Előkészítés
=====================================

Ez a modul felelős az adatok betöltéséért, tisztításáért és előkészítéséért
a látogatószám előrejelző modell számára.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split

class DataPreparation:
    def __init__(self):
        self.scaler = StandardScaler()
        self.label_encoders = {}
        
    def generate_sample_data(self, start_date='2022-01-01', days=730):
        """
        Minta adatok generálása a hackathon demonstrációhoz
        
        Args:
            start_date (str): Kezdő dátum
            days (int): Napok száma
            
        Returns:
            pd.DataFrame: Generált adatok
        """
        print("🔄 Minta adatok generálása...")
        
        # Dátumok generálása
        dates = pd.date_range(start=start_date, periods=days, freq='D')
        
        # Alapvető adatok inicializálása
        data = []
        
        for date in dates:
            # Szezon meghatározása (1-4: tél, tavasz, nyár, ősz)
            month = date.month
            if month in [12, 1, 2]:
                season = 1  # Tél
            elif month in [3, 4, 5]:
                season = 2  # Tavasz
            elif month in [6, 7, 8]:
                season = 3  # Nyár
            else:
                season = 4  # Ősz
            
            # Hétvége és hét napja
            day_of_week = date.weekday() + 1  # 1-7 (hétfő-vasárnap)
            is_weekend = 1 if day_of_week in [6, 7] else 0
            
            # Ünnepnapok szimulálása (egyszerűsített)
            holidays = [
                (1, 1),   # Újév
                (3, 15),  # Nemzeti ünnep
                (5, 1),   # Munka ünnepe
                (8, 20),  # Szent István nap
                (10, 23), # Nemzeti ünnep
                (11, 1),  # Mindenszentek
                (12, 24), # Szenteste
                (12, 25), # Karácsony
                (12, 26)  # Karácsony másnapja
            ]
            is_holiday = 1 if (date.month, date.day) in holidays else 0
            
            # Iskolai szünet szimulálása
            school_holidays = [
                (7, 1, 8, 31),    # Nyári szünet
                (12, 20, 1, 10),  # Téli szünet
                (4, 1, 4, 10)     # Tavaszi szünet
            ]
            is_school_break = 0
            for start_month, start_day, end_month, end_day in school_holidays:
                if ((date.month == start_month and date.day >= start_day) or 
                    (date.month == end_month and date.day <= end_day) or
                    (start_month == 12 and end_month == 1 and 
                     (date.month == 12 or date.month == 1))):
                    is_school_break = 1
                    break
            
            # Időjárás szimulálása szezon alapján
            base_temps = {1: 2, 2: 12, 3: 25, 4: 15}  # Átlaghőmérsékletek szezonként
            temperature = base_temps[season] + np.random.normal(0, 5)
            
            # Csapadék szimulálása
            rainfall = max(0, np.random.exponential(2) if np.random.random() < 0.3 else 0)
            
            # Marketing kiadás szimulálása
            # Magasabb hétvégén és ünnepnapokon
            base_marketing = 300
            if is_weekend or is_holiday:
                marketing_spend = base_marketing * (1.5 + np.random.random() * 0.5)
            else:
                marketing_spend = base_marketing * (0.8 + np.random.random() * 0.4)
            
            # Látogatószám szimulálása (összetett függvény)
            base_visitors = 8000
            
            # Szezonális hatás
            seasonal_multiplier = {1: 0.8, 2: 1.1, 3: 1.3, 4: 1.0}[season]
            
            # Hétvége hatás
            weekend_multiplier = 1.4 if is_weekend else 1.0
            
            # Ünnepnap hatás
            holiday_multiplier = 1.6 if is_holiday else 1.0
            
            # Iskolai szünet hatás
            school_multiplier = 1.2 if is_school_break else 1.0
            
            # Időjárás hatás
            weather_multiplier = 1.0
            if temperature < 0:
                weather_multiplier *= 0.7
            elif temperature > 30:
                weather_multiplier *= 0.8
            elif 15 <= temperature <= 25:
                weather_multiplier *= 1.1
                
            if rainfall > 5:
                weather_multiplier *= 0.6
            
            # Marketing hatás
            marketing_multiplier = 1 + (marketing_spend - 300) / 1000
            
            # Véletlenség
            random_factor = 0.8 + np.random.random() * 0.4
            
            # Végső látogatószám
            visitors = int(base_visitors * seasonal_multiplier * weekend_multiplier * 
                          holiday_multiplier * school_multiplier * weather_multiplier * 
                          marketing_multiplier * random_factor)
            
            # Minimum 1000 látogató
            visitors = max(1000, visitors)
            
            data.append({
                'datum': date.strftime('%Y-%m-%d'),
                'latogatoszam': visitors,
                'atlaghomerseklet': round(temperature, 1),
                'csapadek': round(rainfall, 1),
                'unnepnap': is_holiday,
                'iskolai_szunet': is_school_break,
                'marketing_kiadas': round(marketing_spend, 0),
                'het_napja': day_of_week,
                'honap': date.month,
                'szezon': season,
                'hetvege': is_weekend
            })
        
        df = pd.DataFrame(data)
        print(f"✅ {len(df)} nap adatai generálva")
        return df
    
    def load_and_clean_data(self, file_path='data/hackathon_data.csv'):
        """
        Adatok betöltése és alapvető tisztítás
        
        Args:
            file_path (str): CSV fájl elérési útja
            
        Returns:
            pd.DataFrame: Tisztított adatok
        """
        print(f"🔄 Adatok betöltése: {file_path}")
        
        try:
            df = pd.read_csv(file_path)
            print(f"✅ {len(df)} sor betöltve")
        except FileNotFoundError:
            print("⚠️  Adatfájl nem található, minta adatok generálása...")
            df = self.generate_sample_data()
            os.makedirs('data', exist_ok=True)
            df.to_csv(file_path, index=False, encoding='utf-8')
            print(f"✅ Minta adatok mentve: {file_path}")
        
        # Alapvető adattisztítás
        print("🔄 Adatok tisztítása...")
        
        # Dátum oszlop konvertálása
        df['datum'] = pd.to_datetime(df['datum'])
        
        # Hiányzó értékek kezelése
        numeric_columns = ['latogatoszam', 'atlaghomerseklet', 'csapadek', 'marketing_kiadas']
        for col in numeric_columns:
            if col in df.columns:
                df[col] = df[col].fillna(df[col].median())
        
        # Outlierek kezelése (IQR módszer)
        for col in numeric_columns:
            if col in df.columns:
                Q1 = df[col].quantile(0.25)
                Q3 = df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                
                # Outlierek capping-je
                df[col] = df[col].clip(lower_bound, upper_bound)
        
        print("✅ Adatok tisztítva")
        return df
    
    def create_features(self, df):
        """
        Új jellemzők létrehozása
        
        Args:
            df (pd.DataFrame): Alapadatok
            
        Returns:
            pd.DataFrame: Bővített adatok
        """
        print("🔄 Új jellemzők létrehozása...")
        
        df = df.copy()
        
        # Dátum alapú jellemzők
        df['ev'] = df['datum'].dt.year
        df['het_szama'] = df['datum'].dt.isocalendar().week
        df['ev_napja'] = df['datum'].dt.dayofyear
        
        # Hétvége jellemző (ha nincs)
        if 'hetvege' not in df.columns:
            df['hetvege'] = (df['het_napja'].isin([6, 7])).astype(int)
        
        # Időjárás kategóriák
        df['hideg'] = (df['atlaghomerseklet'] < 5).astype(int)
        df['meleg'] = (df['atlaghomerseklet'] > 25).astype(int)
        df['esik'] = (df['csapadek'] > 1).astype(int)
        
        # Marketing kategóriák
        df['alacsony_marketing'] = (df['marketing_kiadas'] < 200).astype(int)
        df['magas_marketing'] = (df['marketing_kiadas'] > 500).astype(int)
        
        # Interakciós jellemzők
        df['hetvege_es_jo_ido'] = df['hetvege'] * (1 - df['hideg']) * (1 - df['esik'])
        df['unnep_es_marketing'] = df['unnepnap'] * df['magas_marketing']
        
        # Lag jellemzők (előző napi értékek)
        df = df.sort_values('datum')
        df['latogatoszam_lag1'] = df['latogatoszam'].shift(1)
        df['atlaghomerseklet_lag1'] = df['atlaghomerseklet'].shift(1)
        
        # Rolling átlagok (7 napos)
        df['latogatoszam_7d_avg'] = df['latogatoszam'].rolling(window=7, min_periods=1).mean()
        df['atlaghomerseklet_7d_avg'] = df['atlaghomerseklet'].rolling(window=7, min_periods=1).mean()
        
        print(f"✅ {len([col for col in df.columns if col not in ['datum', 'latogatoszam']])} jellemző létrehozva")
        return df
    
    def encode_categorical(self, df):
        """
        Kategorikus változók kódolása
        
        Args:
            df (pd.DataFrame): Adatok
            
        Returns:
            pd.DataFrame: Kódolt adatok
        """
        print("🔄 Kategorikus változók kódolása...")
        
        df = df.copy()
        
        # One-hot encoding a hét napjaihoz
        df_encoded = pd.get_dummies(df, columns=['het_napja'], prefix='nap', dtype=int)
        
        # Hónap encoding
        df_encoded = pd.get_dummies(df_encoded, columns=['honap'], prefix='honap', dtype=int)
        
        # Szezon encoding
        df_encoded = pd.get_dummies(df_encoded, columns=['szezon'], prefix='szezon', dtype=int)
        
        print("✅ Kategorikus változók kódolva")
        return df_encoded
    
    def prepare_features_target(self, df):
        """
        Jellemzők és célváltozó elkülönítése
        
        Args:
            df (pd.DataFrame): Teljes adathalmaz
            
        Returns:
            tuple: (X, y) jellemzők és célváltozó
        """
        print("🔄 Jellemzők és célváltozó elkülönítése...")
        
        # Célváltozó
        y = df['latogatoszam'].values
        
        # Jellemzők (dátum és célváltozó kizárása)
        feature_columns = [col for col in df.columns 
                          if col not in ['datum', 'latogatoszam']]
        X = df[feature_columns]
        
        # Numerikus oszlopok skálázása
        numeric_columns = X.select_dtypes(include=[np.number]).columns
        X_scaled = X.copy()
        X_scaled[numeric_columns] = self.scaler.fit_transform(X[numeric_columns])
        
        print(f"✅ {X_scaled.shape[1]} jellemző és {len(y)} minta elkészítve")
        return X_scaled, y, feature_columns
    
    def split_data(self, X, y, test_size=0.2, random_state=42):
        """
        Adatok train/test felosztása
        
        Args:
            X: Jellemzők
            y: Célváltozó
            test_size (float): Test halmaz aránya
            random_state (int): Random seed
            
        Returns:
            tuple: (X_train, X_test, y_train, y_test)
        """
        print(f"🔄 Adatok felosztása (train: {1-test_size:.0%}, test: {test_size:.0%})...")
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state, shuffle=True
        )
        
        print(f"✅ Train: {len(X_train)} minta, Test: {len(X_test)} minta")
        return X_train, X_test, y_train, y_test
    
    def get_data_summary(self, df):
        """
        Adatok összefoglaló statisztikái
        
        Args:
            df (pd.DataFrame): Adatok
            
        Returns:
            dict: Összefoglaló statisztikák
        """
        summary = {
            'rows': len(df),
            'columns': len(df.columns),
            'date_range': f"{df['datum'].min()} - {df['datum'].max()}",
            'avg_visitors': df['latogatoszam'].mean(),
            'min_visitors': df['latogatoszam'].min(),
            'max_visitors': df['latogatoszam'].max(),
            'missing_values': df.isnull().sum().sum()
        }
        
        return summary
    
    def full_pipeline(self, file_path='data/hackathon_data.csv'):
        """
        Teljes adat előkészítési pipeline
        
        Args:
            file_path (str): Adatfájl elérési útja
            
        Returns:
            tuple: (X_train, X_test, y_train, y_test, feature_columns, summary)
        """
        print("🚀 Teljes adat előkészítési pipeline indítása...\n")
        
        # 1. Adatok betöltése és tisztítása
        df = self.load_and_clean_data(file_path)
        
        # 2. Új jellemzők létrehozása
        df = self.create_features(df)
        
        # 3. Kategorikus változók kódolása
        df = self.encode_categorical(df)
        
        # 4. Jellemzők és célváltozó elkülönítése
        X, y, feature_columns = self.prepare_features_target(df)
        
        # 5. Train/test felosztás
        X_train, X_test, y_train, y_test = self.split_data(X, y)
        
        # 6. Összefoglaló
        summary = self.get_data_summary(df)
        
        print("\n" + "="*50)
        print("📊 ADAT ELŐKÉSZÍTÉS ÖSSZEFOGLALÓ")
        print("="*50)
        print(f"Összes sor: {summary['rows']:,}")
        print(f"Összes oszlop: {summary['columns']:,}")
        print(f"Dátum tartomány: {summary['date_range']}")
        print(f"Átlagos látogatószám: {summary['avg_visitors']:,.0f}")
        print(f"Min látogatószám: {summary['min_visitors']:,}")
        print(f"Max látogatószám: {summary['max_visitors']:,}")
        print(f"Hiányzó értékek: {summary['missing_values']}")
        print(f"Train minták: {len(X_train):,}")
        print(f"Test minták: {len(X_test):,}")
        print("="*50)
        
        return X_train, X_test, y_train, y_test, feature_columns, summary

# Példa használat
if __name__ == "__main__":
    # Adat előkészítés inicializálása
    data_prep = DataPreparation()
    
    # Teljes pipeline futtatása
    X_train, X_test, y_train, y_test, features, summary = data_prep.full_pipeline()
    
    print("\n🎯 Adat előkészítés befejezve!")
    print(f"Jellemzők: {len(features)}")
    print(f"Első 10 jellemző: {features[:10]}")


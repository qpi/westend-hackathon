"""
Westend Hackathon - Egyszerű Lineáris Regresszió Demo
====================================================

Ez a script egy egyszerűsített lineáris regressziós modellt mutat be
demonstrációs célokra. Könnyen érthető és gyorsan futtatható.

Ideális hackathon prezentációkhoz és oktatási célokra.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_percentage_error
from sklearn.model_selection import train_test_split
import warnings
warnings.filterwarnings('ignore')

class SimpleLinearDemo:
    def __init__(self):
        self.model = None
        self.feature_names = None
        self.scaler_params = None
        
    def load_data(self):
        """
        Egyszerűsített adatok betöltése
        """
        print("📊 Adatok betöltése...")
        
        try:
            data = pd.read_csv('data/hackathon_data.csv')
            data['datum'] = pd.to_datetime(data['datum'])
            print(f"✅ {len(data)} nap adatai betöltve")
            return data
        except FileNotFoundError:
            print("❌ Adatfájl nem található!")
            print("🔧 Futtassa előbb: python src/data_preparation.py")
            return None
    
    def prepare_simple_features(self, data):
        """
        Egyszerű jellemzők előkészítése (csak a legfontosabbak)
        """
        print("🔧 Egyszerű jellemzők előkészítése...")
        
        # Csak a legérthetőbb jellemzők
        features = pd.DataFrame()
        features['homerseklet'] = data['atlaghomerseklet']
        features['csapadek'] = data['csapadek'] 
        features['marketing'] = data['marketing_kiadas']
        features['hetvege'] = data['hetvege']
        features['unnepnap'] = data['unnepnap']
        features['iskolai_szunet'] = data['iskolai_szunet']
        
        # Egyszerű származtatott jellemzők
        features['jo_ido'] = ((features['homerseklet'] > 15) & 
                             (features['homerseklet'] < 25) & 
                             (features['csapadek'] < 1)).astype(int)
        
        features['rossz_ido'] = ((features['homerseklet'] < 5) | 
                                (features['csapadek'] > 5)).astype(int)
        
        features['magas_marketing'] = (features['marketing'] > 500).astype(int)
        
        # Interakció: hétvége + jó idő
        features['hetvege_jo_ido'] = features['hetvege'] * features['jo_ido']
        
        self.feature_names = features.columns.tolist()
        
        print(f"✅ {len(self.feature_names)} egyszerű jellemző készítve")
        return features
    
    def train_simple_model(self, X, y):
        """
        Egyszerű lineáris regresszió betanítása
        """
        print("🤖 Egyszerű lineáris modell betanítása...")
        
        # Train-test felosztás
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Lineáris regresszió
        self.model = LinearRegression()
        self.model.fit(X_train, y_train)
        
        # Előrejelzések
        y_pred_train = self.model.predict(X_train)
        y_pred_test = self.model.predict(X_test)
        
        # Értékelés
        train_r2 = r2_score(y_train, y_pred_train)
        test_r2 = r2_score(y_test, y_pred_test)
        test_rmse = np.sqrt(mean_squared_error(y_test, y_pred_test))
        test_mape = mean_absolute_percentage_error(y_test, y_pred_test) * 100
        
        print(f"✅ Modell betanítva!")
        print(f"   Train R²: {train_r2:.4f}")
        print(f"   Test R²: {test_r2:.4f}")
        print(f"   Test RMSE: {test_rmse:.0f} fő")
        print(f"   Test MAPE: {test_mape:.2f}%")
        
        return X_train, X_test, y_train, y_test, y_pred_test
    
    def explain_model(self):
        """
        Modell magyarázata egyszerű nyelvezet
        """
        print("\n🔍 MODELL MAGYARÁZAT")
        print("=" * 50)
        print("A modell egy egyszerű matematikai képlet:")
        print("Látogatószám = Konstans + (Tényező1 × Súly1) + (Tényező2 × Súly2) + ...")
        print()
        
        print("📊 TÉNYEZŐK HATÁSA:")
        print("-" * 30)
        
        # Koefficiensek értelmezése
        for i, (feature, coef) in enumerate(zip(self.feature_names, self.model.coef_)):
            effect = "pozitív" if coef > 0 else "negatív"
            strength = "erős" if abs(coef) > 1000 else "közepes" if abs(coef) > 500 else "gyenge"
            
            print(f"{feature:20}: {coef:8.0f} ({strength} {effect} hatás)")
        
        print(f"{'Alapérték':20}: {self.model.intercept_:8.0f}")
        
        print("\n💡 ÉRTELMEZÉS:")
        print("- Pozitív szám = növeli a látogatószámot")
        print("- Negatív szám = csökkenti a látogatószámot") 
        print("- Nagyobb abszolút érték = erősebb hatás")
    
    def create_visualizations(self, X_test, y_test, y_pred_test):
        """
        Egyszerű vizualizációk
        """
        print("\n📈 Vizualizációk készítése...")
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # 1. Előrejelzés vs Valóság
        axes[0,0].scatter(y_test, y_pred_test, alpha=0.6, color='blue')
        axes[0,0].plot([y_test.min(), y_test.max()], 
                      [y_test.min(), y_test.max()], 'r--', lw=2)
        axes[0,0].set_xlabel('Valós Látogatószám')
        axes[0,0].set_ylabel('Előrejelzett Látogatószám')
        axes[0,0].set_title('Előrejelzés Pontossága')
        axes[0,0].grid(True, alpha=0.3)
        
        # 2. Tényezők fontossága
        coefs = self.model.coef_
        colors = ['green' if c > 0 else 'red' for c in coefs]
        axes[0,1].barh(self.feature_names, coefs, color=colors, alpha=0.7)
        axes[0,1].set_xlabel('Hatás Erőssége')
        axes[0,1].set_title('Tényezők Hatása')
        axes[0,1].grid(True, alpha=0.3)
        
        # 3. Hiba eloszlás
        residuals = y_test - y_pred_test
        axes[1,0].hist(residuals, bins=20, alpha=0.7, color='skyblue')
        axes[1,0].set_xlabel('Előrejelzési Hiba')
        axes[1,0].set_ylabel('Gyakoriság')
        axes[1,0].set_title('Hibák Eloszlása')
        axes[1,0].grid(True, alpha=0.3)
        
        # 4. Hiba vs Előrejelzés
        axes[1,1].scatter(y_pred_test, residuals, alpha=0.6, color='orange')
        axes[1,1].axhline(y=0, color='r', linestyle='--')
        axes[1,1].set_xlabel('Előrejelzett Értékek')
        axes[1,1].set_ylabel('Hibák')
        axes[1,1].set_title('Hibák Mintázata')
        axes[1,1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('outputs/simple_linear_demo.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print("✅ Vizualizációk kész: outputs/simple_linear_demo.png")
    
    def interactive_prediction(self):
        """
        Interaktív előrejelzés demo
        """
        print("\n🔮 INTERAKTÍV ELŐREJELZÉS DEMO")
        print("=" * 50)
        
        scenarios = [
            {
                "név": "Tipikus hétköznap",
                "homerseklet": 15, "csapadek": 0, "marketing": 300,
                "hetvege": 0, "unnepnap": 0, "iskolai_szunet": 0
            },
            {
                "név": "Hétvégi jó idő", 
                "homerseklet": 22, "csapadek": 0, "marketing": 500,
                "hetvege": 1, "unnepnap": 0, "iskolai_szunet": 0
            },
            {
                "név": "Esős ünnepnap",
                "homerseklet": 12, "csapadek": 8, "marketing": 700,
                "hetvege": 0, "unnepnap": 1, "iskolai_szunet": 0
            },
            {
                "név": "Téli hétvége",
                "homerseklet": -2, "csapadek": 0, "marketing": 400,
                "hetvege": 1, "unnepnap": 0, "iskolai_szunet": 0
            },
            {
                "név": "Nyári csúcs",
                "homerseklet": 28, "csapadek": 0, "marketing": 800,
                "hetvege": 1, "unnepnap": 1, "iskolai_szunet": 1
            }
        ]
        
        predictions = []
        for scenario in scenarios:
            # Jellemzők előkészítése
            features = [
                scenario["homerseklet"],
                scenario["csapadek"], 
                scenario["marketing"],
                scenario["hetvege"],
                scenario["unnepnap"],
                scenario["iskolai_szunet"]
            ]
            
            # Származtatott jellemzők
            jo_ido = int((features[0] > 15) and (features[0] < 25) and (features[1] < 1))
            rossz_ido = int((features[0] < 5) or (features[1] > 5))
            magas_marketing = int(features[2] > 500)
            hetvege_jo_ido = features[3] * jo_ido
            
            features.extend([jo_ido, rossz_ido, magas_marketing, hetvege_jo_ido])
            
            # Előrejelzés
            prediction = self.model.predict([features])[0]
            prediction = max(1000, int(prediction))  # Minimum 1000
            predictions.append(prediction)
            
            print(f"{scenario['név']:20}: {prediction:6,} fő")
        
        print(f"\nÁtlag előrejelzés: {np.mean(predictions):,.0f} fő")
        print(f"Legnagyobb eltérés: {max(predictions) - min(predictions):,} fő")
        
        return scenarios, predictions
    
    def business_impact(self):
        """
        Üzleti hatás számítás
        """
        print("\n💰 ÜZLETI HATÁS KALKULÁCIÓ")
        print("=" * 50)
        
        # Alapadatok
        avg_visitors = 12000
        spend_per_visitor = 45  # EUR
        daily_revenue = avg_visitors * spend_per_visitor
        
        print(f"Jelenlegi átlag látogatók: {avg_visitors:,} fő/nap")
        print(f"Átlagos költés: {spend_per_visitor} EUR/fő")
        print(f"Napi bevétel: {daily_revenue:,} EUR")
        
        # Modell hasznai
        print(f"\n🎯 MODELL HASZNAI:")
        
        # Marketing optimalizálás
        marketing_improvement = 0.15  # 15%
        marketing_benefit = daily_revenue * 365 * marketing_improvement
        print(f"Marketing optimalizálás (+15%): {marketing_benefit:,.0f} EUR/év")
        
        # Személyzet optimalizálás  
        staff_improvement = 0.20  # 20%
        staff_cost_ratio = 0.12
        staff_benefit = daily_revenue * 365 * staff_cost_ratio * staff_improvement
        print(f"Személyzet optimalizálás (+20%): {staff_benefit:,.0f} EUR/év")
        
        # Készlet optimalizálás
        inventory_improvement = 0.10  # 10%
        inventory_cost_ratio = 0.08
        inventory_benefit = daily_revenue * 365 * inventory_cost_ratio * inventory_improvement
        print(f"Készlet optimalizálás (+10%): {inventory_benefit:,.0f} EUR/év")
        
        total_benefit = marketing_benefit + staff_benefit + inventory_benefit
        print(f"\n💎 ÖSSZESÍTETT HASZON: {total_benefit:,.0f} EUR/év")
        
        # ROI
        implementation_cost = 30000  # EUR (egyszerű verzió)
        roi = (total_benefit - implementation_cost) / implementation_cost * 100
        payback_months = implementation_cost / (total_benefit / 12)
        
        print(f"\n📊 BEFEKTETÉSI MEGTÉRÜLÉS:")
        print(f"Implementációs költség: {implementation_cost:,} EUR")
        print(f"ROI (első év): {roi:.0f}%")
        print(f"Megtérülési idő: {payback_months:.1f} hónap")
        
        if payback_months < 6:
            print("🎉 KIVÁLÓ BEFEKTETÉS!")
        elif payback_months < 12:
            print("✅ JÓ BEFEKTETÉS!")
        else:
            print("⚠️ Megfontolásra érdemes.")
    
    def full_demo(self):
        """
        Teljes demo futtatása
        """
        print("🚀 EGYSZERŰ LINEÁRIS REGRESSZIÓ DEMO")
        print("=" * 60)
        print("Hackathon prezentációhoz optimalizált egyszerű modell\n")
        
        # 1. Adatok betöltése
        data = self.load_data()
        if data is None:
            return False
        
        # 2. Jellemzők előkészítése
        X = self.prepare_simple_features(data)
        y = data['latogatoszam']
        
        # 3. Modell betanítása
        X_train, X_test, y_train, y_test, y_pred_test = self.train_simple_model(X, y)
        
        # 4. Modell magyarázata
        self.explain_model()
        
        # 5. Vizualizációk
        self.create_visualizations(X_test, y_test, y_pred_test)
        
        # 6. Interaktív demo
        scenarios, predictions = self.interactive_prediction()
        
        # 7. Üzleti hatás
        self.business_impact()
        
        print(f"\n🎯 DEMO BEFEJEZVE!")
        print("=" * 30)
        print("✅ Egyszerű, érthető modell")
        print("✅ Valós előrejelzések")
        print("✅ Üzleti értékteremtés")
        print("✅ Prezentációra kész!")
        
        return True

def main():
    """
    Fő demo futtatás
    """
    demo = SimpleLinearDemo()
    success = demo.full_demo()
    
    if success:
        print(f"\n🎪 PREZENTÁCIÓS TIPPEK:")
        print("1. Kezdje az üzleti problémával")
        print("2. Mutassa be az egyszerű modellt")
        print("3. Demonstrálja az előrejelzéseket")
        print("4. Hangsúlyozza az üzleti hasznot")
        print("5. Zárja a következő lépésekkel")
    
if __name__ == "__main__":
    main()

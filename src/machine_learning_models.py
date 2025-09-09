"""
Westend Hackathon - Machine Learning Modellek
=============================================

Ez a modul felelős a látogatószám előrejelző modellek betanításáért,
értékeléséért és összehasonlításáért.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# Sklearn imports
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import (mean_squared_error, mean_absolute_error, 
                           r2_score, mean_absolute_percentage_error)
from sklearn.model_selection import cross_val_score, GridSearchCV
import joblib
import os
from datetime import datetime

# XGBoost import (with fallback)
try:
    from xgboost import XGBRegressor
    XGBOOST_AVAILABLE = True
except ImportError:
    XGBOOST_AVAILABLE = False
    print("⚠️  XGBoost nem elérhető, kihagyva a modellekből")

from data_preparation import DataPreparation

class MLModels:
    def __init__(self):
        self.models = {}
        self.trained_models = {}
        self.results = {}
        self.feature_importance = {}
        
    def initialize_models(self):
        """
        Machine learning modellek inicializálása
        """
        print("🤖 Machine Learning modellek inicializálása...")
        
        self.models = {
            'Linear Regression': LinearRegression(),
            'Ridge Regression': Ridge(alpha=1.0),
            'Lasso Regression': Lasso(alpha=1.0),
            'Random Forest': RandomForestRegressor(
                n_estimators=100, 
                random_state=42,
                n_jobs=-1
            ),
            'Gradient Boosting': GradientBoostingRegressor(
                n_estimators=100,
                random_state=42
            ),
            'Decision Tree': DecisionTreeRegressor(
                random_state=42,
                max_depth=10
            ),
            'K-Nearest Neighbors': KNeighborsRegressor(
                n_neighbors=5
            ),
            'Support Vector Regression': SVR(
                kernel='rbf',
                C=100,
                epsilon=0.1
            )
        }
        
        # XGBoost hozzáadása ha elérhető
        if XGBOOST_AVAILABLE:
            self.models['XGBoost'] = XGBRegressor(
                n_estimators=100,
                random_state=42,
                n_jobs=-1
            )
        
        print(f"✅ {len(self.models)} modell inicializálva")
        return self.models
    
    def train_models(self, X_train, y_train):
        """
        Összes modell betanítása
        
        Args:
            X_train: Tanító jellemzők
            y_train: Tanító célváltozó
        """
        print("🏋️ Modellek betanítása...")
        
        for name, model in self.models.items():
            print(f"  🔄 {name} betanítása...")
            try:
                model.fit(X_train, y_train)
                self.trained_models[name] = model
                print(f"  ✅ {name} sikeresen betanítva")
            except Exception as e:
                print(f"  ❌ {name} betanítása sikertelen: {str(e)}")
        
        print(f"✅ {len(self.trained_models)} modell sikeresen betanítva")
    
    def evaluate_models(self, X_train, y_train, X_test, y_test):
        """
        Modellek értékelése
        
        Args:
            X_train: Tanító jellemzők
            y_train: Tanító célváltozó
            X_test: Teszt jellemzők
            y_test: Teszt célváltozó
        """
        print("📊 Modellek értékelése...")
        
        for name, model in self.trained_models.items():
            print(f"  🔄 {name} értékelése...")
            
            # Előrejelzések
            y_train_pred = model.predict(X_train)
            y_test_pred = model.predict(X_test)
            
            # Metrikák számítása
            train_rmse = np.sqrt(mean_squared_error(y_train, y_train_pred))
            test_rmse = np.sqrt(mean_squared_error(y_test, y_test_pred))
            
            train_mae = mean_absolute_error(y_train, y_train_pred)
            test_mae = mean_absolute_error(y_test, y_test_pred)
            
            train_r2 = r2_score(y_train, y_train_pred)
            test_r2 = r2_score(y_test, y_test_pred)
            
            train_mape = mean_absolute_percentage_error(y_train, y_train_pred) * 100
            test_mape = mean_absolute_percentage_error(y_test, y_test_pred) * 100
            
            # Cross-validation
            try:
                cv_scores = cross_val_score(model, X_train, y_train, 
                                          cv=5, scoring='neg_root_mean_squared_error')
                cv_rmse = -cv_scores.mean()
                cv_std = cv_scores.std()
            except:
                cv_rmse = np.nan
                cv_std = np.nan
            
            # Eredmények tárolása
            self.results[name] = {
                'train_rmse': train_rmse,
                'test_rmse': test_rmse,
                'train_mae': train_mae,
                'test_mae': test_mae,
                'train_r2': train_r2,
                'test_r2': test_r2,
                'train_mape': train_mape,
                'test_mape': test_mape,
                'cv_rmse': cv_rmse,
                'cv_std': cv_std,
                'y_test_pred': y_test_pred,
                'y_train_pred': y_train_pred
            }
            
            print(f"    Test RMSE: {test_rmse:.0f}")
            print(f"    Test R²: {test_r2:.4f}")
            print(f"    Test MAPE: {test_mape:.2f}%")
        
        print("✅ Modellek értékelve")
    
    def get_feature_importance(self, feature_names):
        """
        Jellemző fontosságok kinyerése
        
        Args:
            feature_names: Jellemző nevek listája
        """
        print("🔍 Jellemző fontosságok kinyerése...")
        
        for name, model in self.trained_models.items():
            try:
                if hasattr(model, 'feature_importances_'):
                    # Tree-based modellek
                    importance = model.feature_importances_
                elif hasattr(model, 'coef_'):
                    # Linear modellek
                    importance = np.abs(model.coef_)
                else:
                    continue
                
                # Fontosságok DataFrame-be
                feature_imp = pd.DataFrame({
                    'feature': feature_names,
                    'importance': importance
                }).sort_values('importance', ascending=False)
                
                self.feature_importance[name] = feature_imp
                
            except Exception as e:
                print(f"  ⚠️ {name}: {str(e)}")
        
        print(f"✅ {len(self.feature_importance)} modell jellemző fontossága kinyerve")
    
    def print_results_summary(self):
        """
        Eredmények összefoglalójának kiírása
        """
        print("\n" + "="*80)
        print("🏆 MODELL ÉRTÉKELÉSI EREDMÉNYEK")
        print("="*80)
        
        # Eredmények DataFrame-be
        results_df = pd.DataFrame(self.results).T
        results_df = results_df.sort_values('test_rmse')
        
        print(f"{'Modell':<25} {'Test RMSE':<12} {'Test R²':<10} {'Test MAPE':<12} {'CV RMSE':<12}")
        print("-" * 80)
        
        for model_name in results_df.index:
            result = self.results[model_name]
            print(f"{model_name:<25} "
                  f"{result['test_rmse']:<12.0f} "
                  f"{result['test_r2']:<10.4f} "
                  f"{result['test_mape']:<12.2f}% "
                  f"{result['cv_rmse']:<12.0f}")
        
        # Legjobb modell
        best_model = results_df.index[0]
        print(f"\n🥇 Legjobb modell: {best_model}")
        print(f"   Test RMSE: {self.results[best_model]['test_rmse']:.0f}")
        print(f"   Test R²: {self.results[best_model]['test_r2']:.4f}")
        print(f"   Test MAPE: {self.results[best_model]['test_mape']:.2f}%")
        
        return best_model
    
    def create_visualizations(self, y_test, feature_names):
        """
        Vizualizációk létrehozása
        
        Args:
            y_test: Valós teszt értékek
            feature_names: Jellemző nevek
        """
        print("📈 Vizualizációk létrehozása...")
        
        # 1. Modell teljesítmény összehasonlítás
        self._plot_model_comparison()
        
        # 2. Előrejelzés vs Valóság
        self._plot_predictions_vs_actual(y_test)
        
        # 3. Jellemző fontosságok
        self._plot_feature_importance()
        
        # 4. Residual plotok
        self._plot_residuals(y_test)
        
        print("✅ Vizualizációk létrehozva")
    
    def _plot_model_comparison(self):
        """Modell teljesítmény összehasonlítás"""
        
        # Matplotlib verzió
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        models = list(self.results.keys())
        test_rmse = [self.results[m]['test_rmse'] for m in models]
        test_r2 = [self.results[m]['test_r2'] for m in models]
        test_mape = [self.results[m]['test_mape'] for m in models]
        cv_rmse = [self.results[m]['cv_rmse'] for m in models]
        
        # RMSE
        axes[0,0].bar(models, test_rmse, color='skyblue')
        axes[0,0].set_title('Test RMSE Összehasonlítás')
        axes[0,0].set_ylabel('RMSE')
        axes[0,0].tick_params(axis='x', rotation=45)
        
        # R²
        axes[0,1].bar(models, test_r2, color='lightgreen')
        axes[0,1].set_title('Test R² Összehasonlítás')
        axes[0,1].set_ylabel('R²')
        axes[0,1].tick_params(axis='x', rotation=45)
        
        # MAPE
        axes[1,0].bar(models, test_mape, color='salmon')
        axes[1,0].set_title('Test MAPE Összehasonlítás')
        axes[1,0].set_ylabel('MAPE (%)')
        axes[1,0].tick_params(axis='x', rotation=45)
        
        # CV RMSE
        valid_cv = [(m, cv) for m, cv in zip(models, cv_rmse) if not np.isnan(cv)]
        if valid_cv:
            cv_models, cv_values = zip(*valid_cv)
            axes[1,1].bar(cv_models, cv_values, color='orange')
        axes[1,1].set_title('Cross-Validation RMSE')
        axes[1,1].set_ylabel('CV RMSE')
        axes[1,1].tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        
        # Mentés
        os.makedirs('outputs', exist_ok=True)
        plt.savefig('outputs/model_comparison.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def _plot_predictions_vs_actual(self, y_test):
        """Előrejelzés vs Valóság plotok"""
        
        # Top 4 modell kiválasztása
        sorted_models = sorted(self.results.items(), 
                             key=lambda x: x[1]['test_rmse'])[:4]
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        axes = axes.ravel()
        
        for i, (model_name, results) in enumerate(sorted_models):
            y_pred = results['y_test_pred']
            
            axes[i].scatter(y_test, y_pred, alpha=0.6)
            axes[i].plot([y_test.min(), y_test.max()], 
                        [y_test.min(), y_test.max()], 'r--', lw=2)
            axes[i].set_xlabel('Valós Látogatószám')
            axes[i].set_ylabel('Előrejelzett Látogatószám')
            axes[i].set_title(f'{model_name}\nR² = {results["test_r2"]:.4f}')
            axes[i].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('outputs/predictions_vs_actual.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def _plot_feature_importance(self):
        """Jellemző fontosságok vizualizálása"""
        
        if not self.feature_importance:
            return
        
        # Top 3 modell feature importance
        top_models = list(self.feature_importance.keys())[:3]
        
        fig, axes = plt.subplots(1, len(top_models), figsize=(20, 6))
        if len(top_models) == 1:
            axes = [axes]
        
        for i, model_name in enumerate(top_models):
            feature_imp = self.feature_importance[model_name].head(15)
            
            axes[i].barh(feature_imp['feature'], feature_imp['importance'])
            axes[i].set_title(f'{model_name}\nTop 15 Jellemző')
            axes[i].set_xlabel('Fontosság')
            axes[i].invert_yaxis()
        
        plt.tight_layout()
        plt.savefig('outputs/feature_importance.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def _plot_residuals(self, y_test):
        """Residual plotok"""
        
        # Legjobb modell residual analízise
        best_model = min(self.results.items(), key=lambda x: x[1]['test_rmse'])
        model_name, results = best_model
        
        y_pred = results['y_test_pred']
        residuals = y_test - y_pred
        
        fig, axes = plt.subplots(1, 2, figsize=(15, 6))
        
        # Residuals vs Predicted
        axes[0].scatter(y_pred, residuals, alpha=0.6)
        axes[0].axhline(y=0, color='r', linestyle='--')
        axes[0].set_xlabel('Előrejelzett Értékek')
        axes[0].set_ylabel('Residuals')
        axes[0].set_title(f'{model_name} - Residuals vs Predicted')
        axes[0].grid(True, alpha=0.3)
        
        # Residuals histogram
        axes[1].hist(residuals, bins=30, alpha=0.7, color='skyblue')
        axes[1].set_xlabel('Residuals')
        axes[1].set_ylabel('Gyakoriság')
        axes[1].set_title(f'{model_name} - Residuals Eloszlása')
        axes[1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('outputs/residual_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def save_models(self, best_model_name=None):
        """
        Modellek mentése
        
        Args:
            best_model_name: Legjobb modell neve (ha None, akkor az összes)
        """
        print("💾 Modellek mentése...")
        
        os.makedirs('models', exist_ok=True)
        
        if best_model_name:
            # Csak a legjobb modell mentése
            model = self.trained_models[best_model_name]
            filename = f'models/best_model_{best_model_name.replace(" ", "_").lower()}.joblib'
            joblib.dump(model, filename)
            print(f"✅ Legjobb modell mentve: {filename}")
        else:
            # Összes modell mentése
            for name, model in self.trained_models.items():
                filename = f'models/model_{name.replace(" ", "_").lower()}.joblib'
                joblib.dump(model, filename)
            print(f"✅ {len(self.trained_models)} modell mentve")
        
        # Eredmények mentése
        results_df = pd.DataFrame(self.results).T
        results_df.to_csv('outputs/model_results.csv')
        print("✅ Eredmények mentve: outputs/model_results.csv")
    
    def full_pipeline(self):
        """
        Teljes ML pipeline futtatása
        
        Returns:
            tuple: (best_model_name, results)
        """
        print("🚀 Teljes Machine Learning Pipeline indítása...\n")
        
        # 1. Adatok előkészítése
        data_prep = DataPreparation()
        X_train, X_test, y_train, y_test, feature_names, summary = data_prep.full_pipeline()
        
        print("\n" + "="*50)
        print("🤖 MACHINE LEARNING MODELLEK")
        print("="*50)
        
        # 2. Modellek inicializálása
        self.initialize_models()
        
        # 3. Modellek betanítása
        self.train_models(X_train, y_train)
        
        # 4. Modellek értékelése
        self.evaluate_models(X_train, y_train, X_test, y_test)
        
        # 5. Jellemző fontosságok
        self.get_feature_importance(feature_names)
        
        # 6. Eredmények összefoglalása
        best_model_name = self.print_results_summary()
        
        # 7. Vizualizációk
        self.create_visualizations(y_test, feature_names)
        
        # 8. Modellek mentése
        self.save_models(best_model_name)
        
        print(f"\n🎯 Machine Learning Pipeline befejezve!")
        print(f"🏆 Legjobb modell: {best_model_name}")
        
        return best_model_name, self.results

# Példa használat
if __name__ == "__main__":
    # ML pipeline futtatása
    ml_models = MLModels()
    best_model, results = ml_models.full_pipeline()
    
    print("\n🎉 Sikeres befejezés!")
    print(f"Legjobb modell: {best_model}")

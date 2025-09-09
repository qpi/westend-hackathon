"""
Westend Hackathon - Software Architecture Diagram Generator
==========================================================

Szoftver architektúra diagram generálása a látogatószám előrejelző rendszerhez.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, ConnectionPatch, Rectangle
import numpy as np

def create_software_architecture():
    """Szoftver architektúra diagram létrehozása"""
    
    fig, ax = plt.subplots(1, 1, figsize=(18, 14))
    ax.set_xlim(0, 22)
    ax.set_ylim(0, 16)
    ax.axis('off')
    
    # Színek definiálása
    colors = {
        'frontend': '#E3F2FD',          # Világoskék
        'backend': '#FFF3E0',           # Világos narancssárga
        'data': '#F1F8E9',              # Világoszöld
        'ml': '#FCE4EC',                # Világos rózsaszín
        'external': '#F3E5F5',          # Világos lila
        'infrastructure': '#FFEBEE'     # Világos piros
    }
    
    # FRONTEND RÉTEG
    frontend_box = FancyBboxPatch((1, 13), 20, 2.5,
                                 boxstyle="round,pad=0.1", 
                                 facecolor=colors['frontend'], 
                                 edgecolor='black', linewidth=2)
    ax.add_patch(frontend_box)
    ax.text(11, 14.7, 'FRONTEND RÉTEG (Presentation Layer)', 
            ha='center', va='center', fontsize=16, fontweight='bold')
    
    # Frontend komponensek
    frontend_components = [
        {'name': 'Streamlit\nWeb Interface', 'pos': (4, 14), 'desc': 'Interaktív UI\nDashboard'},
        {'name': 'Plotly\nVisualization', 'pos': (8, 14), 'desc': 'Grafikonok\nChartok'},
        {'name': 'Input Forms', 'pos': (12, 14), 'desc': 'Paraméter\nBeállítások'},
        {'name': 'Real-time\nPredictions', 'pos': (16, 14), 'desc': 'Élő\nElőrejelzések'},
        {'name': 'Export/\nDownload', 'pos': (19, 14), 'desc': 'CSV/PNG\nLetöltés'}
    ]
    
    for comp in frontend_components:
        box = FancyBboxPatch((comp['pos'][0]-0.8, comp['pos'][1]-0.6), 1.6, 1.2,
                            boxstyle="round,pad=0.05", 
                            facecolor='white', 
                            edgecolor='blue', linewidth=1)
        ax.add_patch(box)
        ax.text(comp['pos'][0], comp['pos'][1]+0.2, comp['name'], 
                ha='center', va='center', fontsize=9, fontweight='bold')
        ax.text(comp['pos'][0], comp['pos'][1]-0.3, comp['desc'], 
                ha='center', va='center', fontsize=7)
    
    # APPLICATION LOGIC RÉTEG
    app_logic_box = FancyBboxPatch((1, 10), 20, 2.5,
                                  boxstyle="round,pad=0.1", 
                                  facecolor=colors['backend'], 
                                  edgecolor='black', linewidth=2)
    ax.add_patch(app_logic_box)
    ax.text(11, 11.7, 'APPLICATION LOGIC RÉTEG (Business Layer)', 
            ha='center', va='center', fontsize=16, fontweight='bold')
    
    # Application Logic komponensek
    app_components = [
        {'name': 'Prediction\nController', 'pos': (4, 11), 'desc': 'Előrejelzési\nLogika'},
        {'name': 'Data\nValidator', 'pos': (8, 11), 'desc': 'Input\nValidáció'},
        {'name': 'Feature\nEngineering', 'pos': (12, 11), 'desc': 'Jellemző\nGenerálás'},
        {'name': 'Model\nManager', 'pos': (16, 11), 'desc': 'Modell\nKezelés'},
        {'name': 'Cache\nManager', 'pos': (19, 11), 'desc': 'Gyorsítótár\nKezelés'}
    ]
    
    for comp in app_components:
        box = FancyBboxPatch((comp['pos'][0]-0.8, comp['pos'][1]-0.6), 1.6, 1.2,
                            boxstyle="round,pad=0.05", 
                            facecolor='white', 
                            edgecolor='orange', linewidth=1)
        ax.add_patch(box)
        ax.text(comp['pos'][0], comp['pos'][1]+0.2, comp['name'], 
                ha='center', va='center', fontsize=9, fontweight='bold')
        ax.text(comp['pos'][0], comp['pos'][1]-0.3, comp['desc'], 
                ha='center', va='center', fontsize=7)
    
    # MACHINE LEARNING RÉTEG
    ml_box = FancyBboxPatch((1, 7), 20, 2.5,
                           boxstyle="round,pad=0.1", 
                           facecolor=colors['ml'], 
                           edgecolor='black', linewidth=2)
    ax.add_patch(ml_box)
    ax.text(11, 8.7, 'MACHINE LEARNING RÉTEG (AI Engine)', 
            ha='center', va='center', fontsize=16, fontweight='bold')
    
    # ML komponensek
    ml_components = [
        {'name': 'Random Forest\nRegressor', 'pos': (4, 8), 'desc': 'Fő Előrejelző\nModell'},
        {'name': 'Linear\nRegression', 'pos': (7, 8), 'desc': 'Backup\nModell'},
        {'name': 'XGBoost\nRegressor', 'pos': (10, 8), 'desc': 'Alternatív\nModell'},
        {'name': 'Model\nEvaluator', 'pos': (13, 8), 'desc': 'Teljesítmény\nMérés'},
        {'name': 'Cross\nValidation', 'pos': (16, 8), 'desc': 'Modell\nValidáció'},
        {'name': 'Hyperparameter\nTuning', 'pos': (19, 8), 'desc': 'Paraméter\nOptimalizálás'}
    ]
    
    for comp in ml_components:
        box = FancyBboxPatch((comp['pos'][0]-0.7, comp['pos'][1]-0.6), 1.4, 1.2,
                            boxstyle="round,pad=0.05", 
                            facecolor='white', 
                            edgecolor='purple', linewidth=1)
        ax.add_patch(box)
        ax.text(comp['pos'][0], comp['pos'][1]+0.2, comp['name'], 
                ha='center', va='center', fontsize=8, fontweight='bold')
        ax.text(comp['pos'][0], comp['pos'][1]-0.3, comp['desc'], 
                ha='center', va='center', fontsize=6)
    
    # DATA ACCESS RÉTEG
    data_box = FancyBboxPatch((1, 4), 20, 2.5,
                             boxstyle="round,pad=0.1", 
                             facecolor=colors['data'], 
                             edgecolor='black', linewidth=2)
    ax.add_patch(data_box)
    ax.text(11, 5.7, 'DATA ACCESS RÉTEG (Data Layer)', 
            ha='center', va='center', fontsize=16, fontweight='bold')
    
    # Data Access komponensek
    data_components = [
        {'name': 'CSV\nReader', 'pos': (4, 5), 'desc': 'Fájl\nOlvasás'},
        {'name': 'Pandas\nDataFrame', 'pos': (7, 5), 'desc': 'Adat\nManipuláció'},
        {'name': 'Data\nCleaner', 'pos': (10, 5), 'desc': 'Adat\nTisztítás'},
        {'name': 'Feature\nStore', 'pos': (13, 5), 'desc': 'Jellemző\nTárolás'},
        {'name': 'Model\nPersistence', 'pos': (16, 5), 'desc': 'Modell\nMentés'},
        {'name': 'Cache\nStorage', 'pos': (19, 5), 'desc': 'Gyorsítótár\nTárolás'}
    ]
    
    for comp in data_components:
        box = FancyBboxPatch((comp['pos'][0]-0.7, comp['pos'][1]-0.6), 1.4, 1.2,
                            boxstyle="round,pad=0.05", 
                            facecolor='white', 
                            edgecolor='green', linewidth=1)
        ax.add_patch(box)
        ax.text(comp['pos'][0], comp['pos'][1]+0.2, comp['name'], 
                ha='center', va='center', fontsize=8, fontweight='bold')
        ax.text(comp['pos'][0], comp['pos'][1]-0.3, comp['desc'], 
                ha='center', va='center', fontsize=6)
    
    # EXTERNAL SERVICES
    external_box = FancyBboxPatch((1, 1), 10, 2.5,
                                 boxstyle="round,pad=0.1", 
                                 facecolor=colors['external'], 
                                 edgecolor='black', linewidth=2)
    ax.add_patch(external_box)
    ax.text(6, 2.7, 'KÜLSŐ SZOLGÁLTATÁSOK', 
            ha='center', va='center', fontsize=14, fontweight='bold')
    
    external_services = [
        {'name': 'Weather\nAPI', 'pos': (3, 2), 'desc': 'Időjárási\nAdatok'},
        {'name': 'Calendar\nAPI', 'pos': (6, 2), 'desc': 'Ünnepnap\nInformációk'},
        {'name': 'File\nSystem', 'pos': (9, 2), 'desc': 'Helyi\nFájlok'}
    ]
    
    for service in external_services:
        box = FancyBboxPatch((service['pos'][0]-0.8, service['pos'][1]-0.6), 1.6, 1.2,
                            boxstyle="round,pad=0.05", 
                            facecolor='white', 
                            edgecolor='purple', linewidth=1)
        ax.add_patch(box)
        ax.text(service['pos'][0], service['pos'][1]+0.2, service['name'], 
                ha='center', va='center', fontsize=9, fontweight='bold')
        ax.text(service['pos'][0], service['pos'][1]-0.3, service['desc'], 
                ha='center', va='center', fontsize=7)
    
    # INFRASTRUCTURE
    infra_box = FancyBboxPatch((12, 1), 9, 2.5,
                              boxstyle="round,pad=0.1", 
                              facecolor=colors['infrastructure'], 
                              edgecolor='black', linewidth=2)
    ax.add_patch(infra_box)
    ax.text(16.5, 2.7, 'INFRASTRUKTÚRA', 
            ha='center', va='center', fontsize=14, fontweight='bold')
    
    infra_components = [
        {'name': 'Python 3.11+', 'pos': (14, 2), 'desc': 'Runtime\nKörnyezet'},
        {'name': 'Streamlit\nServer', 'pos': (16.5, 2), 'desc': 'Web\nSzerver'},
        {'name': 'Local\nStorage', 'pos': (19, 2), 'desc': 'Helyi\nTárolás'}
    ]
    
    for infra in infra_components:
        box = FancyBboxPatch((infra['pos'][0]-0.8, infra['pos'][1]-0.6), 1.6, 1.2,
                            boxstyle="round,pad=0.05", 
                            facecolor='white', 
                            edgecolor='red', linewidth=1)
        ax.add_patch(box)
        ax.text(infra['pos'][0], infra['pos'][1]+0.2, infra['name'], 
                ha='center', va='center', fontsize=9, fontweight='bold')
        ax.text(infra['pos'][0], infra['pos'][1]-0.3, infra['desc'], 
                ha='center', va='center', fontsize=7)
    
    # KAPCSOLATOK - Nyilak a rétegek között
    layer_connections = [
        # Frontend -> Application Logic
        ((11, 13), (11, 12.5)),
        # Application Logic -> ML Layer
        ((11, 10), (11, 9.5)),
        # ML Layer -> Data Access
        ((11, 7), (11, 6.5)),
        # Data Access -> External Services
        ((6, 4), (6, 3.5)),
        # Data Access -> Infrastructure
        ((16, 4), (16, 3.5))
    ]
    
    for start, end in layer_connections:
        arrow = ConnectionPatch(start, end, "data", "data",
                              arrowstyle="<->", shrinkA=5, shrinkB=5,
                              mutation_scale=20, fc="black", lw=3)
        ax.add_patch(arrow)
    
    # Cím és alcím
    ax.text(11, 15.7, 'WESTEND MALL - LÁTOGATÓSZÁM ELŐREJELZŐ RENDSZER', 
            ha='center', va='center', fontsize=20, fontweight='bold')
    ax.text(11, 15.3, 'Szoftver Architektúra Diagram (Layered Architecture Pattern)', 
            ha='center', va='center', fontsize=14, style='italic')
    
    # Jelmagyarázat
    legend_elements = [
        mpatches.Patch(color=colors['frontend'], label='Frontend Réteg'),
        mpatches.Patch(color=colors['backend'], label='Alkalmazás Logika'),
        mpatches.Patch(color=colors['ml'], label='ML Engine'),
        mpatches.Patch(color=colors['data'], label='Adat Hozzáférés'),
        mpatches.Patch(color=colors['external'], label='Külső Szolgáltatások'),
        mpatches.Patch(color=colors['infrastructure'], label='Infrastruktúra')
    ]
    ax.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(0.02, 0.98))
    
    # Technológiai stack annotáció
    tech_stack = """
    TECHNOLÓGIAI STACK:
    • Python 3.11+
    • Streamlit (Web Framework)
    • Scikit-learn (ML Library)
    • Pandas (Data Processing)
    • Plotly (Visualization)
    • Joblib (Model Persistence)
    • NumPy (Numerical Computing)
    """
    ax.text(0.5, 0.5, tech_stack, ha='left', va='bottom', fontsize=9,
            bbox=dict(boxstyle="round,pad=0.5", facecolor='lightyellow', alpha=0.8))
    
    plt.tight_layout()
    plt.savefig('docs/software_architecture.png', dpi=300, bbox_inches='tight')
    plt.savefig('outputs/software_architecture.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print("✅ Szoftver architektúra diagram elkészült!")
    print("📁 Mentve: docs/software_architecture.png")

if __name__ == "__main__":
    create_software_architecture()

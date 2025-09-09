"""
Westend Hackathon - Data Flow Diagram Generator
==============================================

Adatáramlási diagram generálása a látogatószám előrejelző rendszerhez.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, ConnectionPatch
import numpy as np

def create_dataflow_diagram():
    """Adatáramlási diagram létrehozása"""
    
    fig, ax = plt.subplots(1, 1, figsize=(16, 12))
    ax.set_xlim(0, 20)
    ax.set_ylim(0, 15)
    ax.axis('off')
    
    # Színek definiálása
    colors = {
        'data_source': '#E3F2FD',      # Világoskék
        'processing': '#FFF3E0',        # Világos narancssárga
        'storage': '#F1F8E9',           # Világoszöld
        'ml_model': '#FCE4EC',          # Világos rózsaszín
        'output': '#F3E5F5',            # Világos lila
        'user': '#FFEBEE'               # Világos piros
    }
    
    # 1. ADATFORRÁSOK (Felső sor)
    data_sources = [
        {'name': 'Történelmi\nLátogatószám\nAdatok', 'pos': (2, 13), 'color': colors['data_source']},
        {'name': 'Időjárási\nAdatok\n(API)', 'pos': (6, 13), 'color': colors['data_source']},
        {'name': 'Naptári\nAdatok\n(Ünnepek)', 'pos': (10, 13), 'color': colors['data_source']},
        {'name': 'Marketing\nKampány\nAdatok', 'pos': (14, 13), 'color': colors['data_source']},
        {'name': 'Szezonális\nTrendek', 'pos': (18, 13), 'color': colors['data_source']}
    ]
    
    for source in data_sources:
        box = FancyBboxPatch((source['pos'][0]-0.8, source['pos'][1]-0.7), 1.6, 1.4,
                            boxstyle="round,pad=0.1", 
                            facecolor=source['color'], 
                            edgecolor='black', linewidth=1)
        ax.add_patch(box)
        ax.text(source['pos'][0], source['pos'][1], source['name'], 
                ha='center', va='center', fontsize=9, fontweight='bold')
    
    # 2. ADATGYŰJTÉS ÉS ELŐKÉSZÍTÉS (Második sor)
    preprocessing_box = FancyBboxPatch((4, 10), 12, 1.5,
                                      boxstyle="round,pad=0.1", 
                                      facecolor=colors['processing'], 
                                      edgecolor='black', linewidth=2)
    ax.add_patch(preprocessing_box)
    ax.text(10, 10.75, 'ADATGYŰJTÉS ÉS ELŐKÉSZÍTÉS', 
            ha='center', va='center', fontsize=12, fontweight='bold')
    ax.text(10, 10.25, '• Adatok normalizálása • Feature Engineering • Hiányzó értékek kezelése\n• Outlier detektálás • Kategorikus kódolás • Idősor előkészítés', 
            ha='center', va='center', fontsize=9)
    
    # 3. ADATTÁROLÁS (Harmadik sor)
    storage_elements = [
        {'name': 'Nyers Adatok\n(CSV/Excel)', 'pos': (4, 7.5), 'color': colors['storage']},
        {'name': 'Tisztított\nAdatbázis\n(Pandas)', 'pos': (10, 7.5), 'color': colors['storage']},
        {'name': 'Feature Store\n(Engineered\nFeatures)', 'pos': (16, 7.5), 'color': colors['storage']}
    ]
    
    for storage in storage_elements:
        box = FancyBboxPatch((storage['pos'][0]-1.2, storage['pos'][1]-0.8), 2.4, 1.6,
                            boxstyle="round,pad=0.1", 
                            facecolor=storage['color'], 
                            edgecolor='black', linewidth=1)
        ax.add_patch(box)
        ax.text(storage['pos'][0], storage['pos'][1], storage['name'], 
                ha='center', va='center', fontsize=10, fontweight='bold')
    
    # 4. GÉPI TANULÁSI PIPELINE (Negyedik sor)
    ml_pipeline = FancyBboxPatch((2, 4.5), 16, 2,
                                boxstyle="round,pad=0.1", 
                                facecolor=colors['ml_model'], 
                                edgecolor='black', linewidth=2)
    ax.add_patch(ml_pipeline)
    ax.text(10, 5.8, 'GÉPI TANULÁSI PIPELINE', 
            ha='center', va='center', fontsize=14, fontweight='bold')
    
    # ML komponensek
    ml_components = [
        {'name': 'Train/Test\nSplit', 'pos': (4, 5)},
        {'name': 'Random Forest\nRegressor', 'pos': (8, 5)},
        {'name': 'Model\nValidation', 'pos': (12, 5)},
        {'name': 'Hyperparameter\nTuning', 'pos': (16, 5)}
    ]
    
    for comp in ml_components:
        ax.text(comp['pos'][0], comp['pos'][1], comp['name'], 
                ha='center', va='center', fontsize=9, fontweight='bold',
                bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.8))
    
    # 5. MODELL TÁROLÁS (Ötödik sor)
    model_storage = FancyBboxPatch((8, 2), 4, 1.2,
                                  boxstyle="round,pad=0.1", 
                                  facecolor=colors['storage'], 
                                  edgecolor='black', linewidth=2)
    ax.add_patch(model_storage)
    ax.text(10, 2.6, 'BETANÍTOTT MODELL', 
            ha='center', va='center', fontsize=12, fontweight='bold')
    ax.text(10, 2.2, '(Random Forest .joblib)', 
            ha='center', va='center', fontsize=10)
    
    # 6. ALKALMAZÁSI RÉTEG (Alsó sor)
    app_components = [
        {'name': 'Streamlit\nWeb App', 'pos': (4, 0.5), 'color': colors['output']},
        {'name': 'Előrejelzési\nAPI', 'pos': (10, 0.5), 'color': colors['output']},
        {'name': 'Vizualizáció\n& Reporting', 'pos': (16, 0.5), 'color': colors['output']}
    ]
    
    for comp in app_components:
        box = FancyBboxPatch((comp['pos'][0]-1.2, comp['pos'][1]-0.5), 2.4, 1,
                            boxstyle="round,pad=0.1", 
                            facecolor=comp['color'], 
                            edgecolor='black', linewidth=1)
        ax.add_patch(box)
        ax.text(comp['pos'][0], comp['pos'][1], comp['name'], 
                ha='center', va='center', fontsize=10, fontweight='bold')
    
    # NYILAK - Adatáramlás
    arrows = [
        # Adatforrásokból előkészítésbe
        ((2, 12.3), (6, 11.5)),
        ((6, 12.3), (8, 11.5)),
        ((10, 12.3), (10, 11.5)),
        ((14, 12.3), (12, 11.5)),
        ((18, 12.3), (14, 11.5)),
        
        # Előkészítésből tárolásba
        ((7, 9.5), (4, 8.3)),
        ((10, 9.5), (10, 8.3)),
        ((13, 9.5), (16, 8.3)),
        
        # Tárolásból ML pipeline-ba
        ((4, 6.7), (4, 6.5)),
        ((10, 6.7), (10, 6.5)),
        ((16, 6.7), (16, 6.5)),
        
        # ML pipeline-ból modell tárolásba
        ((10, 4.5), (10, 3.2)),
        
        # Modell tárolásból alkalmazásokba
        ((8.8, 2), (4, 1)),
        ((10, 2), (10, 1)),
        ((11.2, 2), (16, 1))
    ]
    
    for start, end in arrows:
        arrow = ConnectionPatch(start, end, "data", "data",
                              arrowstyle="->", shrinkA=5, shrinkB=5,
                              mutation_scale=20, fc="black", lw=2)
        ax.add_patch(arrow)
    
    # Cím és metrikák
    ax.text(10, 14.5, 'WESTEND MALL - LÁTOGATÓSZÁM ELŐREJELZŐ RENDSZER', 
            ha='center', va='center', fontsize=18, fontweight='bold')
    ax.text(10, 14, 'Adatáramlási Diagram (Data Flow Architecture)', 
            ha='center', va='center', fontsize=14, style='italic')
    
    # Jelmagyarázat
    legend_elements = [
        mpatches.Patch(color=colors['data_source'], label='Adatforrások'),
        mpatches.Patch(color=colors['processing'], label='Adatfeldolgozás'),
        mpatches.Patch(color=colors['storage'], label='Adattárolás'),
        mpatches.Patch(color=colors['ml_model'], label='ML Pipeline'),
        mpatches.Patch(color=colors['output'], label='Kimeneti Réteg')
    ]
    ax.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(0.98, 0.98))
    
    plt.tight_layout()
    plt.savefig('docs/dataflow_diagram.png', dpi=300, bbox_inches='tight')
    plt.savefig('outputs/dataflow_diagram.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print("✅ Adatáramlási diagram elkészült!")
    print("📁 Mentve: docs/dataflow_diagram.png")

if __name__ == "__main__":
    create_dataflow_diagram()

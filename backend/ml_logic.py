import pandas as pd
from ydata_profiling import ProfileReport
from pycaret.classification import setup, compare_models, pull, save_model
import os

def generate_profile_report(df: pd.DataFrame, title: str) -> str:
    """Generate interactive EDA report"""
    profile = ProfileReport(
        df, 
        title=title,
        explorative=True,
        correlations={"auto": {"calculate": True}},
        missing_diagrams={"heatmap": True}
    )
    return profile.to_html()

def train_classification_model(df: pd.DataFrame, target_column: str):
    """Automated machine learning pipeline"""
    os.makedirs('models', exist_ok=True)
    
    exp = setup(
        data=df,
        target=target_column,
        session_id=123,
        silent=True,
        verbose=False
    )
    
    best_model = compare_models(
        fold=5,  
        sort='Accuracy'  
    )
    
    
    results = pull()
    
    
    save_model(best_model, 'models/best_model')
    
    return best_model, results
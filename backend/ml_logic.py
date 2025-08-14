import pandas as pd
from ydata_profiling import ProfileReport
from pycaret.classification import setup, compare_models, pull, save_model, finalize_model
from pathlib import Path
from typing import Tuple, Optional, Any
from datetime import datetime
import logging

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

def train_classification_model(
    df: pd.DataFrame,
    target_column: str,
    sort_metric: str = "Accuracy",
) -> Tuple[Optional[Any], Optional[pd.DataFrame]]:
    """Automated machine learning pipeline for classification."""
    models_dir = Path("models")
    models_dir.mkdir(exist_ok=True)

    try:
        logging.info("Setting up PyCaret experiment...")
        setup(
            data=df,
            target=target_column,
            session_id=123,
            silent=True,  # Suppresses user confirmation prompts
            verbose=False,  # Suppresses detailed output during setup
        )

        logging.info(f"Comparing models based on {sort_metric}...")
        best_model: Optional[Any] = compare_models(fold=5, sort=sort_metric)

        if best_model is None:
            logging.warning("compare_models did not return a best model.")
            return None, None

        logging.info(f"Best model found: {best_model}")

        logging.info("Finalizing the best model on the full dataset...")
        final_model = finalize_model(best_model)
        logging.info(f"Finalized model: {final_model}")

        results: pd.DataFrame = pull()

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        model_name = f"best_model_{timestamp}"
        save_model(final_model, str(models_dir / model_name))
        # save_model adds the .pkl extension automatically
        logging.info(f"Model saved to {models_dir / (model_name + '.pkl')}")

        return final_model, results

    except Exception as e:
        logging.error(f"An error occurred during model training: {e}")
        return None, None
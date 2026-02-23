"""
stage9A_geometric_risk_modeling.bayesian_model.bayesian_evaluation

Evaluation entrypoint specific to the Bayesian Model.
"""
import pandas as pd
from .bayesian_kde_model import BayesianKDEModel
from ..common.evaluation_metrics import compute_metrics
from ..common.bootstrap_validation import evaluate_bootstrap_stability
from ..common.noise_injection import evaluate_noise_robustness

def evaluate_baseline(df: pd.DataFrame):
    model = BayesianKDEModel()
    model.fit(df)
    preds = model.predict_proba(df)
    return compute_metrics(df['Condition'].values, preds)

def evaluate_bootstrap(df: pd.DataFrame, iterations: int):
    return evaluate_bootstrap_stability(BayesianKDEModel, df, iterations)

def evaluate_noise(df: pd.DataFrame, noise_level: float):
    return evaluate_noise_robustness(BayesianKDEModel, df, noise_level)

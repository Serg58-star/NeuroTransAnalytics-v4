"""
stage9A_geometric_risk_modeling.bayesian_model.bayesian_kde_model

Implements the Bayesian Risk Mapping Model: P(Condition | Position in 3D).
Hypothesis: Risk is locally topology-dependent.
"""
import pandas as pd
import numpy as np
from scipy.stats import gaussian_kde

class BayesianKDEModel:
    def __init__(self):
        self.kde_pos = None
        self.kde_all = None
        self.prior_pos = 0.0

    def fit(self, df: pd.DataFrame):
        X_all = df[['ΔSpeed', 'ΔLateral', 'ΔTone']].values.T 
        X_pos = df[df['Condition'] == 1][['ΔSpeed', 'ΔLateral', 'ΔTone']].values.T
        
        self.prior_pos = len(df[df['Condition'] == 1]) / len(df)
        
        if X_pos.shape[1] > 3:
             self.kde_pos = gaussian_kde(X_pos)
        else:
             self.kde_pos = None
             
        self.kde_all = gaussian_kde(X_all)
        
    def predict_proba(self, df: pd.DataFrame) -> np.ndarray:
        if self.kde_pos is None or self.prior_pos == 0:
             return np.zeros(len(df))
             
        X = df[['ΔSpeed', 'ΔLateral', 'ΔTone']].values.T
        
        p_x_given_1 = self.kde_pos(X)
        p_x_all = self.kde_all(X)
        
        p_x_all = np.clip(p_x_all, a_min=1e-10, a_max=None)
        probs = (p_x_given_1 * self.prior_pos) / p_x_all
        
        return np.clip(probs, 0.0, 1.0)

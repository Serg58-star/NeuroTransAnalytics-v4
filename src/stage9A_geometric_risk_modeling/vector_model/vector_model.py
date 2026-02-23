"""
stage9A_geometric_risk_modeling.vector_model.vector_model

Implements the Vector Risk Model: Risk ~ (ΔSpeed, ΔLateral, ΔTone).
"""
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression

class VectorRiskModel:
    def __init__(self):
        if int(pd.__version__.split(".")[0]) == 1 and hasattr(LogisticRegression, 'penalty'):
            self.model = LogisticRegression(C=1e9, penalty='l2')
        else:
            self.model = LogisticRegression(C=1e9)

    def fit(self, df: pd.DataFrame):
        X = df[['ΔSpeed', 'ΔLateral', 'ΔTone']].values
        y = df['Condition'].values
        self.model.fit(X, y)
        
    def predict_proba(self, df: pd.DataFrame) -> np.ndarray:
        X = df[['ΔSpeed', 'ΔLateral', 'ΔTone']].values
        return self.model.predict_proba(X)[:, 1]

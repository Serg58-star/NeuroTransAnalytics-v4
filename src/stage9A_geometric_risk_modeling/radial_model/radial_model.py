"""
stage9A_geometric_risk_modeling.radial_model.radial_model

Implements the Radial Risk Model: Risk ~ Mahalanobis Distance.
"""
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression

class RadialRiskModel:
    def __init__(self):
        # We want unregularized logistic regression for the distance
        if int(pd.__version__.split(".")[0]) == 1 and hasattr(LogisticRegression, 'penalty'):
            self.model = LogisticRegression(C=1e9, penalty='l2')
        else:
            self.model = LogisticRegression(C=1e9)

    def fit(self, df: pd.DataFrame):
        X = df[['Mahalanobis_Distance']].values
        y = df['Condition'].values
        self.model.fit(X, y)
        
    def predict_proba(self, df: pd.DataFrame) -> np.ndarray:
        X = df[['Mahalanobis_Distance']].values
        return self.model.predict_proba(X)[:, 1]

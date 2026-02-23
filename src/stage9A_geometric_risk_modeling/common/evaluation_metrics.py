"""
stage9A_geometric_risk_modeling.common.evaluation_metrics

Defines mandatory evaluation metrics for Task 39:
ROC-AUC, Log-loss, Brier score, Calibration slope.
"""

import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score, log_loss, brier_score_loss
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LogisticRegression

def compute_metrics(y_true: np.ndarray, y_prob: np.ndarray) -> dict:
    """
    Computes the four mandatory metrics for a given set of predictions.
    y_prob must be probabilities of class 1.
    """
    if len(np.unique(y_true)) < 2:
        return {
            'roc_auc': np.nan,
            'log_loss': np.nan,
            'brier_score': np.nan,
            'calibration_slope': np.nan
        }
        
    auc = roc_auc_score(y_true, y_prob)
    
    # Clip probs to avoid log(0)
    y_prob_clipped = np.clip(y_prob, 1e-15, 1 - 1e-15)
    loss = log_loss(y_true, y_prob_clipped)
    
    brier = brier_score_loss(y_true, y_prob)
    
    # Calibration slope (logistic regression of log-odds mapped to true)
    # y = sigmoid(slope * logit(p) + intercept)
    logits = np.log(y_prob_clipped / (1 - y_prob_clipped))
    calib_model = LogisticRegression(penalty='none' if int(pd.__version__.split(".")[0]) == 1 and hasattr(LogisticRegression, 'penalty') else None)
    if not hasattr(LogisticRegression, 'penalty') or calib_model.penalty == 'none':
        calib_model = LogisticRegression(C=1e9) # fallback
        
    try:
        calib_model.fit(logits.reshape(-1, 1), y_true)
        slope = calib_model.coef_[0][0]
    except Exception:
        slope = np.nan
        
    return {
        'roc_auc': float(auc),
        'log_loss': float(loss),
        'brier_score': float(brier),
        'calibration_slope': float(slope)
    }

"""
stage9A_geometric_risk_modeling.common.bootstrap_validation

Implements bootstrap resampling for stability testing of Task 39 models.
"""

import numpy as np
import pandas as pd
from .evaluation_metrics import compute_metrics

def evaluate_bootstrap_stability(model_class, df: pd.DataFrame, n_iterations: int = 100, seed: int = 42) -> dict:
    """
    Evaluates a model's stability over n_iterations of bootstrap resampling.
    Returns mean and SD of AUC and Log-loss.
    """
    rng = np.random.default_rng(seed)
    n_samples = len(df)
    
    aucs = []
    losses = []
    
    for _ in range(n_iterations):
        # Sample with replacement
        indices = rng.choice(n_samples, size=n_samples, replace=True)
        df_boot = df.iloc[indices].copy()
        
        # We also need OOB (Out-of-bag) for valid evaluation to not overfit
        oob_indices = np.setdiff1d(np.arange(n_samples), indices)
        df_oob = df.iloc[oob_indices].copy()
        
        if len(df_oob['Condition'].unique()) < 2 or len(df_boot['Condition'].unique()) < 2:
            continue
            
        model = model_class()
        model.fit(df_boot)
        
        predictions = model.predict_proba(df_oob)
        metrics = compute_metrics(df_oob['Condition'].values, predictions)
        
        if not np.isnan(metrics['roc_auc']):
            aucs.append(metrics['roc_auc'])
            losses.append(metrics['log_loss'])
            
    if not aucs:
        return {'auc_mean': np.nan, 'auc_sd': np.nan, 'loss_mean': np.nan, 'loss_sd': np.nan}
        
    return {
        'auc_mean': float(np.mean(aucs)),
        'auc_sd': float(np.std(aucs)),
        'loss_mean': float(np.mean(losses)),
        'loss_sd': float(np.std(losses))
    }

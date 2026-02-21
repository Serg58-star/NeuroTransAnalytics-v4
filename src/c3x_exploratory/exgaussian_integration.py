"""
c3x_exploratory.exgaussian_integration

This module implements the Ex-Gaussian Parametric Integration exploratory procedure
(Task 35.2, Stage 6 extension).
"""

import numpy as np
import scipy.stats as stats
from typing import Dict, Any, Tuple
from sklearn.decomposition import PCA

class ExGaussianIntegrationAnalysis:
    """
    Implementation of the Task 35.2 Ex-Gaussian Integration exploratory procedure.
    Extracts strictly the Ex-Gaussian parameters and allows structural orthogonality checking via PCA.
    """
    
    def __init__(self):
        self.procedure_name = "Task 35.2 Ex-Gaussian Parametric Integration"
        self.goal = "To compute strictly structural relationships between generic parameters and existing axes."
        
        self.parameters = {
            "distribution": "exgaussian"
        }
        self.reproducibility_notes = "Deterministic Maximum Likelihood Estimation via SciPy; standard scikit-learn PCA."
        
    @property
    def non_interpretation_clause(self) -> str:
        """Mandatory architectural clause."""
        return (
            "This procedure is exploratory and descriptive. "
            "It produces structural representations only and does not imply interpretation, "
            "inference, or evaluation."
        )

    def extract_parameters(self, rt_series: np.ndarray) -> Dict[str, Any]:
        """
        Extracts mu, sigma, and tau from the Ex-Gaussian (exponnorm) fit.
        
        SciPy's exponnorm uses `K` as the primary shape parameter where K = tau/sigma.
        loc roughly = mu, scale = sigma.
        """
        if len(rt_series) < 5:
            return {"mu": np.nan, "sigma": np.nan, "tau": np.nan}
            
        try:
            # SciPy parameterization: K, loc, scale
            # tau = K * scale
            # sigma = scale
            # mu = loc
            K, loc, scale = stats.exponnorm.fit(rt_series)
            
            tau = K * scale
            mu = loc
            sigma = scale
            
            return {
                "mu": float(mu),
                "sigma": float(sigma),
                "tau": float(tau)
            }
        except Exception:
            return {"mu": np.nan, "sigma": np.nan, "tau": np.nan}

    def compute_pca_structure(self, feature_matrix: np.ndarray) -> Dict[str, Any]:
        """
        Computes a Principal Component Analysis on the expanded feature matrix to check if 
        new components (like tau) align to existing components or fall on new dimensions.
        
        feature_matrix: 2D numpy array [n_samples, n_features]
        Expects standardized (Z-scored) data for structural validity.
        """
        if feature_matrix.shape[0] < feature_matrix.shape[1] or feature_matrix.shape[0] < 2:
            return {"eigenvalues": [], "explained_variance_ratio": [], "participation_ratio": np.nan}
            
        # Standardize strictly for structural PCA
        means = np.mean(feature_matrix, axis=0)
        stds = np.std(feature_matrix, axis=0)
        stds[stds == 0] = 1.0
        
        Z = (feature_matrix - means) / stds
        
        pca = PCA()
        pca.fit(Z)
        
        evals = pca.explained_variance_
        ratios = pca.explained_variance_ratio_
        
        # Participation Ratio: PR = (sum(evals))^2 / sum(evals^2)
        pr = np.sum(evals)**2 / np.sum(evals**2)
        
        return {
            "eigenvalues": evals.tolist(),
            "explained_variance_ratio": ratios.tolist(),
            "participation_ratio": float(pr)
        }

    def execute(self, data: np.ndarray) -> Dict[str, Any]:
        """
        Executes the basic extraction sequence on a single RT block.
        PCA requires cross-sequence integration and is handled separately.
        """
        params = self.extract_parameters(data)
        
        return {
            "procedure_name": self.procedure_name,
            "non_interpretation_clause": self.non_interpretation_clause,
            "parameters": self.parameters,
            "exgaussian_parameters": params
        }

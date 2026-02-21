import pytest
import numpy as np

from src.c3x_exploratory.synthetic_parametric import generate_exgaussian_rt
from src.c3x_exploratory.exgaussian_integration import ExGaussianIntegrationAnalysis

class TestExGaussianIntegration:
    
    def test_structural_compliance(self):
        proc = ExGaussianIntegrationAnalysis()
        
        assert "This procedure is exploratory and descriptive." in proc.non_interpretation_clause
        assert proc.procedure_name == "Task 35.2 Ex-Gaussian Parametric Integration"
        
        data = generate_exgaussian_rt(n_samples=50, seed=42)
        res = proc.execute(data)
        
        assert "procedure_name" in res
        assert "non_interpretation_clause" in res
        assert "exgaussian_parameters" in res
        
        params = res["exgaussian_parameters"]
        assert "mu" in params
        assert "sigma" in params
        assert "tau" in params
        
    def test_parameter_extraction_accuracy(self):
        # We generate an ex-gaussian with known parameters and check if the extract approximates it
        # Note: MLE fitting on small N is noisy, but on N=2000 it should be quite close
        true_mu = 400.0
        true_sigma = 30.0
        true_tau = 100.0
        
        data = generate_exgaussian_rt(n_samples=2000, mu=true_mu, sigma=true_sigma, tau=true_tau, seed=42)
        
        proc = ExGaussianIntegrationAnalysis()
        res = proc.execute(data)
        params = res["exgaussian_parameters"]
        
        assert np.isclose(params["mu"], true_mu, rtol=0.05, atol=20)
        assert np.isclose(params["sigma"], true_sigma, rtol=0.1, atol=10)
        assert np.isclose(params["tau"], true_tau, rtol=0.1, atol=20)
        
    def test_pca_structural_computation(self):
        proc = ExGaussianIntegrationAnalysis()
        
        # Matrix: 100 samples, 5 features
        rng = np.random.default_rng(42)
        matrix = rng.normal(size=(100, 5))
        
        # Make feature 5 highly correlated with feature 1 (so it's not independent)
        matrix[:, 4] = matrix[:, 0] + rng.normal(scale=0.1, size=100)
        
        res = proc.compute_pca_structure(matrix)
        
        assert len(res["eigenvalues"]) == 5
        assert len(res["explained_variance_ratio"]) == 5
        assert res["participation_ratio"] > 0
        
        # Because feature 5 is redundant, the last eigenvalue should be very small
        assert res["eigenvalues"][-1] < 0.2

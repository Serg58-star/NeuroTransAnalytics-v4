import pytest
import numpy as np

from src.c3x_exploratory.synthetic_parametric import (
    generate_normal_rt,
    generate_lognormal_rt,
    generate_gamma_rt,
    generate_weibull_rt,
    generate_exgaussian_rt
)
from src.c3x_exploratory.parametric_modeling import ParametricModelingAnalysis

class TestParametricGeneratorsAndProcedure:
    
    def test_parametric_structure(self):
        proc = ParametricModelingAnalysis()
        
        assert "This procedure is exploratory and descriptive." in proc.non_interpretation_clause
        assert proc.procedure_name == "Task 35.1 Parametric Distribution Modeling"
        
        data = generate_lognormal_rt(n_samples=50, seed=42)
        res = proc.execute(data)
        
        assert "procedure_name" in res
        assert "non_interpretation_clause" in res
        assert "fits" in res
        
        assert "normal" in res["fits"]
        assert "lognormal" in res["fits"]
        assert "best_fit_aic" in res["fits"]
        
    def test_structural_accuracy_normal(self):
        # Normal data should ideally be matched best by normal or exgaussian (which reduces to normal)
        data = generate_normal_rt(n_samples=5000, loc=500, scale=30, seed=42)
        proc = ParametricModelingAnalysis()
        res = proc.execute(data)
        
        # In a very large pure normal sample, Normal AIC should be very close to the best 
        # (ExGaussian adds a parameter, so AIC might favor Normal or be virtually identical)
        fits = res["fits"]
        norm_aic = fits["normal"]["aic"]
        lognorm_aic = fits["lognormal"]["aic"]
        
        # Ensure it fits better than highly skewed lognorm
        assert norm_aic < lognorm_aic

    def test_structural_accuracy_lognormal(self):
        data = generate_lognormal_rt(n_samples=5000, s=0.5, scale=500, seed=42)
        proc = ParametricModelingAnalysis()
        res = proc.execute(data)
        
        fits = res["fits"]
        norm_aic = fits["normal"]["aic"]
        lognorm_aic = fits["lognormal"]["aic"]
        
        # Lognormal should destroy Normal on a highly skewed lognormal synthetic sample
        assert lognorm_aic < norm_aic
        
        # It should likely be the best_fit_aic
        assert res["fits"]["best_fit_aic"] == "lognormal"

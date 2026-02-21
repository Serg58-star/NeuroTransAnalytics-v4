import pytest
import numpy as np
from src.c3x_exploratory.synthetic_variability import (
    generate_skewed_rt,
    generate_heavy_tail_rt,
    generate_high_variance_rt
)
from src.c3x_exploratory.variability import VariabilityAnalysis

class TestSyntheticVariabilityGenerators:
    def test_skewed_generator(self):
        # positive alpha = right skewed
        data_right = generate_skewed_rt(n_samples=5000, mean=500, std=50, skew_alpha=10.0, seed=42)
        # negative alpha = left skewed
        data_left = generate_skewed_rt(n_samples=5000, mean=500, std=50, skew_alpha=-10.0, seed=42)
        
        proc = VariabilityAnalysis()
        metrics_right = proc.analyze_skew_kurtosis(data_right)
        metrics_left = proc.analyze_skew_kurtosis(data_left)
        
        assert metrics_right["skewness"] > 0
        assert metrics_left["skewness"] < 0
        
    def test_heavy_tail_generator(self):
        # student t with low df has higher kurtosis than normal
        data_heavy = generate_heavy_tail_rt(n_samples=5000, mean=500, std=50, df=3.0, seed=42)
        data_normal = generate_heavy_tail_rt(n_samples=5000, mean=500, std=50, df=100.0, seed=42) # near normal
        
        proc = VariabilityAnalysis()
        metrics_heavy = proc.analyze_skew_kurtosis(data_heavy)
        metrics_normal = proc.analyze_skew_kurtosis(data_normal)
        
        assert metrics_heavy["kurtosis"] > metrics_normal["kurtosis"]

    def test_high_variance_generator(self):
        target_mad = 80.0
        data = generate_high_variance_rt(n_samples=1000, mean=500, target_mad=target_mad, seed=42)
        
        proc = VariabilityAnalysis()
        metrics = proc.analyze_variance(data)
        
        assert np.isclose(metrics["mad"], target_mad, rtol=0.05)


class TestVariabilityAnalysisProcedure:
    def test_procedure_structure_compliance(self):
        # Must contain non-interpretation clause and follow structure
        proc = VariabilityAnalysis()
        assert "This procedure is exploratory and descriptive." in proc.non_interpretation_clause
        assert proc.procedure_name == "Stage 6 Variability and Tail Geometry"
        
        data = generate_skewed_rt(n_samples=36, seed=42)
        result = proc.execute(data)
        
        assert "procedure_name" in result
        assert "non_interpretation_clause" in result
        assert "skew_kurtosis" in result
        assert "tail_geometry" in result
        assert "variance" in result
        
        # Check specific keys
        assert "skewness" in result["skew_kurtosis"]
        assert "tail_to_mad_ratio" in result["tail_geometry"]
        assert "cv_robust" in result["variance"]

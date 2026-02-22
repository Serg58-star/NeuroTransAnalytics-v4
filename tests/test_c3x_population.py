"""
tests/test_c3x_population.py

Validates the PopulationGeometryAnalysis exploratory procedure using
synthetic datasets (continuum vs discrete)
"""
import pytest
from src.c3x_exploratory.synthetic_population import generate_continuum_population, generate_discrete_population
from src.c3x_exploratory.population_geometry import PopulationGeometryAnalysis

def test_continuum_population():
    X_cont = generate_continuum_population(n_samples=2000, seed=42)
    analysis = PopulationGeometryAnalysis()
    results = analysis.execute(X_cont)
    
    assert results["non_interpretation_clause"] == analysis.non_interpretation_clause
    assert results["conclusion"] == "CONTINUUM"
    assert results["density"]["hopkins"] < 0.85
    
def test_discrete_population():
    X_disc = generate_discrete_population(n_samples=600, seed=42)
    analysis = PopulationGeometryAnalysis()
    results = analysis.execute(X_disc)
    
    assert results["conclusion"] == "STABLE DISCRETE TYPES"
    assert results["density"]["hopkins"] > 0.65

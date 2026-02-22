"""
scripts/run_stage7_population_synthetic.py

Executes the Stage 7 Population Geometry Audit using synthetic
Continuous and Discrete trait-core datasets.
Outputs results cleanly, and saves plots.
"""

import os
import json
import numpy as np
import matplotlib.pyplot as plt

plt.style.use('ggplot')

from src.c3x_exploratory.synthetic_population import generate_continuum_population, generate_discrete_population
from src.c3x_exploratory.population_geometry import PopulationGeometryAnalysis

def plot_3d_scatter(X: np.ndarray, title: str, filename: str):
    """Saves a 3D scatter plot of the population."""
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(X[:, 0], X[:, 1], X[:, 2], alpha=0.6, s=20, c='royalblue')
    
    ax.set_title(title)
    ax.set_xlabel("Speed Axis")
    ax.set_ylabel("Lateral Axis")
    ax.set_zlabel("Residual Tone")
    
    plt.tight_layout()
    plt.savefig(filename, dpi=150)
    plt.close()

def plot_gap_statistic(k_range, gaps, title, filename):
    plt.figure(figsize=(8, 5))
    plt.plot(k_range, gaps, marker='o', linestyle='-', color='indigo')
    plt.title(title)
    plt.xlabel("Number of Clusters (k)")
    plt.ylabel("Gap Statistic")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(filename, dpi=150)
    plt.close()

def main():
    out_dir = "results/stage7_population_geometry"
    os.makedirs(out_dir, exist_ok=True)
    
    print("=" * 60)
    print("STAGE 7: POPULATION GEOMETRY AUDIT (SYNTHETIC VERIFICATION)")
    print("=" * 60)
    
    analysis = PopulationGeometryAnalysis()
    print(f"\n[Architectural Compliance]\n{analysis.non_interpretation_clause}\n")
    
    # 1. Evaluate Continuum
    print("-" * 60)
    print("Scenario A: Continuous Population (No distinct subtypes)")
    X_cont = generate_continuum_population(n_samples=1000, seed=101)
    
    # Plotting
    plot_3d_scatter(X_cont, "Synthetic Continuum Population", os.path.join(out_dir, "synthetic_continuum_3d.png"))
    
    res_cont = analysis.execute(X_cont)
    
    print(f"Hopkins Statistic: {res_cont['density']['hopkins']:.3f} (expect < 0.60)")
    best_sil_cont = max(res_cont['clustering']['metrics']['kmeans']['silhouette'])
    print(f"Best KMeans Silhouette: {best_sil_cont:.3f}")
    print(f"Gap Optimal k: {res_cont['gap']['optimal_k']}")
    
    print(f"\n>>> FINAL CONCLUSION: {res_cont['conclusion']}")
    
    plot_gap_statistic(
        list(range(1, 9)), 
        res_cont['gap']['scores'], 
        "Gap Statistic: Continuum", 
        os.path.join(out_dir, "gap_continuum.png")
    )
    
    with open(os.path.join(out_dir, "results_continuum.json"), "w") as f:
        json.dump(res_cont, f, indent=2)
        
        
    # 2. Evaluate Discrete Types
    print("\n" + "-" * 60)
    print("Scenario B: Discrete Subtypes (Stable Trait Clusters)")
    X_disc = generate_discrete_population(n_samples=1000, seed=102)
    
    # Plotting
    plot_3d_scatter(X_disc, "Synthetic Discrete Types Population", os.path.join(out_dir, "synthetic_discrete_3d.png"))
    
    res_disc = analysis.execute(X_disc)
    
    print(f"Hopkins Statistic: {res_disc['density']['hopkins']:.3f} (expect > 0.65)")
    best_sil_disc = max(res_disc['clustering']['metrics']['kmeans']['silhouette'])
    print(f"Best KMeans Silhouette: {best_sil_disc:.3f}")
    print(f"Gap Optimal k: {res_disc['gap']['optimal_k']}")
    
    print(f"\n>>> FINAL CONCLUSION: {res_disc['conclusion']}")
    
    plot_gap_statistic(
        list(range(1, 9)), 
        res_disc['gap']['scores'], 
        "Gap Statistic: Discrete Types", 
        os.path.join(out_dir, "gap_discrete.png")
    )
    
    with open(os.path.join(out_dir, "results_discrete.json"), "w") as f:
        json.dump(res_disc, f, indent=2)

    print("\n" + "=" * 60)
    print(f"Validation complete. Artifacts saved to '{out_dir}/'")

if __name__ == "__main__":
    main()

"""
Example script for running Exploratory Lab pipeline.

This demonstrates the basic workflow for Этап 1 (MVP).
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from exploratory_lab.pipelines.exp_pipeline_v0 import ExploratoryPipeline


def main():
    """Run exploratory analysis pipeline."""
    
    # Initialize pipeline
    pipeline = ExploratoryPipeline(db_path="data/neurotrans.db")
    
    # Run with minimum 3 sessions per subject
    results = pipeline.run(min_sessions=3)
    
    # Access results
    print("\n=== Results Summary ===")
    print(f"Features shape: {results['features'].shape}")
    print(f"\nPCA Analysis:")
    print(f"  - Effective dimensionality: {results['pca']['n_components_kaiser']} components")
    print(f"\nCluster Analysis:")
    print(f"  - Hopkins statistic: {results['hopkins']:.3f}")
    print(f"  - Best silhouette score: {max(results['silhouette'].values()):.3f}")
    
    # Interpretation
    print("\n=== Interpretation ===")
    if results['hopkins'] < 0.5:
        print("→ GRADIENT structure detected (continuous variation)")
    elif results['hopkins'] > 0.7:
        print("→ CLUSTER structure detected (discrete groups)")
    else:
        print("→ MIXED or WEAK structure")
    
    if max(results['silhouette'].values()) > 0.35:
        print("→ Clusters are REAL and well-separated")
    elif max(results['silhouette'].values()) > 0.25:
        print("→ Weak clustering (proceed with caution)")
    else:
        print("→ NO meaningful clusters found")


if __name__ == "__main__":
    main()

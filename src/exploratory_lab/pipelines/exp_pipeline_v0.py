"""
Exploratory Pipeline v0 - MVP Implementation

End-to-end pipeline for baseline exploratory analysis:
1. Load trial-level data
2. Extract 6 baseline features
3. Analyze dimensionality (PCA)
4. Test cluster tendency (Hopkins)
5. Fit UMAP for visualization

This pipeline implements Этап 1 (MVP) from the approved design.
"""

import pandas as pd
from pathlib import Path
from typing import Optional, Dict, Any
import json

from ..data_loader import TrialLevelDataLoader
from ..feature_engineering.baseline_features import BaselineFeatureExtractor
from ..feature_engineering.correlation_validator import CorrelationValidator
from ..geometry.dimensionality import DimensionalityAnalyzer
from ..geometry.clustering import ClusterAnalyzer


class ExploratoryPipeline:
    """
    End-to-end pipeline for exploratory analysis.
    
    Usage:
    ------
    pipeline = ExploratoryPipeline()
    results = pipeline.run(min_sessions=3)
    """
    
    def __init__(self, db_path: str = "data/neurotrans.db"):
        """
        Initialize the pipeline.
        
        Parameters
        ----------
        db_path : str
            Path to SQLite database
        """
        self.db_path = db_path
        self.data_loader = TrialLevelDataLoader(db_path)
        self.feature_extractor = BaselineFeatureExtractor()
        self.correlation_validator = CorrelationValidator()
        self.dim_analyzer = DimensionalityAnalyzer()
        self.cluster_analyzer = ClusterAnalyzer()
        
        self.features_df = None
        self.correlation_results = None
        self.pca_results = None
        self.umap_embedding = None
        self.hopkins_score = None
        self.silhouette_scores = None
    
    def run(
        self,
        subject_ids: Optional[list] = None,
        min_sessions: int = 3,
        output_dir: str = "data/exploratory"
    ) -> Dict[str, Any]:
        """
        Run complete exploratory analysis pipeline.
        
        Parameters
        ----------
        subject_ids : list, optional
            Specific subjects to analyze. If None, analyze all.
        min_sessions : int, default=3
            Minimum number of sessions required
        output_dir : str
            Directory for saving results
        
        Returns
        -------
        dict
            Complete analysis results
        """
        print("=== Exploratory Lab Pipeline v0.1 ===\n")
        
        # Step 1: Load trial data
        print(f"[1/6] Loading trial-level data (min_sessions={min_sessions})...")
        trials_df = self.data_loader.load_trials(
            subject_ids=subject_ids,
            min_sessions=min_sessions
        )
        print(f"  → Loaded {len(trials_df)} trials from {trials_df['subject_id'].nunique()} subjects")
        
        # Step 2: Extract features
        print("\n[2/7] Extracting corrected baseline features (11 features)...")
        self.features_df = self.feature_extractor.extract_population_features(trials_df)
        print(f"  → Extracted features for {len(self.features_df)} subjects")
        print(f"  → Features: {list(self.features_df.columns)}")
        
        # Step 2.5: Validate correlation structure (Task 27.1)
        print("\n[3/7] Validating correlation structure...")
        self.correlation_results = self.correlation_validator.analyze(
            self.features_df, threshold=0.8
        )
        print(self.correlation_results['summary'])
        
        # Step 3: PCA analysis
        print("\n[4/7] Analyzing dimensionality (PCA)...")
        self.pca_results = self.dim_analyzer.fit_pca(self.features_df)
        print(f"  → Eigenvalues: {self.pca_results['eigenvalues'][:3]}")
        print(f"  → Components with eigenvalue > 1: {self.pca_results['n_components_kaiser']}")
        print(f"  → Cumulative variance (2 PCs): {self.pca_results['cumulative_variance'][1]:.2%}")
        
        # Step 4: Hopkins Statistic
        print("\n[5/7] Testing cluster tendency (Hopkins Statistic)...")
        self.hopkins_score = self.cluster_analyzer.hopkins_statistic(self.features_df)
        print(f"  → Hopkins statistic: {self.hopkins_score:.3f}")
        if self.hopkins_score < 0.5:
            print("  → Interpretation: GRADIENT structure (uniform distribution)")
        elif self.hopkins_score > 0.7:
            print("  → Interpretation: CLUSTER structure")
        else:
            print("  → Interpretation: WEAK clustering tendency")
        
        # Step 5: Silhouette analysis
        print("\n[6/7] Evaluating k-means quality (Silhouette Analysis)...")
        self.silhouette_scores = self.cluster_analyzer.silhouette_analysis(self.features_df)
        best_k = max(self.silhouette_scores, key=self.silhouette_scores.get)
        print(f"  → Best k={best_k} (Silhouette={self.silhouette_scores[best_k]:.3f})")
        if self.silhouette_scores[best_k] > 0.35:
            print("  → Interpretation: REAL cluster structure detected")
        elif self.silhouette_scores[best_k] > 0.25:
            print("  → Interpretation: WEAK cluster structure")
        else:
            print("  → Interpretation: NO meaningful clusters")
        
        # Step 6: UMAP embedding
        print("\n[7/7] Computing UMAP embedding...")
        try:
            self.umap_embedding = self.dim_analyzer.fit_umap(self.features_df)
            print("  → UMAP embedding complete")
        except ImportError:
            print("  → UMAP not available (install with: pip install umap-learn)")
            self.umap_embedding = None
        
        # Save results
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        self._save_results(output_path)
        
        print(f"\n=== Pipeline Complete ===")
        print(f"Results saved to: {output_path}")
        
        return self._compile_results()
    
    def _save_results(self, output_path: Path):
        """Save all results to files."""
        # Features
        features_path = output_path / "features" / "baseline_features_v0.parquet"
        features_path.parent.mkdir(parents=True, exist_ok=True)
        self.features_df.to_parquet(features_path)
        
        # PCA results
        pca_path = output_path / "embeddings" / "pca_results_v0.json"
        pca_path.parent.mkdir(parents=True, exist_ok=True)
        pca_export = {
            'eigenvalues': self.pca_results['eigenvalues'].tolist(),
            'explained_variance': self.pca_results['explained_variance'].tolist(),
            'cumulative_variance': self.pca_results['cumulative_variance'].tolist(),
            'n_components_kaiser': self.pca_results['n_components_kaiser']
        }
        with open(pca_path, 'w') as f:
            json.dump(pca_export, f, indent=2)
        
        # UMAP embedding
        if self.umap_embedding is not None:
            umap_path = output_path / "embeddings" / "umap_embedding_v0.parquet"
            self.umap_embedding.to_parquet(umap_path)
        
        # Correlation matrices (Task 27.1)
        if self.correlation_results is not None:
            corr_path = output_path / "correlations"
            self.correlation_validator.export_results(str(corr_path))
        
        # Summary report
        report_path = output_path / "reports" / "analysis_summary_v0.txt"
        report_path.parent.mkdir(parents=True, exist_ok=True)
        with open(report_path, 'w') as f:
            f.write("=== Exploratory Lab Analysis Summary ===\n\n")
            f.write(f"Sample size: {len(self.features_df)} subjects\n")
            f.write(f"Features: 11 corrected baseline features (Task 27.1)\n\n")
            f.write(f"Correlation Structure:\n")
            if self.correlation_results:
                high_corr = self.correlation_results['high_corr_pairs']
                f.write(f"  - High correlations (|r| > 0.8): {len(high_corr)}\n")
                if self.correlation_results['dominant_axis']['dominates']:
                    pc1_var = self.correlation_results['dominant_axis']['pc1_variance_explained']
                    f.write(f"  - Dominant general factor: Yes (PC1 = {pc1_var:.1%})\n")
                else:
                    f.write(f"  - Dominant general factor: No\n")
            f.write(f"\nPCA Dimensionality:\n")
            f.write(f"  - Components (eigenvalue > 1): {self.pca_results['n_components_kaiser']}\n")
            f.write(f"  - Cumulative variance (2 PCs): {self.pca_results['cumulative_variance'][1]:.2%}\n\n")
            f.write(f"Cluster Tendency:\n")
            f.write(f"  - Hopkins statistic: {self.hopkins_score:.3f}\n")
            f.write(f"  - Best Silhouette (k={max(self.silhouette_scores, key=self.silhouette_scores.get)}): {max(self.silhouette_scores.values()):.3f}\n")
    
    def _compile_results(self) -> Dict[str, Any]:
        """Compile all results into a dictionary."""
        return {
            'features': self.features_df,
            'correlations': self.correlation_results,
            'pca': self.pca_results,
            'hopkins': self.hopkins_score,
            'silhouette': self.silhouette_scores,
            'umap': self.umap_embedding
        }

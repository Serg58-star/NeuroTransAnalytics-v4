"""
Correlation Structure Validator for Exploratory Lab

Performs pre-clustering validation of feature correlation structure.
Required by Task 27.1 before proceeding to PCA/clustering.

Functionality:
1. Pearson and Spearman correlation matrices
2. Multicollinearity detection (VIF)
3. Dominant axis identification
4. Redundant coordinate flagging
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Any
from scipy import stats


class CorrelationValidator:
    """
    Validates correlation structure of feature space.
    
    Detects multicollinearity, redundant coordinates, and dominant axes
    before dimensional reduction.
    """
    
    def __init__(self):
        """Initialize the correlation validator."""
        self.pearson_matrix = None
        self.spearman_matrix = None
        self.vif_scores = None
        self.high_correlations = None
    
    def analyze(self, features_df: pd.DataFrame, 
                threshold: float = 0.8) -> Dict[str, Any]:
        """
        Perform complete correlation structure analysis.
        
        Parameters
        ----------
        features_df : pd.DataFrame
            Feature matrix (subjects × features)
        threshold : float, default=0.8
            Threshold for flagging high correlations
        
        Returns
        -------
        dict
            Analysis results with keys:
            - pearson: Pearson correlation matrix
            - spearman: Spearman correlation matrix
            - vif: VIF scores for each feature
            - high_corr_pairs: List of highly correlated pairs
            - dominant_axis: Whether a dominant speed axis exists
            - summary: Text summary of findings
        """
        # Store for later access
        self.pearson_matrix = features_df.corr(method='pearson')
        self.spearman_matrix = features_df.corr(method='spearman')
        
        # Compute VIF
        self.vif_scores = self._compute_vif(features_df)
        
        # Find high correlations
        self.high_correlations = self._find_high_correlations(
            self.pearson_matrix, threshold
        )
        
        # Check for dominant axis
        dominant_axis = self._check_dominant_axis(features_df)
        
        # Generate summary
        summary = self._generate_summary(threshold)
        
        return {
            'pearson': self.pearson_matrix,
            'spearman': self.spearman_matrix,
            'vif': self.vif_scores,
            'high_corr_pairs': self.high_correlations,
            'dominant_axis': dominant_axis,
            'summary': summary
        }
    
    def _compute_vif(self, features_df: pd.DataFrame) -> pd.Series:
        """
        Compute Variance Inflation Factor for each feature.
        
        VIF = 1 / (1 - R²) where R² is from regressing feature on all others.
        VIF > 10 indicates severe multicollinearity.
        VIF > 5 indicates moderate multicollinearity.
        """
        from sklearn.linear_model import LinearRegression
        
        vif_data = {}
        feature_cols = features_df.columns.tolist()
        
        for i, feature in enumerate(feature_cols):
            # Regress this feature on all others
            X = features_df.drop(columns=[feature]).values
            y = features_df[feature].values
            
            try:
                # Fit linear regression
                lr = LinearRegression()
                lr.fit(X, y)
                
                # Calculate R²
                y_pred = lr.predict(X)
                ss_res = np.sum((y - y_pred) ** 2)
                ss_tot = np.sum((y - np.mean(y)) ** 2)
                
                if ss_tot == 0:
                    vif_data[feature] = np.inf
                else:
                    r_squared = 1 - (ss_res / ss_tot)
                    
                    # VIF = 1 / (1 - R²)
                    if r_squared >= 0.9999:  # Near-perfect collinearity
                        vif_data[feature] = np.inf
                    else:
                        vif_data[feature] = 1 / (1 - r_squared)
            except:
                vif_data[feature] = np.nan
        
        return pd.Series(vif_data)
    
    def _find_high_correlations(self, corr_matrix: pd.DataFrame, 
                                threshold: float) -> List[Tuple[str, str, float]]:
        """
        Find pairs of features with |r| > threshold.
        
        Returns list of (feature1, feature2, correlation) tuples.
        """
        high_corr = []
        
        # Iterate through upper triangle only (avoid duplicates)
        for i in range(len(corr_matrix.columns)):
            for j in range(i + 1, len(corr_matrix.columns)):
                corr_val = corr_matrix.iloc[i, j]
                
                if abs(corr_val) > threshold:
                    high_corr.append((
                        corr_matrix.columns[i],
                        corr_matrix.columns[j],
                        corr_val
                    ))
        
        # Sort by absolute correlation (descending)
        high_corr.sort(key=lambda x: abs(x[2]), reverse=True)
        
        return high_corr
    
    def _check_dominant_axis(self, features_df: pd.DataFrame) -> Dict[str, Any]:
        """
        Check if there is a dominant "general speed" axis.
        
        Uses PCA to check if PC1 explains > 50% variance and
        has consistent loadings (all same sign).
        """
        from sklearn.decomposition import PCA
        from sklearn.preprocessing import StandardScaler
        
        # Standardize features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(features_df)
        
        # Fit PCA
        pca = PCA()
        pca.fit(X_scaled)
        
        pc1_variance = pca.explained_variance_ratio_[0]
        pc1_loadings = pca.components_[0]
        
        # Check if all loadings have same sign (general factor)
        all_positive = np.all(pc1_loadings > 0)
        all_negative = np.all(pc1_loadings < 0)
        is_general_factor = all_positive or all_negative
        
        # Check if PC1 dominates (Task 27.2: updated thresholds)
        # 65% = expressed dimensionality, 80% = almost complete
        dominates_expressed = pc1_variance > 0.65
        dominates_complete = pc1_variance > 0.80
        
        return {
            'pc1_variance_explained': pc1_variance,
            'is_general_factor': is_general_factor,
            'dominates_expressed': dominates_expressed and is_general_factor,
            'dominates_complete': dominates_complete and is_general_factor,
            'pc1_loadings': pd.Series(pc1_loadings, index=features_df.columns)
        }
    
    def _generate_summary(self, threshold: float) -> str:
        """Generate text summary of correlation findings."""
        lines = []
        lines.append("=== Correlation Structure Validation ===\n")
        
        # High correlations
        if len(self.high_correlations) > 0:
            lines.append(f"HIGH CORRELATIONS (|r| > {threshold}):")
            for feat1, feat2, r in self.high_correlations[:5]:  # Top 5
                lines.append(f"  - {feat1} ↔ {feat2}: r = {r:.3f}")
            if len(self.high_correlations) > 5:
                lines.append(f"  ... and {len(self.high_correlations) - 5} more")
        else:
            lines.append(f"✓ No high correlations above |r| = {threshold}")
        
        lines.append("")
        
        # VIF warnings
        severe_vif = self.vif_scores[self.vif_scores > 10]
        moderate_vif = self.vif_scores[(self.vif_scores > 5) & (self.vif_scores <= 10)]
        
        if len(severe_vif) > 0:
            lines.append("⚠ SEVERE MULTICOLLINEARITY (VIF > 10):")
            for feat, vif in severe_vif.items():
                lines.append(f"  - {feat}: VIF = {vif:.2f}")
        
        if len(moderate_vif) > 0:
            lines.append("⚠ MODERATE MULTICOLLINEARITY (VIF > 5):")
            for feat, vif in moderate_vif.items():
                lines.append(f"  - {feat}: VIF = {vif:.2f}")
        
        if len(severe_vif) == 0 and len(moderate_vif) == 0:
            lines.append("✓ VIF scores within acceptable range (< 5)")
        
        return "\n".join(lines)
    
    def export_results(self, output_dir: str):
        """
        Export correlation matrices and VIF to CSV files.
        
        Parameters
        ----------
        output_dir : str
            Directory to save results
        """
        from pathlib import Path
        
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Save correlation matrices
        self.pearson_matrix.to_csv(output_path / "correlation_pearson.csv")
        self.spearman_matrix.to_csv(output_path / "correlation_spearman.csv")
        
        # Save VIF scores
        self.vif_scores.to_csv(output_path / "vif_scores.csv", header=['VIF'])
        
        # Save high correlation pairs
        if len(self.high_correlations) > 0:
            high_corr_df = pd.DataFrame(
                self.high_correlations,
                columns=['Feature_1', 'Feature_2', 'Correlation']
            )
            high_corr_df.to_csv(output_path / "high_correlations.csv", index=False)

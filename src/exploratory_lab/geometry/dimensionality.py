"""
Dimensionality Analyzer for Exploratory Lab

Implements PCA, Kernel PCA, and UMAP for latent structure analysis.
"""

import numpy as np
import pandas as pd
from typing import Tuple, Dict, Any
from sklearn.decomposition import PCA, KernelPCA
from sklearn.preprocessing import StandardScaler


try:
    import umap
    UMAP_AVAILABLE = True
except ImportError:
    UMAP_AVAILABLE = False


class DimensionalityAnalyzer:
    """
    Analyzes latent dimensionality of feature space.
    
    Methods:
    - PCA for linear dimensionality
    - Kernel PCA for nonlinear structures
    - UMAP for visualization
    """
    
    def __init__(self):
        """Initialize the analyzer."""
        self.scaler = StandardScaler()
        self.pca_model = None
        self.umap_model = None
        self.scaled_features = None
    
    def fit_pca(self, features_df: pd.DataFrame, n_components: int = None) -> Dict[str, Any]:
        """
        Fit PCA and analyze linear dimensionality.
        
        Parameters
        ----------
        features_df : pd.DataFrame
            Feature matrix (subjects x features)
        n_components : int, optional
            Number of components. If None, use all features.
        
        Returns
        -------
        dict
            PCA analysis results:
            - eigenvalues: array of eigenvalues
            - explained_variance: array of explained variance ratios
            - cumulative_variance: cumulative explained variance
            - n_components_kaiser: number of components with eigenvalue > 1
            - loadings: component loadings matrix
        """
        # Standardize features
        self.scaled_features = self.scaler.fit_transform(features_df)
        
        # Fit PCA
        if n_components is None:
            n_components = min(features_df.shape)
        
        self.pca_model = PCA(n_components=n_components)
        self.pca_model.fit(self.scaled_features)
        
        # Compute eigenvalues
        eigenvalues = self.pca_model.explained_variance_
        
        # Kaiser criterion: eigenvalues > 1
        n_components_kaiser = np.sum(eigenvalues > 1.0)
        
        # Cumulative variance
        cumulative_variance = np.cumsum(self.pca_model.explained_variance_ratio_)
        
        # Component loadings
        loadings = pd.DataFrame(
            self.pca_model.components_.T,
            columns=[f'PC{i+1}' for i in range(n_components)],
            index=features_df.columns
        )
        
        return {
            'eigenvalues': eigenvalues,
            'explained_variance': self.pca_model.explained_variance_ratio_,
            'cumulative_variance': cumulative_variance,
            'n_components_kaiser': int(n_components_kaiser),
            'loadings': loadings,
            'feature_names': list(features_df.columns)
        }
    
    def transform_pca(self, features_df: pd.DataFrame = None, n_components: int = 2) -> pd.DataFrame:
        """
        Transform features to PCA space.
        
        Parameters
        ----------
        features_df : pd.DataFrame, optional
            Features to transform. If None, use features from fit_pca.
        n_components : int, default=2
            Number of components to return.
        
        Returns
        -------
        pd.DataFrame
            Transformed features with columns PC1, PC2, ...
        """
        if self.pca_model is None:
            raise ValueError("Must call fit_pca() first")
        
        if features_df is not None:
            features_scaled = self.scaler.transform(features_df)
        else:
            features_scaled = self.scaled_features
        
        transformed = self.pca_model.transform(features_scaled)[:, :n_components]
        
        return pd.DataFrame(
            transformed,
            columns=[f'PC{i+1}' for i in range(n_components)],
            index=features_df.index if features_df is not None else None
        )
    
    def fit_umap(
        self,
        features_df: pd.DataFrame,
        n_neighbors: int = 15,
        min_dist: float = 0.1,
        n_components: int = 2,
        random_state: int = 42
    ) -> pd.DataFrame:
        """
        Fit UMAP for nonlinear dimensionality reduction and visualization.
        
        Parameters
        ----------
        features_df : pd.DataFrame
            Feature matrix
        n_neighbors : int, default=15
            Local neighborhood size for UMAP
        min_dist : float, default=0.1
            Minimum distance between points in embedding
        n_components : int, default=2
            Dimensionality of embedding (2 or 3 for visualization)
        random_state : int, default=42
            Random seed for reproducibility
        
        Returns
        -------
        pd.DataFrame
            UMAP embedding with columns UMAP1, UMAP2, ...
        """
        if not UMAP_AVAILABLE:
            raise ImportError("UMAP not installed. Run: pip install umap-learn")
        
        # Standardize features
        if self.scaled_features is None:
            self.scaled_features = self.scaler.fit_transform(features_df)
        
        # Fit UMAP
        self.umap_model = umap.UMAP(
            n_neighbors=n_neighbors,
            min_dist=min_dist,
            n_components=n_components,
            random_state=random_state
        )
        
        embedding = self.umap_model.fit_transform(self.scaled_features)
        
        return pd.DataFrame(
            embedding,
            columns=[f'UMAP{i+1}' for i in range(n_components)],
            index=features_df.index
        )

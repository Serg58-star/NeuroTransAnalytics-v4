"""
Cluster Analyzer for Exploratory Lab

Implements Hopkins Statistic, Silhouette Analysis, and DBSCAN.
"""

import numpy as np
import pandas as pd
from typing import Dict, Any, Tuple
from sklearn.neighbors import NearestNeighbors
from sklearn.cluster import KMeans, DBSCAN
from sklearn.metrics import silhouette_score, silhouette_samples
from sklearn.preprocessing import StandardScaler


class ClusterAnalyzer:
    """
    Analyzes cluster structure in feature space.
    
    Methods:
    - Hopkins Statistic: test for cluster tendency
    - Silhouette Analysis: evaluate k-means quality
    - DBSCAN: density-based clustering
    """
    
    def __init__(self):
        """Initialize the analyzer."""
        self.scaler = StandardScaler()
        self.scaled_features = None
    
    def hopkins_statistic(self, features_df: pd.DataFrame, n_samples: int = None) -> float:
        """
        Compute Hopkins Statistic to test for cluster tendency.
        
        Parameters
        ----------
        features_df : pd.DataFrame
            Feature matrix
        n_samples : int, optional
            Number of random samples. If None, use 10% of data.
        
        Returns
        -------
        float
            Hopkins statistic H ∈ [0, 1]
            - H < 0.5: uniform distribution (gradient structure)
            - H > 0.7: clustered distribution
        """
        # Standardize features
        X = self.scaler.fit_transform(features_df)
        n, d = X.shape
        
        if n_samples is None:
            n_samples = max(int(n * 0.1), 10)
        
        n_samples = min(n_samples, n - 1)
        
        # Sample random points from data
        indices = np.random.choice(n, size=n_samples, replace=False)
        X_sample = X[indices]
        
        # Generate random uniform points in same space
        X_random = np.random.uniform(X.min(axis=0), X.max(axis=0), size=(n_samples, d))
        
        # Compute distances
        nbrs = NearestNeighbors(n_neighbors=2).fit(X)
        
        # u_i: distance from random point to nearest real point
        u_distances, _ = nbrs.kneighbors(X_random, n_neighbors=1)
        u_i = u_distances[:, 0]
        
        # w_i: distance from real point to nearest neighbor (excluding self)
        w_distances, _ = nbrs.kneighbors(X_sample, n_neighbors=2)
        w_i = w_distances[:, 1]  # Second nearest is the actual nearest neighbor
        
        # Hopkins statistic
        H = np.sum(u_i) / (np.sum(u_i) + np.sum(w_i))
        
        return float(H)
    
    def silhouette_analysis(
        self,
        features_df: pd.DataFrame,
        k_range: Tuple[int, int] = (2, 10),
        random_state: int = 42
    ) -> Dict[int, float]:
        """
        Perform silhouette analysis for k-means clustering.
        
        Parameters
        ----------
        features_df : pd.DataFrame
            Feature matrix
        k_range : tuple, default=(2, 10)
            Range of k values to test (inclusive)
        random_state : int, default=42
            Random seed
        
        Returns
        -------
        dict
            Silhouette scores for each k
            Keys: k values
            Values: average silhouette score
        """
        # Standardize features
        if self.scaled_features is None:
            self.scaled_features = self.scaler.fit_transform(features_df)
        
        silhouette_scores = {}
        
        for k in range(k_range[0], k_range[1] + 1):
            if k >= len(features_df):
                break
            
            kmeans = KMeans(n_clusters=k, random_state=random_state, n_init=10)
            labels = kmeans.fit_predict(self.scaled_features)
            
            score = silhouette_score(self.scaled_features, labels)
            silhouette_scores[k] = float(score)
        
        return silhouette_scores
    
    def fit_kmeans(
        self,
        features_df: pd.DataFrame,
        n_clusters: int,
        random_state: int = 42
    ) -> Tuple[np.ndarray, float]:
        """
        Fit k-means clustering.
        
        Parameters
        ----------
        features_df : pd.DataFrame
            Feature matrix
        n_clusters : int
            Number of clusters
        random_state : int, default=42
            Random seed
        
        Returns
        -------
        tuple
            - labels: cluster labels for each subject
            - silhouette_score: quality metric
        """
        # Standardize features
        if self.scaled_features is None:
            self.scaled_features = self.scaler.fit_transform(features_df)
        
        kmeans = KMeans(n_clusters=n_clusters, random_state=random_state, n_init=10)
        labels = kmeans.fit_predict(self.scaled_features)
        
        score = silhouette_score(self.scaled_features, labels)
        
        return labels, float(score)
    
    def fit_dbscan(
        self,
        features_df: pd.DataFrame,
        eps: float = 0.5,
        min_samples: int = 5
    ) -> Tuple[np.ndarray, Dict[str, Any]]:
        """
        Fit DBSCAN (density-based clustering).
        
        Parameters
        ----------
        features_df : pd.DataFrame
            Feature matrix
        eps : float, default=0.5
            Maximum distance between samples in a neighborhood
        min_samples : int, default=5
            Minimum samples in a neighborhood for a core point
        
        Returns
        -------
        tuple
            - labels: cluster labels (-1 for noise)
            - stats: clustering statistics
        """
        # Standardize features
        if self.scaled_features is None:
            self.scaled_features = self.scaler.fit_transform(features_df)
        
        dbscan = DBSCAN(eps=eps, min_samples=min_samples)
        labels = dbscan.fit_predict(self.scaled_features)
        
        # Compute statistics
        n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
        n_noise = list(labels).count(-1)
        noise_ratio = n_noise / len(labels) if len(labels) > 0 else 0
        
        stats = {
            'n_clusters': n_clusters,
            'n_noise': n_noise,
            'noise_ratio': noise_ratio
        }
        
        return labels, stats

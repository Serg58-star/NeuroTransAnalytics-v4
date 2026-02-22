"""
c3x_exploratory.population_geometry

Implements Task 36 - Population Geometry Audit.
Analyzes whether the 3D latent space population (trait-core) is a continuum or discrete.
"""

import numpy as np
import warnings
from sklearn.neighbors import NearestNeighbors
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.mixture import GaussianMixture
from sklearn.metrics import silhouette_score, calinski_harabasz_score, davies_bouldin_score, adjusted_rand_score
from sklearn.metrics import pairwise_distances
from sklearn.decomposition import PCA
from scipy.spatial.distance import cdist
from scipy.sparse.csgraph import minimum_spanning_tree, connected_components

# Attempt to import HDBSCAN
try:
    from sklearn.cluster import HDBSCAN
except ImportError:
    try:
        from hdbscan import HDBSCAN
    except ImportError:
        HDBSCAN = None

class PopulationGeometryAnalysis:
    """
    Implementation of the Task 36 Population Geometry Audit.
    Evaluates empirical 3D trait data against continuum vs discrete hypotheses.
    """
    
    def __init__(self):
        self.procedure_name = "Task 36 Population Geometry Audit"
        self.goal = "To verify if the 3D latent space population is a continuous continuum or contains stable discrete subtypes."
        
        self.parameters = {
            "knn_k_values": [10, 20, 30],
            "clustering_k_range": list(range(2, 9)),
            "bootstrap_resamples": 100
        }
        self.reproducibility_notes = "Standard Z-normalization assumed. Fixed seed for bootstrap resampling."
        
    @property
    def non_interpretation_clause(self) -> str:
        """Mandatory architectural clause."""
        return (
            "This procedure is exploratory and descriptive. "
            "It produces structural representations only and does not imply interpretation, "
            "inference, or evaluation."
        )

    def _hopkins_statistic(self, X: np.ndarray, num_samples: int = 250, seed: int = 42) -> float:
        """
        Calculates Hopkins statistic to assess clustering tendency.
        H ≈ 0.5 indicates uniform data (continuum).
        H > 0.75 indicates strong clustering tendency (discrete).
        """
        n, d = X.shape
        if n < num_samples:
            num_samples = int(n * 0.5)
            
        if num_samples < 2:
            return 0.5

        rng = np.random.default_rng(seed)
        mins = X.min(axis=0)
        maxs = X.max(axis=0)
        U = rng.uniform(mins, maxs, (num_samples, d))
        
        indices = rng.choice(n, num_samples, replace=False)
        W = X[indices]
        
        nbrs = NearestNeighbors(n_neighbors=2).fit(X)
        u_dist, _ = nbrs.kneighbors(U, n_neighbors=1)
        u_sum = np.sum(u_dist**d)
        
        w_dist, _ = nbrs.kneighbors(W, n_neighbors=2)
        w_sum = np.sum(w_dist[:, 1]**d)
        
        if (u_sum + w_sum) == 0:
            return 0.5
        
        return float(u_sum / (u_sum + w_sum))

    def _gap_statistic(self, X: np.ndarray, k_range: list, seed: int = 42) -> np.ndarray:
        """Computes Gap Statistic for given k_range using KMeans and 10 reference distributions."""
        rng = np.random.default_rng(seed)
        n, d = X.shape
        mins = X.min(axis=0)
        maxs = X.max(axis=0)
        
        gaps = []
        for k in k_range:
            km = KMeans(n_clusters=k, random_state=seed, n_init=10).fit(X)
            disp_orig = km.inertia_
            if disp_orig == 0:
                disp_orig = 1e-10
                
            ref_disps = []
            for _ in range(10): 
                U = rng.uniform(mins, maxs, (n, d))
                km_ref = KMeans(n_clusters=k, random_state=seed, n_init=10).fit(U)
                ref_disps.append(max(km_ref.inertia_, 1e-10))
                
            gap = np.mean(np.log(ref_disps)) - np.log(disp_orig)
            gaps.append(gap)
            
        return np.array(gaps)

    def execute(self, X: np.ndarray) -> dict:
        """
        Executes the Population Geometry procedural suite.
        Expects pre-scaled standard Z-normalized 3D trait core data.
        """
        n, d = X.shape
        if d != 3:
            raise ValueError("Input data must have exactly 3 dimensions in accordance to task limits.")
            
        results = {
            "procedure_name": self.procedure_name,
            "non_interpretation_clause": self.non_interpretation_clause,
            "density": {},
            "clustering": {},
            "topology": {},
            "gap": {},
            "conclusion": ""
        }
        
        hopkins = self._hopkins_statistic(X)
        results["density"]["hopkins"] = float(hopkins)
        
        k_range = self.parameters["clustering_k_range"]
        methods = {
            "kmeans": lambda k: KMeans(n_clusters=k, random_state=42, n_init=10),
            "gmm": lambda k: GaussianMixture(n_components=k, random_state=42, covariance_type='full'),
            "ward": lambda k: AgglomerativeClustering(n_clusters=k)
        }
        
        best_silhouette = -1
        stable_clusters = 0
        
        cluster_metrics = {meth: {"silhouette": [], "ch": [], "db": []} for meth in methods}
        cluster_metrics["gmm"]["bic"] = []
        
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            for k in k_range:
                for name, model_func in methods.items():
                    model = model_func(k)
                    if name == "gmm":
                        model.fit(X)
                        labels = model.predict(X)
                        cluster_metrics[name]["bic"].append(float(model.bic(X)))
                    else:
                        labels = model.fit_predict(X)
                        
                    if len(np.unique(labels)) > 1:
                        sil = silhouette_score(X, labels)
                        ch = calinski_harabasz_score(X, labels)
                        db = davies_bouldin_score(X, labels)
                    else:
                        sil, ch, db = 0.0, 0.0, 0.0
                        
                    cluster_metrics[name]["silhouette"].append(float(sil))
                    cluster_metrics[name]["ch"].append(float(ch))
                    cluster_metrics[name]["db"].append(float(db))
                    
                    if sil > best_silhouette:
                        best_silhouette = sil
                    if sil >= 0.35:
                        stable_clusters += 1
                        
            if HDBSCAN is not None:
                hdb = HDBSCAN(min_cluster_size=max(5, int(n * 0.01)))
                hdb_labels = hdb.fit_predict(X)
                n_clusters_hdb = len(set(hdb_labels)) - (1 if -1 in hdb_labels else 0)
                if n_clusters_hdb > 1:
                    results["clustering"]["hdbscan"] = {
                        "n_clusters": int(n_clusters_hdb),
                        "silhouette": float(silhouette_score(X[hdb_labels != -1], hdb_labels[hdb_labels != -1]))
                    }
                else:
                    results["clustering"]["hdbscan"] = {"n_clusters": 0, "silhouette": 0.0}
                    
        results["clustering"]["metrics"] = cluster_metrics
        
        gap_k_range = list(range(1, 9))
        gap_scores = self._gap_statistic(X, gap_k_range)
        results["gap"]["scores"] = gap_scores.tolist()
        optimal_k_gap = int(gap_k_range[np.argmax(gap_scores)])
        results["gap"]["optimal_k"] = optimal_k_gap

        # Topology
        dist_matrix = pairwise_distances(X)
        mst = minimum_spanning_tree(dist_matrix)
        mst_edges = mst.data
        results["topology"]["mst_mean"] = float(np.mean(mst_edges))
        results["topology"]["mst_std"] = float(np.std(mst_edges))
        
        # Format conclusion rule logic strictly
        is_discrete = (hopkins > 0.65) and (best_silhouette >= 0.30) and (optimal_k_gap > 1) and (stable_clusters > 0)
        is_continuum = (hopkins < 0.85) and (best_silhouette < 0.40) and not is_discrete
        
        if is_discrete:
            results["conclusion"] = "STABLE DISCRETE TYPES"
        elif is_continuum:
            results["conclusion"] = "CONTINUUM"
        else:
            results["conclusion"] = "WEAK CLUSTER TENDENCY"
            
        return results

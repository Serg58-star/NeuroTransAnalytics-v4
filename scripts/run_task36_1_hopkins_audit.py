"""
scripts/run_task36_1_hopkins_audit.py

Executes the Task 36.1 Hopkins Robustness Audit to verify if H=0.991 is a geometrical artifact.
Produces the Final Valuation Conclusion without interpretation.
"""

import sys
import os
import json
import warnings
import numpy as np
import pandas as pd
from pathlib import Path
from scipy.spatial import ConvexHull, Delaunay
from scipy.stats import chi2
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.decomposition import PCA
from sklearn.neighbors import NearestNeighbors

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
from run_stage7_population_real import load_features, reconstruct_residuals, DATABASE_PATH, LINEAR_CSV, CORE_RESIDUALS

# Output Directory
OUT_DIR = Path(__file__).parent.parent / "results" / "task36_1_hopkins_audit"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Custom Hopkins function to allow passing custom references (for Hull bounding, etc)
def calculate_hopkins(X: np.ndarray, num_samples: int = 250, seed: int = 42, reference_U: np.ndarray = None) -> float:
    n, d = X.shape
    if n < num_samples:
        num_samples = int(n * 0.5)
    
    if num_samples < 2:
        return 0.5

    rng = np.random.default_rng(seed)
    
    if reference_U is None:
        mins = X.min(axis=0)
        maxs = X.max(axis=0)
        U = rng.uniform(mins, maxs, (num_samples, d))
    else:
        # Uniform sample from provided reference distribution
        if len(reference_U) < num_samples:
            U = reference_U
            num_samples = len(reference_U)
        else:
            indices_U = rng.choice(len(reference_U), num_samples, replace=False)
            U = reference_U[indices_U]

    indices_W = rng.choice(n, num_samples, replace=False)
    W = X[indices_W]
    
    nbrs = NearestNeighbors(n_neighbors=2).fit(X)
    
    u_dist, _ = nbrs.kneighbors(U, n_neighbors=1)
    u_sum = np.sum(u_dist**d)
    
    w_dist, _ = nbrs.kneighbors(W, n_neighbors=2)
    w_sum = np.sum(w_dist[:, 1]**d)
    
    if (u_sum + w_sum) == 0:
        return 0.5
    
    return float(u_sum / (u_sum + w_sum))

def sample_in_convex_hull(X, num_samples, seed=42):
    """Uniform sampling inside the convex hull of X using rejection sampling."""
    rng = np.random.default_rng(seed)
    mins = X.min(axis=0)
    maxs = X.max(axis=0)
    
    try:
        hull = ConvexHull(X)
        delaunay = Delaunay(X[hull.vertices])
    except Exception:
        # Fallback if hull fails
        return rng.uniform(mins, maxs, (num_samples, X.shape[1]))
    
    samples = []
    attempts = 0
    max_attempts = num_samples * 50
    
    while len(samples) < num_samples and attempts < max_attempts:
        pts = rng.uniform(mins, maxs, (num_samples, X.shape[1]))
        in_hull = delaunay.find_simplex(pts) >= 0
        samples.extend(pts[in_hull])
        attempts += num_samples
        
    if len(samples) > num_samples:
        samples = samples[:num_samples]
    return np.array(samples)

def check_standardization(core_df):
    X_raw = core_df.values
    
    scaler_std = StandardScaler()
    X_std = scaler_std.fit_transform(X_raw)
    
    scaler_mm = MinMaxScaler()
    X_mm = scaler_mm.fit_transform(X_raw)
    
    pca_whiten = PCA(whiten=True)
    X_whiten = pca_whiten.fit_transform(X_std)
    
    pca_normal = PCA()
    X_pca = pca_normal.fit_transform(X_std)
    
    return {
        "Raw (4D)": calculate_hopkins(X_raw),
        "Z-Norm (4D)": calculate_hopkins(X_std),
        "MinMax (4D)": calculate_hopkins(X_mm),
        "PCA Space (Stage 7 Base)": calculate_hopkins(X_pca[:, :3]),
        "Whitened PCA (Isotropic)": calculate_hopkins(X_whiten[:, :3])
    }

def check_bounding_box(X_3d):
    try:
        hull = ConvexHull(X_3d)
        hull_vol = hull.volume
    except:
        hull_vol = np.nan
        
    mins = X_3d.min(axis=0)
    maxs = X_3d.max(axis=0)
    box_vol = np.prod(maxs - mins)
    
    ratio = hull_vol / box_vol if box_vol > 0 else np.nan
    
    U_hull = sample_in_convex_hull(X_3d, 1000)
    
    return {
        "Box Volume": float(box_vol),
        "Hull Volume": float(hull_vol),
        "Hull/Box Ratio": float(ratio),
        "H (Box Sampling)": calculate_hopkins(X_3d),
        "H (Hull Sampling)": calculate_hopkins(X_3d, reference_U=U_hull)
    }

def check_outliers(X_3d):
    cov = np.cov(X_3d, rowvar=False)
    inv_cov = np.linalg.inv(cov)
    mean = np.mean(X_3d, axis=0)
    
    diff = X_3d - mean
    mahala = np.sum(diff.dot(inv_cov) * diff, axis=1)
    
    threshold = chi2.ppf(0.99, df=3)
    
    mask = mahala <= threshold
    X_clean = X_3d[mask]
    
    outliers_removed = len(X_3d) - len(X_clean)
    
    return {
        "Outliers Removed (99th pct)": int(outliers_removed),
        "H (Pre-removal)": calculate_hopkins(X_3d),
        "H (Clean)": calculate_hopkins(X_clean)
    }

def check_ellipsoidal(X_3d):
    cov = np.cov(X_3d, rowvar=False)
    eigvals, _ = np.linalg.eigh(cov)
    eigvals = np.sort(eigvals)[::-1]
    
    ratio = eigvals[0] / (eigvals[-1] + 1e-10)
    
    # Whitening manually
    D = np.diag(1.0 / np.sqrt(eigvals + 1e-10))
    # Approximation of whitened space
    X_whiten = (X_3d - np.mean(X_3d, axis=0)).dot(D)
    
    return {
        "lambda_1": float(eigvals[0]),
        "lambda_2": float(eigvals[1]),
        "lambda_3": float(eigvals[2]),
        "lambda_1 / lambda_3 Ratio": float(ratio),
        "H (Whitened Sphere)": calculate_hopkins(X_whiten)
    }

def check_edge_density(X_3d):
    mins = X_3d.min(axis=0)
    maxs = X_3d.max(axis=0)
    ranges = maxs - mins
    
    edge_thr = 0.05
    lower_bounds = mins + edge_thr * ranges
    upper_bounds = maxs - edge_thr * ranges
    
    # A point is in the edge if it is outside [lower_bound, upper_bound] for ANY dimension
    in_edge = np.any((X_3d < lower_bounds) | (X_3d > upper_bounds), axis=1)
    prop_edge = np.mean(in_edge)
    
    # Expected proportion for uniform in 3D box where 10% of each dimension is edge
    exp_prop_edge = 1.0 - (1.0 - 2*edge_thr)**3
    
    return {
        "Empirical Edge Density (%)": float(prop_edge * 100),
        "Uniform Expected Edge (%)": float(exp_prop_edge * 100)
    }

def check_sampling_robustness(X_3d):
    # Running standard Hopkins 100 times with different seeds
    h_dist = [calculate_hopkins(X_3d, num_samples=250, seed=i) for i in range(100)]
    
    return {
        "Mean H": float(np.mean(h_dist)),
        "Std H": float(np.std(h_dist)),
        "Min H": float(np.min(h_dist)),
        "Max H": float(np.max(h_dist))
    }

def synthetic_replay():
    rng = np.random.default_rng(100)
    N = 1000
    
    # Uniform Box
    U_box = rng.uniform(-1, 1, (N, 3))
    
    # Elongated Ellipsoid
    U_ellipsoid = rng.normal(0, 1, (N, 3))
    U_ellipsoid[:, 0] *= 10.0 # stretch 10x
    
    # Gradient Density
    U_grad = rng.exponential(1.0, (N, 3))
    
    return {
        "Uniform Box 3D": calculate_hopkins(U_box),
        "Elongated Ellipsoid (10:1 ratio)": calculate_hopkins(U_ellipsoid),
        "Gradient Cloud": calculate_hopkins(U_grad)
    }

def generate_report(results, verdict):
    lines = [
        "# Task 36.1: Hopkins Robustness & Geometric Validation Audit Report",
        "",
        "## 1. Standardization Audit",
        "| Transformation | Hopkins Statistic (H) |",
        "|---|---|",
    ]
    for k, v in results["standardization"].items():
        lines.append(f"| {k} | {v:.4f} |")
        
    lines.extend([
        "",
        "## 2. Bounding Box Audit",
        "| Metric | Value |",
        "|---|---|",
    ])
    for k, v in results["bounding_box"].items():
        lines.append(f"| {k} | {v:.4f} |")

    lines.extend([
        "",
        "## 3. Outlier Impact (Mahalanobis 99th pct)",
        "| Metric | Value |",
        "|---|---|",
    ])
    for k, v in results["outliers"].items():
        val_str = str(v) if isinstance(v, int) else f"{v:.4f}"
        lines.append(f"| {k} | {val_str} |")
        
    lines.extend([
        "",
        "## 4. Ellipsoidal Geometry Check",
        "| Metric | Value |",
        "|---|---|",
    ])
    for k, v in results["ellipsoidal"].items():
        lines.append(f"| {k} | {v:.4f} |")
        
    lines.extend([
        "",
        "## 5. Edge Density Effect",
        "| Metric | Value (%) |",
        "|---|---|",
    ])
    for k, v in results["edge"].items():
        lines.append(f"| {k} | {v:.4f} |")

    lines.extend([
        "",
        "## 6. Sampling Robustness (N=100 bootstraps)",
        "| Metric | Value |",
        "|---|---|",
    ])
    for k, v in results["sampling"].items():
        lines.append(f"| {k} | {v:.4f} |")
        
    lines.extend([
        "",
        "## 7. Synthetic Reference Replay",
        "| Distribution Type | Hopkins Statistic (H) |",
        "|---|---|",
    ])
    for k, v in results["synthetic"].items():
        lines.append(f"| {k} | {v:.4f} |")

    lines.extend([
        "",
        "---",
        "## FINAL VALUATION CONCLUSION",
        f"**{verdict}**",
        ""
    ])
    return "\n".join(lines)


def main():
    print("=" * 60)
    print("TASK 36.1: HOPKINS ROBUSTNESS AUDIT")
    print("=" * 60)

    features_df = load_features(str(DATABASE_PATH))
    linear_csv = pd.read_csv(LINEAR_CSV, index_col=0)
    residuals_df = reconstruct_residuals(features_df, linear_csv)
    core_data = residuals_df[CORE_RESIDUALS].dropna()
    
    # Extract Base PCA 3D Space (used in Stage 7)
    scaler = StandardScaler()
    X_std = scaler.fit_transform(core_data.values)
    pca = PCA(n_components=3, random_state=42)
    X_3d = pca.fit_transform(X_std)
    
    print("\nRunning audits...")
    results = {
        "standardization": check_standardization(core_data),
        "bounding_box": check_bounding_box(X_3d),
        "outliers": check_outliers(X_3d),
        "ellipsoidal": check_ellipsoidal(X_3d),
        "edge": check_edge_density(X_3d),
        "sampling": check_sampling_robustness(X_3d),
        "synthetic": synthetic_replay()
    }
    
    # Evaluate Verdict
    # If Whitened H is severely drops < 0.70 while Original H is 0.99, it's heavily inflated by eigenvalues.
    # If Hull Sampling heavily drops H < 0.70, it's artificially inflated by the box bounds.
    h_hull = results["bounding_box"]["H (Hull Sampling)"]
    h_whitened = results["ellipsoidal"]["H (Whitened Sphere)"]
    
    if h_hull > 0.85 and h_whitened > 0.85:
        verdict = "HOPKINS_CONFIRMED"
    elif h_hull < 0.70 or h_whitened < 0.70:
        if h_hull < 0.60 or h_whitened < 0.60:
            verdict = "HOPKINS_ARTIFACT"
        else:
            verdict = "HOPKINS_PARTIALLY_INFLATED"
    else:
        verdict = "HOPKINS_PARTIALLY_INFLATED"

    report = generate_report(results, verdict)
    
    with open(OUT_DIR / "Task_36_1_Audit_Report.md", "w", encoding="utf-8") as f:
        f.write(report)
        
    with open(OUT_DIR / "audit_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4)
        
    print(f"\nFinal Verdict: {verdict}")
    print(f"Results saved to {OUT_DIR}")
    
    return 0

if __name__ == "__main__":
    exit(main())

import os
import sqlite3
import pandas as pd
import numpy as np
from src.c3x_exploratory.exgaussian_integration import ExGaussianIntegrationAnalysis
from src.c3x_exploratory.microdynamics import MicrodynamicAnalysis
from src.c3x_exploratory.variability import VariabilityAnalysis

DB_PATH = "c:/NeuroTransAnalytics-v4/neuro_data.db"

def fetch_real_data(db_path: str) -> pd.DataFrame:
    """Fetch structured block data per subject from neuro_data.db."""
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Database not found at {db_path}")
        
    conn = sqlite3.connect(db_path)
    
    query = "SELECT subject_id, "
    cols = [f"tst{test}_{trial}" for test in [1, 2, 3] for trial in range(1, 37)]
    query += ", ".join(cols) + " FROM trials;"
    
    df_wide = pd.read_sql_query(query, conn)
    conn.close()
    
    # Pivot
    records = []
    for idx, row in df_wide.iterrows():
        subj = row["subject_id"]
        for test in [1, 2, 3]:
            for trial in range(1, 37):
                val = row[f"tst{test}_{trial}"]
                if pd.notna(val) and val > 0:
                    records.append({
                        "subject_id": subj,
                        "test_id": test,
                        "rt": val
                    })
    return pd.DataFrame(records)

def run_exgaussian_integration():
    print("Loading real experimental data for Task 35.2 (Ex-Gaussian Integration)...")
    df = fetch_real_data(DB_PATH)
    
    exg_analyzer = ExGaussianIntegrationAnalysis()
    micro_analyzer = MicrodynamicAnalysis()
    var_analyzer = VariabilityAnalysis()
    
    results = []
    
    for (subj, test_id), group in df.groupby(["subject_id", "test_id"]):
        rt_series = group["rt"].values
        if len(rt_series) < 20: # Require a solid chunk of valid trials
            continue
            
        # 1. Macro features
        median_rt = np.median(rt_series)
        mad = np.median(np.abs(rt_series - median_rt))
        
        # 2. Ex-Gaussian features
        exg = exg_analyzer.execute(rt_series)["exgaussian_parameters"]
        
        # 3. Microdynamic features
        bursts = micro_analyzer.analyze_bursts(rt_series)["total_burst_frequency"]
        
        # 4. Tail Geometry features
        skew = var_analyzer.analyze_skew_kurtosis(rt_series)["skewness"]
        
        results.append({
            "subject_id": subj,
            "test_id": test_id,
            "median_rt": median_rt,   # Proxy for Speed Axis
            "mad": mad,               # Tightly coupled to Speed
            "mu": exg["mu"],
            "sigma": exg["sigma"],
            "tau": exg["tau"],
            "burst_freq": bursts,     # Proxy for Microdymamics
            "skewness": skew          # Proxy for Tail Geometry
        })
        
    results_df = pd.DataFrame(results).dropna()
    print(f"\nExtraction complete. N={len(results_df)} valid test blocks.")
    
    print("\n--- Correlation Structure (Spearman) ---")
    corr_cols = ["median_rt", "tau", "mu", "sigma", "burst_freq", "skewness"]
    corr = results_df[corr_cols].corr(method="spearman").round(3)
    print(corr)
    
    print("\n--- Extended PCA Structure ---")
    # Build feature matrix
    pca_cols = ["median_rt", "mu", "sigma", "tau", "burst_freq", "skewness"]
    feature_matrix = results_df[pca_cols].values
    
    pca_metrics = exg_analyzer.compute_pca_structure(feature_matrix)
    print("Metrics included:", ", ".join(pca_cols))
    print(f"Eigenvalues: {[round(e, 3) for e in pca_metrics['eigenvalues']]}")
    print(f"Explained Variance Ratio: {[round(r, 3) for r in pca_metrics['explained_variance_ratio']]}")
    print(f"Participation Ratio (PR): {round(pca_metrics['participation_ratio'], 3)}")
    
    print("\nInterpretation Guidelines:")
    print("1. If tau correlates strongly with median_rt -> tau is embedded in Speed.")
    print("2. If tau strongly correlates with burst_freq -> tau tracks state-transition frequency.")
    print("3. If PR > 3.0 and lowest eigenvalue > 0.5 -> extended feature space possesses true irreducible dimensionality.")

if __name__ == "__main__":
    run_exgaussian_integration()

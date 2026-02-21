import os
import sqlite3
import pandas as pd
import numpy as np

from src.c3x_exploratory.parametric_modeling import ParametricModelingAnalysis

DB_PATH = "c:/NeuroTransAnalytics-v4/neuro_data.db"

def fetch_real_data(db_path: str) -> pd.DataFrame:
    """Fetch structured block data per subject from neuro_data.db using trials table."""
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Database not found at {db_path}")
        
    conn = sqlite3.connect(db_path)
    
    # Query all valid test values
    query = "SELECT subject_id, "
    
    cols = []
    for test in [1, 2, 3]:
        for trial in range(1, 37):
            cols.append(f"tst{test}_{trial}")
            
    query += ", ".join(cols) + " FROM trials;"
    
    df_wide = pd.read_sql_query(query, conn)
    conn.close()
    
    # Pivot from wide to long format
    records = []
    for idx, row in df_wide.iterrows():
        subj = row["subject_id"]
        for test in [1, 2, 3]:
            for trial in range(1, 37):
                val = row[f"tst{test}_{trial}"]
                if pd.notna(val) and val > 0: # Only keep valid RTs > 0
                    records.append({
                        "subject_id": subj,
                        "test_id": test,
                        "trial_idx": trial,
                        "rt": val
                    })
                    
    df_long = pd.DataFrame(records)
    return df_long

def run_stage6_parametric():
    """Run Parametric Distribution Modeling on all subjects/tests."""
    print("Loading real experimental data for Task 35.1 (Parametric Modeling)...")
    df = fetch_real_data(DB_PATH)
    
    analyzer = ParametricModelingAnalysis()
    
    results = []
    
    for (subj, test_id), group in df.groupby(["subject_id", "test_id"]):
        rt_series = group["rt"].values
        
        # We need at least 15 valid trials to fit reliably
        if len(rt_series) < 15:
            continue
            
        metrics = analyzer.execute(rt_series)
        
        fits = metrics["fits"]
        row = {
            "subject_id": subj,
            "test_id": test_id,
            "n_trials": len(rt_series),
            "best_fit_aic": fits["best_fit_aic"],
            "best_fit_bic": fits["best_fit_bic"],
            "norm_aic": fits["normal"]["aic"],
            "lognorm_aic": fits["lognormal"]["aic"],
            "gamma_aic": fits["gamma"]["aic"],
            "weibull_aic": fits["weibull"]["aic"],
            "exgauss_aic": fits["exgaussian"]["aic"]
        }
        results.append(row)
        
    results_df = pd.DataFrame(results)
    print("\nExtraction complete.")
    
    if len(results_df) == 0:
        print("No valid test sequences found.")
        return
        
    print("\n--- Summary: Dominant Generative Models ---")
    print("\nBy AIC (Akaike Information Criterion):")
    print(results_df["best_fit_aic"].value_counts(normalize=True).round(3) * 100)
    
    print("\nBy BIC (Bayesian Information Criterion):")
    print(results_df["best_fit_bic"].value_counts(normalize=True).round(3) * 100)
    
    print("\nProcedure execution finished. Interpretations of the population dominance should be documented.")

if __name__ == "__main__":
    run_stage6_parametric()

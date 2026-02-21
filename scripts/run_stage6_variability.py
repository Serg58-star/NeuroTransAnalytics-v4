import os
import sqlite3
import pandas as pd
import numpy as np

from src.c3x_exploratory.variability import VariabilityAnalysis

DB_PATH = "c:/NeuroTransAnalytics-v4/neuro_data.db"

def fetch_real_data(db_path: str) -> pd.DataFrame:
    """Fetch structured block data per subject."""
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Database not found at {db_path}")
        
    conn = sqlite3.connect(db_path)
    
    # query all valid test values (ignoring -1 which might be missing)
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
def run_stage_6():
    """Run Variability Analysis on all subjects/tests."""
    print("Loading real experimental data for Stage 6...")
    df = fetch_real_data(DB_PATH)
    
    analyzer = VariabilityAnalysis()
    
    results = []
    
    for (subj, test_id), group in df.groupby(["subject_id", "test_id"]):
        rt_series = group["rt"].values
        
        # We need at least 15 valid trials to make reliable shape geometry inference
        if len(rt_series) < 15:
            continue
            
        metrics = analyzer.execute(rt_series)
        
        row = {
            "subject_id": subj,
            "test_id": test_id,
            "n_trials": len(rt_series),
            "skewness": metrics["skew_kurtosis"]["skewness"],
            "kurtosis": metrics["skew_kurtosis"]["kurtosis"],
            "tail_absolute": metrics["tail_geometry"]["tail_absolute"],
            "tail_normalized": metrics["tail_geometry"]["tail_normalized"],
            "tail_to_mad_ratio": metrics["tail_geometry"]["tail_to_mad_ratio"],
            "mad": metrics["variance"]["mad"],
            "cv_robust": metrics["variance"]["cv_robust"]
        }
        results.append(row)
        
    results_df = pd.DataFrame(results)
    print("\nExtraction complete.")
    
    if len(results_df) == 0:
        print("No valid test sequences found.")
        return
        
    print("\n--- Summary Statistics across N={} sequences ---".format(len(results_df)))
    print(results_df[["skewness", "kurtosis", "tail_absolute", "tail_to_mad_ratio", "cv_robust"]].describe().round(3))
    
    # Check for Speed-Stability trade-off (correlation median <-> mad)
    # This requires merging with median, which we can compute quickly here
    medians = df.groupby(["subject_id", "test_id"])["rt"].median().reset_index()
    medians.columns = ["subject_id", "test_id", "median_rt"]
    
    merged = pd.merge(results_df, medians, on=["subject_id", "test_id"])
    
    print("\n--- Structural Correlations ---")
    corr = merged[["median_rt", "mad", "skewness", "tail_to_mad_ratio"]].corr(method="spearman").round(3)
    print(corr)
    
    print("\n--- Interpretation Guidelines for Integration ---")
    print("1. If MAD and median_rt are highly correlated -> Speed/Stability are coupled.")
    print("2. If Skewness/Tail-MAD are independent from median_rt -> Shape geometry may be a separate axis.")
    print("\nProcedure execution finished. Output is strictly structural.")

if __name__ == "__main__":
    run_stage_6()

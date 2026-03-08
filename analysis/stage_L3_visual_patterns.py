import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys

sys.path.append(os.path.abspath("analysis"))
import robust_statistics as rs

DB_PATH = "neuro_data.db"
COMPONENTS_PATH = "docs/audit_legacy/Stage L/L_results/L_component_dataset.csv"
FIG_DIR = "docs/audit_legacy/Stage L/figures"

def generate_visualizations():
    os.makedirs(FIG_DIR, exist_ok=True)
    
    print(f"Loading data from {COMPONENTS_PATH}...")
    df = pd.read_csv(COMPONENTS_PATH)
    
    # Restructure for comparison
    # We want to compare the distribution of delta_v4 and delta_v5_mt
    df_v4 = df.dropna(subset=['delta_v4']).copy()
    df_v5 = df.dropna(subset=['delta_v5_mt']).copy()
    
    df_v4['component'] = 'Delta V4 (Color-Simple)'
    df_v4['delta_val'] = df_v4['delta_v4']
    
    df_v5['component'] = 'Delta V5/MT (Shift-Simple)'
    df_v5['delta_val'] = df_v5['delta_v5_mt']
    
    df_combined = pd.concat([df_v4, df_v5], ignore_index=True)
    
    # 4.1 RT Distribution -> Component Distribution
    print("Generating rt_distribution.png...")
    plt.figure(figsize=(10,6))
    sns.histplot(data=df_combined, x='delta_val', hue='component', bins=60, kde=True, palette='muted')
    plt.title("Functional Component Transition Distribution ($\Delta V$)")
    plt.xlabel("Delta Time (ms)")
    plt.ylabel("Frequency")
    plt.savefig(os.path.join(FIG_DIR, "rt_distribution.png")) # Keep legacy name for runner but content changed
    plt.close()
    
    print("Generating rt_distribution_by_test.png...")
    plt.figure(figsize=(10,6))
    sns.boxplot(data=df_combined, x='delta_val', y='component', palette='muted')
    plt.title("Component Timing by Type")
    plt.xlabel("Delta Time (ms)")
    plt.ylabel("Component")
    plt.savefig(os.path.join(FIG_DIR, "rt_distribution_by_test.png"))
    plt.close()
    
    # 4.2 RT vs PSI -> Component vs PSI
    print("Generating rt_vs_psi.png...")
    # Group by PSI and calculate median Delta
    median_psi = df_combined.groupby(['psi', 'component'])['delta_val'].median().reset_index()
    plt.figure(figsize=(12,6))
    sns.lineplot(data=median_psi, x='psi', y='delta_val', hue='component', marker='o')
    plt.title("Median Component Timing vs Pre-Stimulus Interval (PSI)")
    plt.xlabel("PSI (ms)")
    plt.ylabel("Median Delta (ms)")
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.savefig(os.path.join(FIG_DIR, "rt_vs_psi.png"))
    plt.close()
    
    # 4.3 RT vs Visual Field -> Component vs Visual Field
    print("Generating rt_vs_field.png...")
    plt.figure(figsize=(10,6))
    sns.boxplot(data=df_combined, x='stim_pos', y='delta_val', hue='component', order=['left', 'center', 'right'], palette='Set2')
    plt.title("Component Timing by Visual Field")
    plt.xlabel("Visual Field")
    plt.ylabel("Delta Time (ms)")
    plt.savefig(os.path.join(FIG_DIR, "rt_vs_field.png"))
    plt.close()
    
    # 4.4 RT vs Stimulus Index -> Component vs Stimulus Index
    print("Generating rt_vs_index.png...")
    plt.figure(figsize=(14,6))
    # using np.median, and IQR for error shading
    sns.lineplot(data=df_combined, x='stimulus_index', y='delta_val', hue='component', estimator=np.median, errorbar=('pi', 50), marker='s')
    plt.title("Median Component Timing vs Stimulus Index (with IQR)")
    plt.xlabel("Stimulus Index (1-36)")
    plt.ylabel("Median Delta (ms)")
    plt.xticks(range(1, 37))
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.savefig(os.path.join(FIG_DIR, "rt_vs_index.png"))
    plt.close()
    
    # 4.5 RT vs Test Type -> Delta V1/V4/V5 comparison
    print("Generating rt_vs_test_type.png...")
    # Let's show V1, V4, V5 magnitudes here
    df_v1 = df.dropna(subset=['delta_v1']).copy()
    df_v1['component'] = 'Delta V1 (Base)'
    df_v1['delta_val'] = df_v1['delta_v1']
    df_all = pd.concat([df_v1, df_v4, df_v5], ignore_index=True)
    
    plt.figure(figsize=(10,6))
    sns.barplot(data=df_all, x='component', y='delta_val', palette='pastel', estimator=np.median, errorbar=('pi', 50))
    plt.title("Median Component Magnitudes ($\Delta V1, \Delta V4, \Delta V5$)")
    plt.xlabel("Component")
    plt.ylabel("Median Timing (ms)")
    plt.savefig(os.path.join(FIG_DIR, "rt_vs_test_type.png"))
    plt.close()
    
    # 4.6 Error Structure (Keep SQL query for errors as errors are trial-level, not component-level)
    print("Generating errors_by_test_type.png...")
    conn = sqlite3.connect(DB_PATH)
    query_errors = '''
        SELECT 'simple' AS test_type, SUM(tst1_premature) AS premature, SUM(tst1_late) AS late FROM trials
        UNION ALL
        SELECT 'shift' AS test_type, SUM(tst3_premature) AS premature, SUM(tst3_late) AS late FROM trials
        UNION ALL
        SELECT 'color' AS test_type, SUM(tst2_premature) AS premature, SUM(tst2_late) AS late FROM trials
    '''
    df_errors = pd.read_sql(query_errors, conn)
    conn.close()
    
    df_errors_melted = df_errors.melt(id_vars="test_type", var_name="error_type", value_name="count")
    
    plt.figure(figsize=(10,6))
    sns.barplot(data=df_errors_melted, x='test_type', y='count', hue='error_type', order=['simple', 'shift', 'color'], palette='pastel')
    plt.title("Premature vs Late Errors by Test Type")
    plt.xlabel("Test Type")
    plt.ylabel("Total Error Count")
    plt.savefig(os.path.join(FIG_DIR, "errors_by_test_type.png"))
    plt.close()
    
    print("Visualizations created successfully.")

if __name__ == '__main__':
    generate_visualizations()

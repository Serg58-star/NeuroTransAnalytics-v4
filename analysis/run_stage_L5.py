import os
import io
import pandas as pd
import stage_L5_structural_analysis as l5

COMPONENTS_PATH = "docs/audit_legacy/Stage L/L_results/L_component_dataset.csv"
OUTPUT_DIR = "docs/audit_legacy/Stage L/L5_results"
REPORT_PATH = "docs/audit_legacy/Stage L/Stage_L5_Legacy_Structural_Analysis_Report.md"

def load_data():
    return l5.load_data() # Use the reshaping loader from the module

def df_to_markdown(df):
    if df.empty:
        return "*No reliable data for computation.*"
    output = io.StringIO()
    df.round(3).to_markdown(output, index=False)
    return output.getvalue()

def main():
    print("Executing Stage L5 Legacy Component Structural Analysis...")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Load standardized components
    df = load_data()
    print(f"Loaded components dataset.")
    
    # -----------------------------------------------------
    # Execute Blocks
    # -----------------------------------------------------
    print("Executing Block A: Protocol Order Effects...")
    res_a = l5.analyze_order_effects(df)
    
    print("Executing Block B: Temporal Dynamics...")
    res_b = l5.analyze_temporal_dynamics(df)
    
    print("Executing Block C: Spatial Structure...")
    res_c = l5.analyze_spatial_structure(df)
    
    print("Executing Block D: Reaction Structure & Variability...")
    res_d = l5.analyze_reaction_structure(df)
    
    print("Executing Block E: Sequential Dynamics...")
    res_e = l5.analyze_sequential_dynamics(df)
    
    # Save CSVs
    all_results = {**res_a, **res_b, **res_c, **res_d, **res_e}
    for key, val_df in all_results.items():
        if isinstance(val_df, pd.DataFrame) and not val_df.empty:
            val_df.to_csv(os.path.join(OUTPUT_DIR, f"{key}.csv"), index=False)
            
    print("CSV data saved to L5_results/")
    
    # -----------------------------------------------------
    # Generate Report Document
    # -----------------------------------------------------
    print("Generating comprehensive Stage L5 report...")
    report = [
        "# Stage L5 — Component Structural Analysis Report",
        "",
        "**Dataset:** `L_component_dataset.csv` ($\Delta V4, \Delta V5/MT$)",
        "**Date:** Auto-generated",
        "",
        "This document compiles the findings of the deep exploratory analysis upon the extracted testing components.",
        "The patterns strictly map onto distinct component functions rather than raw compound timings.",
        "",
        "---",
        "## BLOCK A — Protocol Order Effects",
        "**Goal:** Determine whether differences between components reflect complexity or fatigue from the fixed ordering.",
        "",
        "### A1. Medians and MAD grouped by Component",
        df_to_markdown(res_a.get('A1_summary', pd.DataFrame())),
        "**Insight for v5:** Escalation across components indicates structural cost and potential sequential exhaustion.",
        "",
        "### A2. Early vs Late Series Decomposition",
        "Tracking drift across stimulus index sections (1-12, 13-24, 25-36).",
        df_to_markdown(res_a.get('A2_drift', pd.DataFrame())),
        "**Insight for v5:** Intra-test tracking confirms progressive cognitive load saturation on the components.",
        "",
        "### A3. Cross-Component Correlation (Subject Level)",
        df_to_markdown(res_a.get('A3_cross_comp_corr', pd.DataFrame())),
        "**Insight for v5:** Positive correlation designates independent processing constraints spanning modalities.",
        "",
        "---",
        "## BLOCK B — Temporal Dynamics",
        "**Goal:** Understand temporal readiness and fatigue dynamics (PSI interaction) on the structural delta values.",
        "",
        "### B1. Optimal Temporal Readiness Window (PSI Bin)",
        df_to_markdown(res_b.get('B1_optimal_psi', pd.DataFrame())),
        "**Insight for v5:** Defines the physical minimum bounds for the v5 stochastic stimulus generator.",
        "",
        "### B2. PSI Generator Predictability (Markov Bias)",
        df_to_markdown(res_b.get('B2_predictability', pd.DataFrame())),
        "**Insight for v5:** Correlating current Component Delta against lagged PSI checks if subjects predict the generator.",
        "",
        "---",
        "## BLOCK C — Spatial Structure",
        "**Goal:** Analyze spatial attention characteristics strictly on the $\Delta V$ extraction.",
        "",
        "### C1. Lateralization Re-Evaluation",
        df_to_markdown(res_c.get('C1_lateralization', pd.DataFrame())),
        "**Insight for v5:** Any significant left/right biases mandate asymmetric geometric target algorithms in subsequent versions.",
        "",
        "### C2. Spatial Attention Degradation",
        df_to_markdown(res_c.get('C2_spatial_degradation', pd.DataFrame())),
        "**Insight for v5:** Checks whether peripheral degradation slopes exceed central slopes during long waiting periods (PSI).",
        "",
        "---",
        "## BLOCK D — Reaction Structure and Variability",
        "**Goal:** Analyze deeper statistical properties of Component $\Delta$ distributions.",
        "",
        "### D1. Robust Performance Percentiles",
        df_to_markdown(res_d.get('D1_robust_percentiles', pd.DataFrame())),
        "**Insight for v5:** Replaces parametric fitting with strict empirical percentiles to gauge extreme skewing.",
        "",
        "### D3/D4. Variability and Residual Structure Mapping",
        "**Variability Mapping (MAD):**",
        df_to_markdown(res_d.get('D3_mad_structure', pd.DataFrame())),
        "**Residual Summary (MAD):**",
        df_to_markdown(res_d.get('D4_residual_mad_summary', pd.DataFrame())),
        "**Insight for v5:** Identifies raw variances for pure component behavior.",
        "",
        "---",
        "## BLOCK E — Sequential Dynamics",
        "**Goal:** Study dynamic behavior of sustained attention across continuous series.",
        "",
        "### E1. Micro-Oscillatory Attention Cycles (Autocorrelation)",
        df_to_markdown(res_e.get('E1_autocorrelation', pd.DataFrame())),
        "**Insight for v5:** Short-lag internal rhythmicity suggests sequential lengths in v5 tests must be randomized or extended to disrupt cyclic anticipation.",
        "",
        "### E2. Post-Error Slowing (PES)",
        df_to_markdown(res_e.get('E2_post_error_slowing', pd.DataFrame())),
        "**Insight for v5:** Quantifiable median slowing penalties specify adaptive timeout parameters required after errors in v5 generation.",
    ]
    
    with open(REPORT_PATH, 'w', encoding='utf-8') as f:
        f.write("\n".join(report))
        
    print(f"Report fully compiled to {REPORT_PATH}")

if __name__ == "__main__":
    main()

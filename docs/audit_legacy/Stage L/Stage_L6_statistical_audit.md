# Stage L6 Statistical Audit Report

**Date:** Auto-generated

This document registers the presence of non-robust statistics inside Stage-L analytical codebase.

| File | Line | Content |
|---|---|---|
| stage_L3_visual_patterns.py | 52 | $ mean_psi = df_combined.groupby(['psi', 'component'])['delta_val'].mean().reset_index() $ |
| stage_L4_model_adapter.py | 56 | $ beta0 = comp_df[comp_col].mean() - beta1 * comp_df['psi'].mean() $ |
| stage_L4_model_adapter.py | 71 | $ left_delta = comp_df[comp_df['stim_pos'] == 'left'][comp_col].mean() $ |
| stage_L4_model_adapter.py | 72 | $ center_delta = comp_df[comp_df['stim_pos'] == 'center'][comp_col].mean() $ |
| stage_L4_model_adapter.py | 73 | $ right_delta = comp_df[comp_df['stim_pos'] == 'right'][comp_col].mean() $ |
| stage_L4_model_adapter.py | 92 | $ seq_means = comp_df.groupby('stimulus_index')[comp_col].mean().sort_index() $ |
| stage_L5_structural_analysis.py | 60 | $ subj_means = df.groupby(['subject_id', 'component'])['delta_val'].mean().unstack().dropna() $ |
| stage_L5_structural_analysis.py | 102 | $ if len(subj_df) > 5 and subj_df['psi'].std() > 0: $ |
| stage_L5_structural_analysis.py | 103 | $ slope, _, _, _, _ = stats.linregress(subj_df['psi'], subj_df['delta_val']) $ |
| stage_L5_structural_analysis.py | 127 | $ slope, _, _, _, _ = stats.linregress(sub['psi'], sub['delta_val']) $ |
| stage_L5_structural_analysis.py | 152 | $ d3_var = df.groupby(['component', 'stim_pos'])['delta_val'].std().reset_index().rename(columns={'delta_val': 'delta_std'}) $ |
| stage_L5_structural_analysis.py | 160 | $ slope, intercept, _, _, _ = stats.linregress(sub_df['psi'], sub_df['delta_val']) $ |
| stage_L5_structural_analysis.py | 197 | $ baseline = np.mean(deltas) $ |
| stage_L5_structural_analysis.py | 208 | $ 'baseline_delta': baseline, 'mean_post_error_delta': np.mean(pes_deltas) $ |

**Total violations:** 14


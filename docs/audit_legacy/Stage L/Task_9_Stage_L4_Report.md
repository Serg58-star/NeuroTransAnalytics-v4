# Task 9 Stage L4 Report — Model Integration

Dataset: `neuro_data.db`
Generated automatically by `run_stage_L4.py`.

## Overview
This report documents the integration of legacy Boxbase `reactions_view` data into existing analytical functions derived from the `src/` modules verified during Task 8.
The models were invoked cleanly via the `stage_L4_model_adapter.py` interface without modifying the previously validated `src/` core functions.

---

## 1. Robust Percentile Component Parameters
Calculated replacing Ex-Gaussian fits with deterministic non-parametric indices (Median, MAD, IQR).

| component           |   median_ms |   mad_ms |   iqr_ms |
|:--------------------|------------:|---------:|---------:|
| Delta V4 (Color)    |         108 |       36 |       73 |
| Delta V5/MT (Shift) |         129 |       46 |       96 |

---

## 2. Robust PSI Sensitivity Modeling
Assessed relationship between distinct Pre-Stimulus Interval (PSI) bins and Median $\Delta$ RT.

| component           |   median_short_psi_ms |   median_medium_psi_ms |   median_long_psi_ms |   psi_long_vs_short_ms |
|:--------------------|----------------------:|-----------------------:|---------------------:|-----------------------:|
| Delta V4 (Color)    |                   121 |                     95 |                   94 |                    -27 |
| Delta V5/MT (Shift) |                   145 |                    119 |                  118 |                    -27 |

---

## 3. Lateralization Indices
Positional analysis using Robust Medians corresponding to central and peripheral visual fields.

| component           |   Delta_left_ms |   Delta_center_ms |   Delta_right_ms |   lateralization_index_ms |
|:--------------------|----------------:|------------------:|-----------------:|--------------------------:|
| Delta V4 (Color)    |             115 |               109 |            100   |                     -15   |
| Delta V5/MT (Shift) |             136 |               127 |            124.5 |                     -11.5 |

---

## 4. Non-Parametric Intra-Series Dynamics
Trend analysis applying Spearman rank correlation across progressive median $\Delta V$'s.

| component           |   trend_spearman_rho |   trend_pval |   series_start_delta_ms |   series_end_delta_ms |
|:--------------------|---------------------:|-------------:|------------------------:|----------------------:|
| Delta V4 (Color)    |            0.223209  |     0.19068  |                      74 |                 122   |
| Delta V5/MT (Shift) |           -0.0695294 |     0.686991 |                     130 |                 148.5 |

---

## Conclusion
The models were successfully adjusted to strictly use robust statistics across independent components.
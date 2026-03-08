# Task L6 Statistical Corrections — Implementation Plan

Date: March 8, 2026
Version: v1
Status: Proposed (Awaiting Approval)
Reference: `Task — Исправление статистических нарушений Stage-L.md`

## 1. Goal Description

The Stage L architecture currently relies on non-robust statistics (`mean`, `std`, `var`, `sem`) in L3, L4, L5 analyses. This violates the project's strict Robust Statistics Standard.

This plan outlines the complete removal of mean-based metrics and models across Stage-L components and replacing them exclusively with Median and MAD (Median Absolute Deviation), alongside recalculation of all datasets and reports.

## User Review Required
>
> [!IMPORTANT]
> The plan proposes substantial modifications to the previously written Stage-L scripts (L3, L4, L5) to completely replace parametric evaluations (mean, standard deviation, variance, Ex-Gaussian tau/mu, linear regressions on means) with non-parametric equivalents (median, MAD, IQR, median binning).
> Please explicitly approve this Implementation Plan (v1) before execution begins!

## Proposed Changes

### 1. Robust Statistics Core Module

#### [NEW] `analysis/robust_statistics.py`

A new utility file will encompass all allowed statistical calculations:

- `median_value(data)`
- `mad_value(data)` — utilizing standard Median Absolute Deviation.
- `iqr_value(data)`
- `percentile_range(data, p_low, p_high)`

### 2. Analytical Script Modifications

#### [MODIFY] `analysis/stage_L3_visual_patterns.py`

- Replace all `.mean()` calls with median calculations.
- Replace `.std()` and `.sem()` with MAD.
- In seaborn plotting functions, inject `estimator=np.median` and provide custom errorbar logic based on IQR/MAD.

#### [MODIFY] `analysis/stage_L4_model_adapter.py`

- Remove Ex-Gaussian parametric fitting.
- Remove ordinary least squares (OLS) linear regressions (PSI → RT).
- Implement Median $\Delta V$ by PSI bins.

#### [MODIFY] `analysis/stage_L5_structural_analysis.py`

- Replace aggregated variables: `mean_delta` → `median_delta`, `var_delta`, `delta_std` → `mad_delta`, `sem_delta` → MAD-scaled error.
- Adjust algorithms to strictly summarize over medians.

### 3. Reporting and Artifact generation Layer

- **Audit Script**: Generate `docs/audit_legacy/Stage L/Stage_L6_statistical_audit.md`.
- **Validation Script**: Generate `docs/audit_legacy/Stage L/Stage_L6_validation_report.md`.
- **Regenerate Results**: Run updated pipelines to emit the final versions of L3, L4, and L5 reports.

## Verification Plan

1. Code Audit across L-scripts for forbidden strings (`mean`, `std`, `var`, `sem`, `linregress`).
2. Verify visual outputs reference median and MAD.

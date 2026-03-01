# Stage 9B — Implementation Plan (Functional Monitoring Framework v5)

**Version:** v1
**Date:** 2026-03-01

## 1. Goal Description

Establish the longitudinal Functional Monitoring Framework for the v5 Dual-Space Architecture. This stage transitions the geometric models from synthetic static/two-phase states into a continuous N-timepoint monitoring scaffold. We will compute longitudinal metrics (ΔSeverity, Acceleration, DII), construct stability envelopes, define the Early Instability Threshold (EIT), and classify the geometric vector field over time. This is a pure monitoring framework (no predictive risk scoring yet).

## 2. User Review Required
>
> [!IMPORTANT]
> Pursuant to the Governance Rule, **explicit written approval** is required before execution of this architectural implementation plan.
> Please provide the following phrase to approve: **"Approved for implementation. Reference: Stage 9B v1"**

## 3. Proposed Changes

### [MODIFY] `src/stage9A_v5_architecture/validation/population_generator_v5.py`

- Add a new generation mode supporting N consecutive timepoints per subject (`generate_longitudinal_population(n_subjects, timepoints)`).
- Timepoints will mathematically evolve: starting stable ($t=0$), entering load/fatigue ($t=k$), and either recovering or collapsing ($t=N$).
- The data structure will return `(N_subjects, Timepoints, 12)` arrays.

### [NEW] `src/stage9A_v5_architecture/validation/task_9B_longitudinal_monitoring.py`

- Iterate over the generated longitudinal time points to evaluate each subject's trajectory.
- **Severity Core:** Compute $S_i(t)$ utilizing the locked MCD Robust Covariance model from Task 51A.
- **Load Geometry:** Compute $\Delta Z_i(t) = Z_{F(t)}^{anchored} - Z_{F(t-1)}$ utilizing the anchored standardizer from Task 52A.
- **Trajectory Metrics:**
  - `Slope` ($S_i(t) - S_i(t-1)$).
  - `Acceleration` ($S_i(t) - 2S_i(t-1) + S_i(t-2)$).
- **Stability Scaffold:**
  - Build the Envelope (Median, IQR, 95th Percentile) for $S$ and $\Delta S$.
  - Define EIT triggers: Slope > 95th %ile OR DII > 90th %ile OR 3-step positive Acceleration.
  - Quadrant Classification (Severity vs DII interaction).
- **Output:** Generate `Stage_9B_Functional_Monitoring_Report.md` containing metrics, envelope verification, and mathematical stability proofs over time (Silhouette < 0.25).

## 4. Verification Plan

1. Run the `task_9B_longitudinal_monitoring.py` script bridging the new generative data.
2. Verify that the envelope boundaries are smooth and continuous (no bimodal fracturing).
3. Check the condition covariance matrices and topological coherence boundaries (Silhouette score).
4. Assert all Stage 9B requirements are met to declare the Monitoring Framework LOCKED (Synthetic).

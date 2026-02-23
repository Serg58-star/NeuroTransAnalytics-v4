# Task 43 — Real Longitudinal Dataset Integration  
## Stage 9B Functional Monitoring Framework  
**NeuroTransAnalytics-v4**

**Version:** v1  
**Date:** 2026-02-23  
**Branch Target:** `feature/stage9B_functional_monitoring_framework`  
**Status:** Draft — Approval Required Before Implementation  

---

# 1. Context

Stage 9B Functional Monitoring Framework v1:

- Implemented  
- Deterministically validated on synthetic trajectory (SUBJ-001)  
- Architecture boundaries preserved  
- No mutation of C3-Core  
- No mutation of Stage 9A  
- `k_min_consecutive = 2` locked  

The framework has been validated only on synthetic sequences.

Next step:

> Empirically validate longitudinal monitoring behaviour on real repeated-session data without altering geometry or fluctuation logic.

---

# 2. Objective

Integrate real longitudinal session data from `neuro_data.db` into the Stage 9B monitoring pipeline to:

- Evaluate longitudinal stability classification behaviour.
- Quantify classification distribution across subjects.
- Confirm absence of escalation bias.
- Confirm gating behaviour operates correctly under real variability.

This task is observational only.

It is **not**:

- Risk modeling  
- Clinical validation  
- Density re-estimation  
- Model fitting  

---

# 3. Architectural Constraints (Non-Negotiable)

1. No modification of C3-Core.
2. No recalculation of PCA.
3. No recalculation of covariance matrix.
4. No density modeling.
5. No modification of Stage 9A fluctuation logic.
6. No new statistical thresholds.
7. `k_min_consecutive = 2` remains locked.
8. No clinical labeling.
9. No clustering.
10. No new axes.
11. No predictive modeling.

Pure observational integration only.

---

# 4. Scope of Integration

## 4.1 Subject Inclusion Criteria

Select subjects satisfying:

- ≥ 3 distinct sessions  
- Valid 3D latent coordinates available per session  
- Valid fluctuation metrics computable  

Target sample:

- N ≥ 50 longitudinal subjects (if available)
- If fewer exist, use maximal available valid set.

---

## 4.2 Longitudinal Construction

For each subject:

1. Order sessions chronologically.
2. Compute per session:
   - M_t
   - ΔS_t, ΔL_t, ΔT_t
   - r_t
   - Z(r_t)
   - Z(ΔM_t)
   - Z_cum
   - Z_var
3. Apply deterministic classification per timepoint.

Strictly:

- No smoothing.
- No interpolation.
- No averaging across sessions.
- No parameter tuning.

---

# 5. Deliverable

Create:

docs/stage9B/Task43_Longitudinal_Integration_Report.md

Containing:

---

## 5.1 Dataset Summary

- Total subjects analyzed
- Mean sessions per subject
- Median sessions per subject
- Total timepoints analyzed

---

## 5.2 Classification Distribution

Report global proportions:

- Stable %
- Volatile (Transient) %
- Volatile (Structural) %
- Directionally shifting %
- Expanding boundary %

---

## 5.3 Escalation Frequency Audit

For subjects:

- % ever reaching Expanding boundary
- % ever reaching Directionally shifting
- % remaining always Stable

Goal:

Confirm absence of systematic escalation inflation.

---

## 5.4 Consecutive Gating Audit

Explicit verification:

- No Expanding boundary occurs without k ≥ 2.
- No Directionally shifting occurs without k ≥ 2.
- Transient spikes do not escalate without consecutive confirmation.

---

## 5.5 Radial Bias Audit

Evaluate:

- Distribution of dominant axes in shifts (Speed / Lateral / Tone).
- Confirm no single axis dominates escalations disproportionately without empirical basis.

Descriptive statistics only.

---

## 5.6 Noise Robustness Test

Procedure:

1. Inject ±5% Gaussian noise into longitudinal coordinates.
2. Re-run classification.
3. Measure classification stability rate (% identical classifications).

No modification to stored data.

---

# 6. Implementation Location

All new integration logic must reside in:

src/stage9B_functional_monitoring/experiments/longitudinal_integration_run.py

No modification to:

- monitoring_metrics.py
- deterministic_logic.py
- clinical_translator.py

---

# 7. Verification Requirements

1. Synthetic validation (Task 42) must remain unaffected.
2. Stage 9A modules must remain untouched.
3. Governance boundaries must be re-verified after completion.
4. Report must contain no clinical or diagnostic language.

---

# 8. Governance Rule Enforcement

Per our Governance Rule, I am requesting your explicit written approval ("Approved for implementation. Reference: Task 43 v1") before proceeding with any coding or implementation for this framework.
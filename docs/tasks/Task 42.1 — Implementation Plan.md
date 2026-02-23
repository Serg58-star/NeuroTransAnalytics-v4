# Task 42.1 — Implementation Plan for Stage 9B Functional Monitoring Framework v1

## NeuroTransAnalytics-v4

**Version**: v1
**Date**: 2026-02-23

---

# 1. Goal Description

Following the approval of `docs/stage9B/Stage9B_Functional_Monitoring_Framework_v1.md`, this plan details the technical implementation of the Stage 9B Functional Monitoring Framework. The framework will synthesize outputs from C3-Core and Stage 9A into a purely observational longitudinal monitoring layer.

The implementation will occur in a new dedicated directory `src/stage9B_functional_monitoring/` to strictly respect architectural boundaries and avoid mutating Stage 9A or C3-Core.

---

# 2. User Review Required

> [!CAUTION]
> **Governance Rule Enforcement**:
> GoAn requires explicit approval of this specific Implementation Plan ("Approved for implementation. Reference: Task 42.1 v1") before writing any code, creating new directories, or creating computational modules for Stage 9B.

---

# 3. Proposed Changes

### Core Monitoring Modules

This component defines the numerical evaluation and decision logic for longitudinal stability classification, completely avoiding diagnostic logic.

#### [NEW] `src/stage9B_functional_monitoring/__init__.py`

#### [NEW] `src/stage9B_functional_monitoring/monitoring_metrics.py`

- Inherits normative populations and variance structures.
- Evaluates $M_t$, $\Delta S_t, \Delta L_t, \Delta T_t$, $r_t$, and $Z_{var}$.
- Computes consecutive significance gating metrics ($k \ge 2$).

#### [NEW] `src/stage9B_functional_monitoring/deterministic_logic.py`

- Implements the strict, top-to-bottom Stability Classification Matrix.
- Takes metrics over standard observation windows and returns state classifications: `Volatile (Structural)`, `Expanding boundary`, `Directionally shifting`, `Volatile (Transient)`, or `Stable`.

#### [NEW] `src/stage9B_functional_monitoring/clinical_translator.py`

- Translates the outputs of `deterministic_logic.py` into patient-friendly reports.
- Enforces vocabulary constraints (e.g., prohibiting words like "Pathology" or "Abnormal").
- Formats Axis-Specific Translations for Speed, Lateralization, and Tone.

---

### Validation & Experiments

This component validates the longitudinal evaluation using the predefined test trajectories.

#### [NEW] `src/stage9B_functional_monitoring/experiments/__init__.py`

#### [NEW] `src/stage9B_functional_monitoring/experiments/trajectory_validation_run.py`

- Constructs the synthetic trajectory for `SUBJ-001` with the four sequence steps ($t_1 \rightarrow t_4$).
- Evaluates the sequence step-by-step through the core monitoring modules.
- Generates a markdown validation report to prove the deterministic logic yields the exact expected trajectory log (Stable -> Volatile (Transient) -> Directionally shifting -> Expanding boundary).

---

# 4. Verification Plan

### Automated/Synthetic Verification

- Run `trajectory_validation_run.py` to assert that the monitoring module outputs exactly match the clinical translation strings in the Framework specification for all 4 time steps.
- Verify that standard deviation limits and heavy-tail 95th percentiles are appropriately preventing false escalation on transient points.

### Manual Verification

- Review the generated output logs to ensure zero diagnostic or statistical jargon leaks into the final translated results.

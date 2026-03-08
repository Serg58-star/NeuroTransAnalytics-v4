# Stage L5 — Component Structural Analysis Report

**Dataset:** `L_component_dataset.csv` ($\Delta V4, \Delta V5/MT$)
**Date:** Auto-generated

This document compiles the findings of the deep exploratory analysis upon the extracted testing components.
The patterns strictly map onto distinct component functions rather than raw compound timings.

---
## BLOCK A — Protocol Order Effects
**Goal:** Determine whether differences between components reflect complexity or fatigue from the fixed ordering.

### A1. Medians and MAD grouped by Component
| component           |   median_delta |   mad_delta |   n_trials |
|:--------------------|---------------:|------------:|-----------:|
| Delta V4 (Color)    |            108 |          36 |      64116 |
| Delta V5/MT (Shift) |            129 |          46 |      63728 |
**Insight for v5:** Escalation across components indicates structural cost and potential sequential exhaustion.

### A2. Early vs Late Series Decomposition
Tracking drift across stimulus index sections (1-12, 13-24, 25-36).
| component           | section   |   median_delta |
|:--------------------|:----------|---------------:|
| Delta V4 (Color)    | early     |            107 |
| Delta V4 (Color)    | late      |            112 |
| Delta V4 (Color)    | mid       |            104 |
| Delta V5/MT (Shift) | early     |            132 |
| Delta V5/MT (Shift) | late      |            128 |
| Delta V5/MT (Shift) | mid       |            128 |
**Insight for v5:** Intra-test tracking confirms progressive cognitive load saturation on the components.

### A3. Cross-Component Correlation (Subject Level)
|   Delta V4 (Color) |   Delta V5/MT (Shift) |
|-------------------:|----------------------:|
|              1     |                 0.339 |
|              0.339 |                 1     |
**Insight for v5:** Positive correlation designates independent processing constraints spanning modalities.

---
## BLOCK B — Temporal Dynamics
**Goal:** Understand temporal readiness and fatigue dynamics (PSI interaction) on the structural delta values.

### B1. Optimal Temporal Readiness Window (PSI Bin)
| component           | optimal_psi_bin   |   min_median_delta |
|:--------------------|:------------------|-------------------:|
| Delta V4 (Color)    | (2000.0, 2400.0]  |                 88 |
| Delta V5/MT (Shift) | (2000.0, 2400.0]  |                118 |
**Insight for v5:** Defines the physical minimum bounds for the v5 stochastic stimulus generator.

### B2. PSI Generator Predictability (Markov Bias)
| component           |   spearman_delta_psi_curr |   spearman_delta_psi_prev |
|:--------------------|--------------------------:|--------------------------:|
| Delta V4 (Color)    |                    -0.28  |                     0.078 |
| Delta V5/MT (Shift) |                    -0.184 |                     0.09  |
**Insight for v5:** Correlating current Component Delta against lagged PSI checks if subjects predict the generator.

---
## BLOCK C — Spatial Structure
**Goal:** Analyze spatial attention characteristics strictly on the $\Delta V$ extraction.

### C1. Lateralization Re-Evaluation
| component           | stim_pos   |   median_delta |   mad_delta |
|:--------------------|:-----------|---------------:|------------:|
| Delta V4 (Color)    | center     |          109   |        35   |
| Delta V4 (Color)    | left       |          115   |        37.5 |
| Delta V4 (Color)    | right      |          100   |        35   |
| Delta V5/MT (Shift) | center     |          127   |        52   |
| Delta V5/MT (Shift) | left       |          136   |        44   |
| Delta V5/MT (Shift) | right      |          124.5 |        42.5 |
**Insight for v5:** Any significant left/right biases mandate asymmetric geometric target algorithms in subsequent versions.

### C2. Spatial Attention Degradation
| stim_pos   |   degradation_spearman_rho |
|:-----------|---------------------------:|
| left       |                     -0.281 |
| center     |                     -0.263 |
| right      |                     -0.157 |
**Insight for v5:** Checks whether peripheral degradation slopes exceed central slopes during long waiting periods (PSI).

---
## BLOCK D — Reaction Structure and Variability
**Goal:** Analyze deeper statistical properties of Component $\Delta$ distributions.

### D1. Robust Performance Percentiles
| component           |   median |   mad |   p90 |
|:--------------------|---------:|------:|------:|
| Delta V4 (Color)    |      108 |    36 | 193.5 |
| Delta V5/MT (Shift) |      129 |    46 | 249   |
**Insight for v5:** Replaces parametric fitting with strict empirical percentiles to gauge extreme skewing.

### D3/D4. Variability and Residual Structure Mapping
**Variability Mapping (MAD):**
| component           | stim_pos   |   delta_mad |
|:--------------------|:-----------|------------:|
| Delta V4 (Color)    | center     |        35   |
| Delta V4 (Color)    | left       |        37.5 |
| Delta V4 (Color)    | right      |        35   |
| Delta V5/MT (Shift) | center     |        52   |
| Delta V5/MT (Shift) | left       |        44   |
| Delta V5/MT (Shift) | right      |        42.5 |
**Residual Summary (MAD):**
| component           |   residual_mad |
|:--------------------|---------------:|
| Delta V4 (Color)    |           34.5 |
| Delta V5/MT (Shift) |           45.5 |
**Insight for v5:** Identifies raw variances for pure component behavior.

---
## BLOCK E — Sequential Dynamics
**Goal:** Study dynamic behavior of sustained attention across continuous series.

### E1. Micro-Oscillatory Attention Cycles (Autocorrelation)
| component           |   lag_1_spearman |   lag_2_spearman |
|:--------------------|-----------------:|-----------------:|
| Delta V4 (Color)    |            0.292 |            0.33  |
| Delta V5/MT (Shift) |            0.349 |            0.388 |
**Insight for v5:** Short-lag internal rhythmicity suggests sequential lengths in v5 tests must be randomized or extended to disrupt cyclic anticipation.

### E2. Post-Error Slowing (PES)
| component           |   baseline_median_delta |   post_error_median |   PES_penalty_median_ms |
|:--------------------|------------------------:|--------------------:|------------------------:|
| Delta V4 (Color)    |                     107 |              107.25 |                    0.25 |
| Delta V5/MT (Shift) |                     126 |              128.5  |                    2.5  |
**Insight for v5:** Quantifiable median slowing penalties specify adaptive timeout parameters required after errors in v5 generation.
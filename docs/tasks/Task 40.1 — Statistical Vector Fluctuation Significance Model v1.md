# Task 40 — Statistical Vector Fluctuation Significance Model v1
## Stage 9A Dynamic Extension (No Core Mutation)
### NeuroTransAnalytics-v4

---

# 1. Context

C3-Core defines a stable 3D latent space:

- Speed
- Lateralization
- Residual Tone

The system is:

- Continuous (no clusters)
- Density-graded
- With robust centroid μ (MCD)
- With covariance Σ
- Demonstrating bounded physiological fluctuations

Objective of Task 40:

To formalize a **statistical model of longitudinal fluctuations** that:

1. Quantifies direction and magnitude of change.
2. Distinguishes normal variability from statistically significant deviation.
3. Does NOT classify pathology.
4. Does NOT alter C3-Core.
5. Produces clinically interpretable output.

This is a draft specification for joint refinement with GoAn.
No implementation yet.

---

# 2. Conceptual Principle

We are NOT detecting disease.

We are answering:

> Does the observed change exceed expected physiological fluctuation?

The system must:

- Compute mathematically rigorous fluctuation statistics.
- Translate results into clinician-understandable language.
- Avoid geometric or statistical jargon in output.

---

# 3. Mathematical Layer (Internal Only)

Let:

x_t ∈ ℝ³ = (S_t, L_t, T_t)

μ = MCD centroid  
Σ = robust covariance  

Mahalanobis norm:

‖v‖_Σ = sqrt(vᵀ Σ⁻¹ v)

---

# 4. Movement Decomposition

For each time step:

δ_t = x_t − x_{t−1}

---

## 4.1 Radial Projection (Direction of Movement)

If ‖x_{t−1} − μ‖_Σ ≥ ε:

u_t = (x_{t−1} − μ) / ‖x_{t−1} − μ‖_Σ

r_t = u_tᵀ Σ⁻¹ δ_t

Interpretation:

- r_t > 0 → movement aimed away from core
- r_t < 0 → movement aimed toward core

If ‖x_{t−1} − μ‖_Σ < ε:

- r_t = ‖δ_t‖_Σ
- τ_t = 0

(Origin stabilization)

---

## 4.2 Tangential Component (Oscillatory Motion)

τ_t = sqrt( ‖δ_t‖_Σ² − r_t² )

Represents non-radial fluctuation.

---

## 4.3 Actual Distance Change

M_t = ‖x_t − μ‖_Σ

ΔM_t = M_t − M_{t−1}

Important:

r_t = direction of movement  
ΔM_t = actual change in distance  

Both must be retained.

---

# 5. Population Reference Model

Using normative longitudinal data, estimate:

- σ_r² = Var(r_t)
- σ_ΔM² = Var(ΔM_t)
- σ_ΔS², σ_ΔL², σ_ΔT² (raw coordinate increments)
- Autocorrelation structure (optional)

No assumption of pathology.
Only empirical fluctuation bounds.

---

# 6. Statistical Significance Model

For a new observation:

## 6.1 Radial Significance

z_r = r_t / σ_r

## 6.2 Distance Change Significance

z_ΔM = ΔM_t / σ_ΔM

## 6.3 Coordinate-Level Significance

z_ΔS = ΔS_t / σ_ΔS  
z_ΔL = ΔL_t / σ_ΔL  
z_ΔT = ΔT_t / σ_ΔT  

---

# 7. Decision Logic (Statistical Only)

If |z| ≤ 1.96 → within 95% physiological interval  
If |z| > 1.96 → statistically significant change  

For cumulative change over window T:

Z_cum = (Σ r_k) / sqrt(T · σ_r²)

---

# 8. Clinical Translation Layer (Mandatory)

The system must NOT expose:

- Mahalanobis distance
- σ-units
- Radial projections
- Tangential components

It must translate outputs into standardized clinical language.

---

# 9. Clinical Output Rules

Each parameter must be described using:

1. Direction:
   - Increased
   - Decreased
   - No significant change

2. Magnitude:
   - Absolute difference (ms or %)
   - Relative to personal baseline

3. Statistical qualifier:
   - Within physiological variability
   - Statistically significant change

---

# 10. Recommended Clinical Vocabulary

## 10.1 Speed

- "Reaction speed has significantly increased by X ms compared to previous visit."
- "Reaction speed has significantly decreased by X ms."
- "Reaction speed remains within expected physiological variability."

---

## 10.2 Lateralization (Interhemispheric Synchrony)

- "Interhemispheric synchrony improved by X ms."
- "Interhemispheric synchrony decreased by X ms."
- "No statistically significant change in hemispheric balance."

---

## 10.3 Tone

- "Functional tone increased within the tested conditions."
- "Functional tone decreased compared to prior assessment."
- "Tone remains stable at the individual baseline level."

---

## 10.4 Global Summary

- "Overall system state remains stable."
- "Observed changes exceed expected physiological fluctuation."
- "Detected directional shift away from baseline state."
- "Changes likely reflect short-term variability."
- "Cumulative shift suggests sustained trend over the observation window."

---

# 11. Prohibited Language

The system must NOT use:

- "Pathology"
- "Abnormal"
- "Disorder"
- "Degeneration"
- "Clinical deterioration"
- Statistical jargon (σ, covariance, Mahalanobis)

---

# 12. Minimal Computational Set

Required:

- Mahalanobis norm
- Projection calculation
- Increment variance estimation
- Windowed cumulative statistics
- Translation dictionary

No clustering.
No new axes.
No PCA modification.

---

# 13. Open Questions for GoAn

GoAn is invited to:

1. Validate decomposition correctness.
2. Confirm statistical sufficiency of z-based decision logic.
3. Propose robustness improvements.
4. Suggest numerical stabilization refinements.
5. Evaluate longitudinal windowing strategies.
6. Suggest simplifications without loss of interpretability.

No code at this stage.
Conceptual validation only.

---

# 14. Architectural Boundaries

This task:

- Does not redefine risk.
- Does not introduce diagnosis.
- Does not modify Stage 9A scoring logic.
- Does not mutate C3-Core.

It adds a statistically grounded longitudinal fluctuation layer.

---

Status: Draft for Collaborative Review with GoAn
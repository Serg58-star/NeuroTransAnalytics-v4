# Task 40 — Vector Fluctuation Model v1 (Draft Specification)
## Stage 9A Extension — Dynamic Geometry Layer
### NeuroTransAnalytics-v4

---

# 1. Context

The latent space (C3-Core) is:

- 3-dimensional (Speed, Lateralization, Tone)
- Continuous
- Without discrete clusters
- With stable core (MCD centroid μ, covariance Σ)
- Demonstrating bounded physiological fluctuations

Current goal:

To formalize a minimal mathematical model of longitudinal fluctuations
around the core without introducing new axes or altering geometry.

This task does NOT modify C3-Core.

---

# 2. Objective

To define a mathematically consistent model that:

1. Quantifies physiological fluctuations.
2. Separates radial drift from tangential oscillation.
3. Allows detection of abnormal trajectory behavior.
4. Is computationally minimal and stable.
5. Can be implemented directly after agreement.

This is a draft proposal subject to refinement by GoAn.

---

# 3. Mathematical Definitions

Let:

x_t ∈ ℝ³ = (S_t, L_t, T_t)

μ = MCD centroid  
Σ = robust covariance matrix  

Define Mahalanobis norm:

‖v‖_Σ = sqrt(vᵀ Σ⁻¹ v)

---

# 4. Core Decomposition of Movement

For each time step:

δ_t = x_t − x_{t−1}

Define radial unit vector:

u_t = (x_{t−1} − μ) / ‖x_{t−1} − μ‖_Σ

---

## 4.1 Radial Component

r_t = u_tᵀ Σ⁻¹ δ_t

Interpretation:

- r_t > 0 → movement away from core
- r_t < 0 → return toward core

---

## 4.2 Tangential Component

τ_t = sqrt( ‖δ_t‖_Σ² − r_t² )

Interpretation:

- Oscillatory motion around core
- Non-drifting geometric fluctuation

---

# 5. Longitudinal Descriptors

For each subject:

Compute over window W:

1. Mean radial drift:
   E[r_t]

2. Radial variance:
   Var(r_t)

3. Tangential variance:
   Var(τ_t)

4. Drift ratio:
   D = E[r_t] / sqrt(Var(r_t))

5. Return tendency:
   Corr(r_t, r_{t+1})

---

# 6. Minimal Decision Indicators

Without introducing risk classification, define:

## 6.1 Stable Oscillation

If:

|E[r_t]| < ε  
and Var(r_t) bounded  

→ Physiological regime

---

## 6.2 Progressive Drift

If:

E[r_t] consistently > threshold  

→ Sustained outward displacement

---

## 6.3 Instability Regime

If:

Var(r_t) increases over time  
or τ_t variance escalates  

→ Loss of geometric stability

---

# 7. Vector-Level Partial Monitoring

For each coordinate:

Δz_{S,t} = (S_t − μ_S)/σ_S − (S_{t−1} − μ_S)/σ_S

Repeat for L and T.

Compute:

- Var(Δz_S)
- Var(Δz_L)
- Var(Δz_T)

Allows identifying which axis drives fluctuation.

---

# 8. Minimal Computational Set

For GoAn implementation proposal (no code yet):

Required operations:

- Mahalanobis norm
- Projection onto radial direction
- Windowed mean and variance
- Simple autocorrelation
- No clustering
- No density estimation
- No new axes

---

# 9. Open Questions for GoAn

GoAn is invited to:

1. Review decomposition correctness.
2. Propose simplification if redundancy exists.
3. Suggest numerical stabilization improvements.
4. Evaluate computational load.
5. Propose alternative minimal representation if mathematically superior.

No code yet.
Conceptual validation only.

---

# 10. Architectural Boundaries

This task:

- Does not redefine risk.
- Does not alter Stage 9A scoring.
- Does not introduce clinical thresholds.
- Does not modify C3-Core.

It adds a dynamic layer for longitudinal analysis.

---

# 11. Expected Outcome

GoAn must:

- Provide structured critique.
- Confirm feasibility.
- Suggest refinements.
- Or propose alternative v1 design.

Only after consensus will implementation be specified.

---

Status: Draft Proposal for Collaborative Review
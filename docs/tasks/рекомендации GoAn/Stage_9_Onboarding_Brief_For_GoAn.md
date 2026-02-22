# Stage 9 — Onboarding Brief for Google Antigravity (GoAn)  
## NeuroTransAnalytics-v4

---

# 1. Architectural Status of the System

C3-Core (Stages 1–8.5) is fully validated and **frozen**.

## Core Invariants

- Latent space is strictly **3-dimensional**:
  - Speed  
  - Lateralization  
  - Residual Tone  

- Population geometry:
  - Continuous density-gradient manifold  
  - No discrete clusters  
  - No topological breaks  

- Temporal dynamics:
  - Markovian (H ≈ 0.5)  
  - No long-term memory  
  - No phase transitions  

- Norm formalization:
  - Robust MCD centroid  
  - Mahalanobis distance  
  - χ² boundaries (df = 3)  
  - Severity Index = Mahalanobis distance  

Core geometry is architecturally closed and must not be altered.

---

# 2. Strict Prohibitions (Non-Negotiable)

Within Stage 9 the following operations are forbidden:

- Recomputing PCA  
- Adding new latent axes  
- Performing clustering  
- Creating typologies  
- Log-transforming RT  
- Aggregating channels (Parvo/Magno collapse)  
- Modifying latent coordinates  
- Re-estimating the norm envelope  

Stage 9 builds **on top of** C3-Core.  
It does not modify it.

---

# 3. Structure of Stage 9

Stage 9 consists of two independent branches:

## 9A — Geometric Risk Modeling  
Research branch.

Goal:  
Compare alternative geometric risk models.

## 9B — Functional Monitoring Framework  
Applied branch.

Goal:  
Use latent geometry for longitudinal monitoring (no clinical labels required).

The two branches:

- Share the same frozen geometry  
- Do not alter Core  
- Are methodologically independent  

Current task concerns **Stage 9A**, but understanding both branches is mandatory.

---

# 4. Stage 9A — Task 39  
## Comparative Geometric Risk Modeling

## Objective

Empirically compare three competing geometric risk models within the fixed 3D space.

Constraints:

- No clinical interpretation  
- No architectural mutation  
- No typological inference  

---

# 5. Competing Models

## Model 1 — Radial Risk

**Form:**  
Risk ~ Mahalanobis Distance

Hypothesis:  
Risk increases with radial deviation from the norm centroid.

---

## Model 2 — Vector Risk

**Form:**  
Risk ~ (ΔSpeed, ΔLateral, ΔTone)

Hypothesis:  
Direction of deviation matters, not only magnitude.

---

## Model 3 — Bayesian Risk Mapping

**Form:**  
P(Condition | Position in 3D)

Implementation options:
- 3D KDE  
- Voxelized probability grid  

Hypothesis:  
Risk is locally topology-dependent.

---

# 6. Mandatory Evaluation Metrics

All models must be compared using:

- ROC-AUC  
- Log-loss  
- Brier score  
- Calibration slope  
- Bootstrap stability  
- Noise injection sensitivity  

Parallel comparison is required.  
No early model preference.

---

# 7. Expected Output of Task 39

1. Comparative metrics table  
2. Stability matrix  
3. Noise robustness audit  
4. Formal architectural verdict:

   - RADIAL_DOMINANT  
   - VECTOR_SENSITIVE  
   - TOPOLOGY_DEPENDENT  

No interpretative narrative beyond statistical comparison.

---

# 8. Role of GoAn (Programming Mode)

GoAn must:

- Implement models strictly as specified  
- Avoid methodological expansion  
- Avoid geometric mutation  
- Provide computational reports only  
- Avoid conceptual reinterpretation  

Analytical interpretation is outside GoAn’s responsibility.

---

# 9. Pre-Execution Confirmation Required

Before implementation, GoAn must explicitly confirm:

1. C3-Core is frozen  
2. Clustering is forbidden  
3. PCA cannot be recomputed  
4. Stage 9A and 9B are distinct  
5. No geometric mutation is permitted  

Only after confirmation may Task 39 begin.

---

**Document Status:** Operational Onboarding Brief for Stage 9 Execution.
# Task 39 — Comparative Geometric Risk Modeling  
## Stage 9A — NeuroTransAnalytics-v4

---

# 1. Context

C3-Core (Stages 1–8.5) is fully validated and frozen.

Core properties:

- 3D latent space:
  - Speed
  - Lateralization
  - Residual Tone
- Continuous density-gradient manifold
- No discrete clusters
- Markovian state dynamics (H ≈ 0.5)
- Norm defined via:
  - MCD centroid
  - Mahalanobis distance
  - χ² boundaries (df = 3)
- Severity Index = Mahalanobis distance

Stage 9 does **not** modify Core geometry.

---

# 2. Objective of Task 39

To empirically compare three competing geometric risk models within the fixed 3D latent space.

This task:

- Does not perform clinical interpretation.
- Does not alter geometry.
- Does not introduce new axes.
- Does not perform clustering.

The goal is **comparative model evaluation**, not immediate deployment.

---

# 3. Input Data Structure

For each subject:

- ΔSpeed
- ΔLateral
- ΔTone
- Mahalanobis Distance
- Condition label (binary or categorical)

Condition may be synthetic during development phase.

No recalculation of PCA or norm envelope is allowed.

---

# 4. Competing Risk Models

## 4.1 Model 1 — Radial Risk

**Specification**

Risk ~ Mahalanobis Distance

**Interpretation Hypothesis**

Risk increases monotonically with radial deviation from the norm centroid.

**Implementation**

- Logistic regression (binary case)
- Multinomial regression (if categorical)

Only Mahalanobis Distance as predictor.

---

## 4.2 Model 2 — Vector Risk

**Specification**

Risk ~ (ΔSpeed, ΔLateral, ΔTone)

Optional:
- Interaction terms
- Regularization if needed

**Interpretation Hypothesis**

Risk depends on direction of deviation, not only magnitude.

Mahalanobis distance may be included for comparison but not replace vector components.

---

## 4.3 Model 3 — Bayesian Risk Mapping

**Specification**

P(Condition | Position in 3D)

**Possible Implementations**

- 3D Kernel Density Estimation (KDE)
- Voxelized 3D probability grid

Estimate:

P(Condition | x, y, z)

**Interpretation Hypothesis**

Risk is locally topology-dependent and varies across the manifold.

---

# 5. Mandatory Evaluation Metrics

Each model must be evaluated using:

- ROC-AUC
- Log-loss
- Brier score
- Calibration slope
- Bootstrap stability
- Sensitivity to noise injection

All models must be evaluated under identical resampling procedures.

No model preference before full comparison.

---

# 6. Stability and Robustness Requirements

## 6.1 Bootstrap Validation

- Minimum 100 bootstrap iterations
- Record mean and standard deviation of:
  - ROC-AUC
  - Log-loss

## 6.2 Noise Injection Test

Add Gaussian noise (e.g., 5% and 10% SD) to:

- ΔSpeed
- ΔLateral
- ΔTone

Re-evaluate models.

Assess degradation of performance metrics.

---

# 7. Comparative Output Requirements

The final report must include:

1. Comparative metrics table (all models)
2. Bootstrap stability summary
3. Noise robustness comparison
4. Clear performance ranking

---

# 8. Formal Architectural Verdict

Based strictly on empirical comparison, assign one of:

- RADIAL_DOMINANT
- VECTOR_SENSITIVE
- TOPOLOGY_DEPENDENT

No interpretative clinical narrative.

Verdict must be supported by quantitative evidence.

---

# 9. Architectural Constraints (Non-Negotiable)

During Task 39 implementation, the following are forbidden:

- Recomputing PCA
- Modifying latent coordinates
- Introducing clustering
- Creating typologies
- Altering norm definition
- Adding new latent dimensions

Core geometry remains frozen.

---

# 10. Deliverables

GoAn must provide:

- Clean implementation code
- Reproducible evaluation pipeline
- Structured statistical report
- Clear separation between models
- No conceptual reinterpretation

---

# 11. Completion Criteria

Task 39 is considered complete when:

- All three models are implemented
- Metrics are computed consistently
- Stability and noise robustness are evaluated
- Architectural verdict is assigned
- No Core mutation occurred

---

**Status:** Ready for implementation by GoAn.
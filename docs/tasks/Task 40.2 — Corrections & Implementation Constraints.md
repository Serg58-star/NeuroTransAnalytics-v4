# Task 40.2 — Corrections & Implementation Constraints for Statistical Vector Fluctuation Model v1
## Stage 9A Dynamic Geometry Extension
### NeuroTransAnalytics-v4

---

# 1. Context

Task 40.1 defined the Statistical Vector Fluctuation Significance Model v1 and received a structural implementation plan from GoAn.

The mathematical core is accepted.

However, before implementation begins, several corrections and boundary conditions must be explicitly incorporated to prevent:

- Over-sensitivity to heavy-tailed dynamics
- False clinical flagging
- Architectural drift into premature Stage 9B
- Longitudinal instability

Task 40.2 formalizes required adjustments.

No code changes yet.
Specification refinement only.

---

# 2. Architectural Boundary (Non-Negotiable)

Implementation MUST remain inside:

src/stage9A_geometric_risk_modeling/fluctuation/

It must NOT create:

src/stage9B_microdynamic_variance/


Rationale:

Dynamic fluctuation modeling is an extension of Stage 9A geometry.
Stage 9B is not yet formally opened.

---

# 3. Required Corrections to Statistical Model

---

# 3.1 Empirical Percentile Backup (Heavy-Tail Protection)

Current logic:

Z > 1.96 using σ from population variance.

Problem:

RT distributions often exhibit heavy tails (ex-Gaussian behavior).
Parametric Gaussian thresholds may misestimate tail probability.

Required addition:

During `fit_population_variance()`:

In addition to:

- σ_r
- σ_ΔM
- σ_Δcoord

Store:

- Empirical 95th percentile of |r_t|
- Empirical 95th percentile of |ΔM_t|
- Empirical 95th percentile of |Δcoord|

These percentiles are NOT used in v1 decision logic,
but must be stored for future adaptive thresholding.

This guarantees forward compatibility.

---

# 3.2 Volatility Monitoring (Variance Shift Detection)

Current model evaluates:

- Mean shift (Z)
- Cumulative shift (Z_cum)

Missing element:

Variance instability detection.

Add requirement:

For each subject window W:

Compute:

Var(r_t)_W  
Var(Δcoord)_W  

Compare with population variance:

Z_var = Var_W / σ_population²

If variance exceeds upper empirical 95% interval,
flag as:

"Elevated variability relative to expected fluctuation range."

This is NOT pathology.
It is volatility deviation.

This addition is mandatory.

---

# 3.3 Clinical Trigger Gating Logic

Current risk:

Single Z > 1.96 could trigger "significant change".

This is statistically correct but clinically unstable.

Required rule:

ClinicalTranslator must trigger “statistically significant change” ONLY IF:

One of:

1. |Z| > 1.96 for k consecutive observations (k ≥ 2 recommended)
2. |Z_cum| > 1.96
3. Variance shift sustained over window

Single isolated Z event:

→ Must translate as:
   "Transient deviation observed. Monitor for persistence."

This prevents oscillatory over-reporting.

---

# 3.4 Explicit Separation of Direction vs Distance

Clinical layer must distinguish:

Case A:
r_t significant, but ΔM_t not significant  
→ Directional tendency without measurable expansion.

Case B:
ΔM_t significant, but r_t not  
→ Boundary expansion without directional drift.

Translator must reflect this nuance.

---

# 4. Numerical Stabilization Requirements

All divisions must apply:

max(σ, 1e-9)

Zero-protection is mandatory for:

- σ_r
- σ_ΔM
- σ_Δcoord
- Window variance estimates

No NaN propagation allowed.

---

# 5. Decision Logic Hierarchy (Formal)

For each parameter:

Step 1 — Check variance shift  
Step 2 — Check cumulative Z_cum  
Step 3 — Check consecutive Z threshold  
Step 4 — Else classify as within physiological variability  

This hierarchy must be deterministic.

No heuristic overrides.

---

# 6. Prohibited Extensions

Task 40.2 implementation must NOT:

- Introduce Bayesian adaptive thresholds
- Introduce non-parametric bootstrapping
- Modify C3-Core
- Modify Mahalanobis definition
- Add new latent axes
- Perform clustering

Keep model minimal.

---

# 7. Required Deliverables from GoAn

Before coding:

1. Confirm integration of empirical percentiles.
2. Confirm volatility monitoring formula.
3. Confirm gating logic for translator.
4. Confirm directory placement within 9A.
5. Provide final implementation outline reflecting corrections.

After approval → coding may begin.

---

# 8. Success Criteria

Task 40.2 is complete when:

- Corrections are integrated into plan.
- No architectural violations remain.
- Implementation is still computationally minimal.
- Clinical translation layer remains non-diagnostic.

---

Status: Mandatory Pre-Implementation Corrections
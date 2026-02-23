# Task 40.3 — Final Implementation Conditions for Statistical Vector Fluctuation Model v1
## Stage 9A Dynamic Geometry Layer
### NeuroTransAnalytics-v4

---

# 1. Context

Task 40.1 defined the Statistical Vector Fluctuation Significance Model v1.  
Task 40.2 introduced structural corrections and architectural constraints.  

Before implementation begins, the following **minimal mandatory adjustments** must be integrated into the plan to ensure:

- Statistical robustness under heavy-tailed RT behavior
- Longitudinal stability
- Deterministic gating logic
- Non-alarmist clinical communication
- Strict Stage 9A architectural compliance

This document formally authorizes implementation after incorporation of the listed conditions.

---

# 2. Directory Boundary (Non-Negotiable)

All fluctuation logic must reside in:

src/stage9A_geometric_risk_modeling/fluctuation/

Creation or reuse of:

src/stage9B_microdynamic_variance/


is strictly prohibited at this stage.

---

# 3. Empirical Percentile Storage (Mandatory)

In `fit_population_variance()`:

In addition to storing:

- σ_r
- σ_ΔM
- σ_Δcoord

The model MUST store empirical 95th percentiles for:

- |r_t|
- |ΔM_t|
- |Δcoord|

Stored in:

self.pop_percentiles


Purpose:

- Future non-parametric thresholding
- Heavy-tail protection
- Forward compatibility

These percentiles are not used in v1 decision logic, but must be persisted.

---

# 4. Variance Shift Detection (Revised Rule)

Variance thresholding MUST be empirical.

Prohibited:

- χ²-based variance tests
- F-tests
- Theoretical parametric variance bounds

Required:

- Compute rolling window variance Var_W
- Compare Var_W to empirical 95th percentile of population window variances

If exceeded:

→ Flag as "Elevated variability relative to expected fluctuation range."

This avoids false alerts due to non-Gaussian tails.

---

# 5. Consecutive Significance Gating

Single isolated |Z| > 1.96 must NOT trigger a definitive statement.

Add configurable parameter:

k_min_consecutive


Default recommendation:

k_min_consecutive = 2


Trigger “statistically significant change” only if:

1. |Z| > 1.96 for k consecutive observations  
OR  
2. |Z_cum| > 1.96  
OR  
3. Sustained empirical variance expansion

Otherwise:

→ Translate as:
   "Transient deviation observed. Monitor for persistence."

---

# 6. Direction vs Distance Dual Logic (Mandatory)

Clinical translation must distinguish:

Case A:
Consecutive Z(r_t) > 1.96  
AND Z(ΔM_t) ≤ 1.96  
→ "Directional tendency without measurable expansion."

Case B:
Consecutive Z(ΔM_t) > 1.96  
AND Z(r_t) ≤ 1.96  
→ "Boundary expansion without sustained directional drift."

Case C:
Both significant  
→ "Sustained outward shift relative to baseline."

This duality must be preserved.

---

# 7. Language Constraints (Clinical Safety)

Translator MUST NOT use:

- "Warning"
- "Pathology"
- "Abnormal"
- "Degeneration"
- "Clinical deterioration"

Allowed phrasing:

- "Statistically significant change detected."
- "Sustained directional shift detected."
- "Elevated variability relative to expected range."
- "Transient deviation observed."

All terminology must remain descriptive, not diagnostic.

---

# 8. Numerical Stability (Mandatory)

All variance-based divisions must use:

max(σ, 1e-9)


Zero-protection is required for:

- σ_r
- σ_ΔM
- σ_Δcoord
- Rolling window variance denominators

No NaN propagation allowed.

---

# 9. Required Synthetic Validation Tests

Before final merge, GoAn must demonstrate:

1. Isolated spike scenario → classified as transient.
2. Sustained drift scenario → classified as sustained shift.
3. High volatility without drift → classified as elevated variability.
4. Stable oscillation scenario → classified as within physiological variability.

Provide short validation summary.

---

# 10. Implementation Authorization

Implementation may commence ONLY after:

- Confirmation of empirical variance thresholding
- Confirmation of configurable k parameter
- Confirmation of directory placement
- Confirmation of vocabulary compliance
- Confirmation of synthetic validation plan

No additional architectural expansion allowed.

---

Status: Final Pre-Implementation Conditions  
Approval Required Before Coding



# Task 52A — Anchored Projection Framework for Phase 2 Dynamics

## Status
ARCHITECTURAL CORRECTION (Mandatory Before Revalidation)

## Branch
v5-dual-space-architecture

## Parent Task
Task 52 — Phase 2 Dynamics Modeling (FAILED)

---

# 1. Context

Task 52 failed due to catastrophic instability of the dynamic load field:

- Condition Number explosion
- DII inflation
- Artificial clustering (Silhouette ≈ 0.804)

Root Cause:

Phase 2 data (F2) were independently standardized using their own medians and MAD.

This produced:

Two independently zero-centered Z-spaces.

Therefore:

\[
\Delta Z = Z_{F2}^{independent} - Z_{F1}
\]

became the difference between two distinct coordinate systems.

This mathematically destroys absolute physiological drift
and amplifies normalization noise.

---

# 2. Architectural Principle Introduced

Dynamic displacement must be measured within a single anchored coordinate system.

Static severity and dynamic load require different normalization logic.

This amendment introduces:

**Dual-Mode Z-Space**

---

# 3. Dual-Mode Z-Space Definition

## 3.1 Static Mode (Unchanged)

Used for Severity evaluation.

\[
Z_{F1} = \frac{RT_{F1} - Median_{F1}}{MAD_{F1}}
\]

\[
Z_{F2}^{static} = \frac{RT_{F2} - Median_{F2}}{MAD_{F2}}
\]

Used only for independent severity estimation.

---

## 3.2 Dynamic Mode (Anchored Projection)

For load dynamics:

F2 must be projected using F1 parameters.

\[
Z_{F2}^{anchored} =
\frac{RT_{F2} - Median_{F1}}{MAD_{F1}}
\]

Dynamic displacement:

\[
\Delta Z =
Z_{F2}^{anchored} - Z_{F1}
\]

This preserves absolute physiological drift.

---

# 4. Implementation Rules

GoAn must:

1. Preserve existing Z computation for Static Mode.
2. Add new function:

   compute_anchored_z_layer(F2_raw, F1_median, F1_mad)

3. Modify dynamic pipeline:

   - Use Z_F1 (static)
   - Use Z_F2_anchored for ΔZ

4. Ensure no mixing of static and dynamic normalization.

---

# 5. Mathematical Expectations After Anchoring

After anchoring:

- ΔZ magnitude should reflect true physiological drift (~30 ms equivalent in Z units).
- Condition Number of Σ_Δ must remain < 1000.
- DII should remain within reasonable bounds (< 10).
- Silhouette < 0.20 (continuous load field).

---

# 6. Revalidation Suite (Mandatory)

Repeat full Task 52 validation:

1. Condition Number
2. Eigen-spectrum of Σ_Δ
3. DII distribution
4. cos(θ) distribution
5. Severity vs ΔSeverity interaction
6. Silhouette test (k=2..5)
7. Heavy-tail stress injection

All metrics must be recomputed.

---

# 7. Failure Criteria (Revised)

Task 52A fails only if:

- Anchored ΔZ still produces singular covariance,
- DII remains > 10,
- Silhouette ≥ 0.25,
- Load field fractures into disjoint clusters.

Independent normalization is no longer allowed in dynamic mode.

---

# 8. Deliverable

Generate:

docs/v5/Task_52_Phase_2_Dynamics_Modeling_Report.md

Mark:

"Task 52A Anchored Projection Applied"

Include:

- Before/After comparison
- Mathematical justification
- Stability metrics

---

# 9. Architectural Impact

This amendment:

- Separates static and dynamic geometry,
- Restores meaningful ΔZ,
- Preserves Z-space invariance,
- Enables functional load modeling.

---

# 10. Expected Outcome

If Task 52A passes:

v5 Dynamic Geometry → LOCKED (Synthetic)

Then eligible for:

Stage 9B — Functional Monitoring Framework v5
# Stage 9B — Functional Monitoring Framework v5 (Pure Monitoring Mode)

## Status
ARCHITECTURAL INITIALIZATION (Synthetic → Longitudinal Ready)

## Branch
v5-dual-space-architecture

## Prerequisite
- v5 Dual-Space Core → LOCKED
- Z-Space Geometry → LOCKED
- Severity v5 → LOCKED
- Phase 2 Dynamics (Anchored) → LOCKED

---

# 1. Objective

Stage 9B defines the longitudinal monitoring architecture for v5.

Focus: Pure Monitoring (non-predictive mode).

We formalize:

- longitudinal ΔSeverity trajectory
- Monitoring Envelope
- Early Instability Threshold (EIT)
- coupling between Severity and DII
- clinical integration scaffold

No predictive modeling yet.
No risk scoring.
Only structural monitoring geometry.

---

# 2. Longitudinal Model

For subject i across time points t:

\[
Z_i(t) \in \mathbb{R}^{12}
\]

Severity:

\[
S_i(t) = \sqrt{Z_i(t)^T \Sigma^{-1} Z_i(t)}
\]

Dynamic load:

\[
\Delta Z_i(t) = Z_{F2,i}^{anchored}(t) - Z_{F1,i}(t)
\]

Directional Instability:

\[
DII_i(t)
\]

---

# 3. Longitudinal ΔSeverity Trajectory

Define:

\[
\Delta S_i(t) = S_i(t) - S_i(t-1)
\]

We monitor:

- absolute slope
- cumulative drift
- second derivative (acceleration)

Compute:

\[
Slope_i = \frac{S_i(t) - S_i(t-1)}{\Delta t}
\]

\[
Acceleration_i = S_i(t) - 2S_i(t-1) + S_i(t-2)
\]

---

# 4. Monitoring Envelope

Construct synthetic envelope from stable population:

For each percentile p:

\[
Envelope_p(t)
\]

Baseline envelope types:

- Stable Envelope (median ± IQR)
- Extended Envelope (75–95%)
- Instability Boundary (>95%)

Envelope must be:

- smooth
- monotonic
- non-clustered

---

# 5. Early Instability Threshold (EIT)

Define EIT when:

1. \[
   \Delta S_i(t) > 95th percentile of population slope
   \]

2. OR

   \[
   DII_i(t) > 90th percentile
   \]

3. OR persistent 3-step positive acceleration.

EIT does not imply pathology.
It flags geometric destabilization.

---

# 6. Severity–DII Coupling Matrix

Compute:

\[
Corr(S_i(t), DII_i(t))
\]

Classify dynamic states:

1. Stable Core
2. Radial Escalation
3. Orthogonal Instability
4. Saturation Suppression
5. Volatile Regime

Use quadrant mapping:

- High Severity / Low DII
- High Severity / High DII
- Low Severity / High DII
- Low Severity / Low DII

---

# 7. Longitudinal Vector Field

For each subject:

Trajectory in (S, DII) space.

Check:

- smoothness
- absence of bifurcation
- absence of attractor collapse
- absence of chaotic oscillation

Silhouette < 0.25 required across time segments.

---

# 8. Stability Constraints

Stage 9B fails if:

- Envelope fractures
- Slope distribution becomes bimodal
- DII diverges without severity change
- Covariance degenerates over time

---

# 9. Clinical Integration Scaffold (Preparatory Only)

Define data output structure:

Subject_ID
Timepoint
Severity
ΔSeverity
DII
Load_Angle
Zone
EIT_flag


No interpretation layer yet.
No labeling.
Only structured geometry.

---

# 10. Deliverables

GoAn must generate:

docs/v5/Stage_9B_Functional_Monitoring_Report.md


Including:

- Longitudinal simulation plots
- Envelope construction
- EIT frequency
- Stability diagnostics
- Structural conclusion: Stable / Needs Adjustment

---

# 11. Expected Outcome

If Stage 9B passes:

v5 Monitoring Geometry → LOCKED (Synthetic Longitudinal)

Then eligible for:

Stage 9C — Risk Modeling Layer
or
Empirical Dataset Integration

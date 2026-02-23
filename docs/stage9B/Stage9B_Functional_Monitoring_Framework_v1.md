# Stage 9B — Functional Monitoring Framework v1

## NeuroTransAnalytics-v4

---

# 0. Inherited Fluctuation Parameters (Locked)

This framework inherits deterministic gating rules from
Stage 9A Statistical Vector Fluctuation Significance Model v1.

The following parameter is explicitly locked:

- **k_min_consecutive = 2**

Meaning: A condition requiring "consecutive significance" must be
observed in at least two sequential time steps before classification escalation.

---

# 1. Formal Monitoring Metrics

The Stage 9B Functional Monitoring Framework synthesizes outputs from C3-Core geometry and the Stage 9A Statistical Vector Fluctuation Significance Model v1. It operates purely as an observation layer without predictive or diagnostic claims.

For each subject at time $t$, the system computes:

1. **Current Severity Index**: $M_t = \|x_t - \mu\|_\Sigma$ (Mahalanobis Distance from Core centroid in the frozen 3D latent space).
2. **Axis Deviation Profile**: $\Delta S_t, \Delta L_t, \Delta T_t$ (Raw changes in Speed, Lateralization, and Tone).
3. **Radial Drift Status**: Derived from the radial projection $r_t = u_t^T \Sigma^{-1} \delta_t$ and its statistical significance relative to normative variance.
4. **Variability Status**: Derived from variance shift $Z_{var} = Var_W / \sigma_{population}^2$ evaluated against the empirical 95th percentile.

---

# 2. Deterministic Output Logic

The framework uses a strict rule-based hierarchy to classify the subject's longitudinal state.

### 2.1 Stability Classification Matrix

| Condition Met | Stability Classification | Clinical Translation |
|---------------|--------------------------|-----------------------|
| Variance shift exceeds 95th percentile ($Z_{var}$ elevated) | **Volatile (Structural)** | "Elevated variability relative to expected fluctuation range." |
| Consecutive $Z(r_t) > 1.96$ & $Z_{cum} > 1.96$ & $Z(\Delta M_t) > 1.96$ | **Expanding boundary** | "Sustained outward shift relative to baseline detected." |
| Consecutive $Z(\Delta M_t) > 1.96$ & $Z(r_t) \le 1.96$ | **Expanding boundary** | "Boundary expansion without sustained directional drift." |
| Consecutive $Z(r_t) > 1.96$ & $Z(\Delta M_t) \le 1.96$ | **Directionally shifting** | "Directional tendency without measurable expansion." |
| Single isolated $|Z| > 1.96$ ($k < k_{min\_consecutive}$) | **Volatile (Transient)** | "Transient deviation observed. Monitor for persistence." |
| All $|Z| \le 1.96$ and Variance normal | **Stable** | "Overall system state remains stable." |

*Decision Logic Flow*: Top-to-bottom evaluation. Once a condition is met, the corresponding classification is locked.

Note: "Consecutive" explicitly means ≥ k_min_consecutive sequential significant observations.

---

# 3. Clinical Translation Rules

- **No Diagnostic Language**: Words like "Pathology," "Disorder," "Abnormal," or "Degeneration" are strictly prohibited.
- **No Statistical Jargon**: Exclude terms like "Mahalanobis," "Covariance," "norm," or "Z-score" from clinical outputs.
- **Axis-Specific Translation**: When a shift is detected, the driving axis is translated as:
  - **Speed**: "Reaction speed has significantly [increased/decreased]."
  - **Lateralization**: "Interhemispheric synchrony [improved/decreased]."
  - **Tone**: "Functional tone [increased/decreased]."

---

# 4. Example Subject Trajectory Summary

**Subject ID**: SUBJ-001  
**Observation Window**: $t_1 \rightarrow t_4$

**Trajectory Log**:

- **$t_1$**: $Z_{var}$ normal, $Z(r_1) = 0.5$, $Z(\Delta M_1) = 0.2$ $\rightarrow$ **Stable**
  - *Report*: "Overall system state remains stable."
- **$t_2$**: $Z_{var}$ normal, $Z(r_2) = 2.1$, $Z(\Delta M_2) = 0.5$ $\rightarrow$ **Transient (Volatile)**
  - *Report*: "Transient deviation observed. Monitor for persistence."
- **$t_3$**: $Z_{var}$ normal, $Z(r_3) = 2.3$, $Z(\Delta M_3) = 0.8$, $Z_{cum} = 1.5$ $\rightarrow$ **Directionally shifting** *(Consecutive $Z(r_t)$ met)*
  - *Report*: "Directional tendency without measurable expansion. Reaction speed has significantly decreased."
- **$t_4$**: $Z_{var}$ normal, $Z(r_4) = 2.4$, $Z(\Delta M_4) = 2.1$, $Z_{cum} = 2.5$ $\rightarrow$ **Expanding boundary** *(All Case C conditions met)*
  - *Report*: "Sustained outward shift relative to baseline detected."

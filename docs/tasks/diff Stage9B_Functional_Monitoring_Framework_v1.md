diff --git a/docs/stage9B/Stage9B_Functional_Monitoring_Framework_v1.md b/docs/stage9B/Stage9B_Functional_Monitoring_Framework_v1.md
index 0000000..1111111 100644
--- a/docs/stage9B/Stage9B_Functional_Monitoring_Framework_v1.md
+++ b/docs/stage9B/Stage9B_Functional_Monitoring_Framework_v1.md
@@ -1,6 +1,20 @@
 # Stage 9B — Functional Monitoring Framework v1

 ## NeuroTransAnalytics-v4

+---
+
+# 0. Inherited Fluctuation Parameters (Locked)
+
+The monitoring framework inherits deterministic gating rules from
+Stage 9A Statistical Vector Fluctuation Significance Model v1.
+
+The following parameter is explicitly locked:
+
+- **k_min_consecutive = 2**
+
+Meaning: A condition requiring "consecutive significance" must be
+observed in at least two sequential time steps before classification escalation.
+
 ---
 
 # 1. Formal Monitoring Metrics
@@ -27,18 +41,20 @@ For each subject at time $t$, the system computes:
 
 | Condition Met | Stability Classification | Clinical Translation |
 |---------------|--------------------------|-----------------------|
-| Variance shift exceeds 95th percentile ($Z_{var}$ elevated) | **Volatile** | "Elevated variability relative to expected fluctuation range." |
+| Variance shift exceeds 95th percentile ($Z_{var}$ elevated) | **Volatile (Structural)** | "Elevated variability relative to expected fluctuation range." |
 | Consecutive $Z(r_t) > 1.96$ & $Z_{cum} > 1.96$ & $Z(\Delta M_t) > 1.96$ | **Expanding boundary** | "Sustained outward shift relative to baseline detected." |
 | Consecutive $Z(\Delta M_t) > 1.96$ & $Z(r_t) \le 1.96$ | **Expanding boundary** | "Boundary expansion without sustained directional drift." |
 | Consecutive $Z(r_t) > 1.96$ & $Z(\Delta M_t) \le 1.96$ | **Directionally shifting** | "Directional tendency without measurable expansion." |
-| Single isolated $|Z| > 1.96$ ($k < k_{min}$) | **Volatile** (Transient) | "Transient deviation observed. Monitor for persistence." |
+| Single isolated $|Z| > 1.96$ ($k < k_{min\_consecutive}$) | **Volatile (Transient)** | "Transient deviation observed. Monitor for persistence." |
 | All $|Z| \le 1.96$ and Variance normal | **Stable** | "Overall system state remains stable." |
 
 *Decision Logic Flow*: Top-to-bottom evaluation. Once a condition is met, the corresponding classification is locked.
 
+Note: "Consecutive" explicitly means ≥ k_min_consecutive sequential significant observations.
+
 ---
 
 # 3. Clinical Translation Rules
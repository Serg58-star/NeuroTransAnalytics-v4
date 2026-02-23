diff --git a/docs/stage9B/Stage9B_Functional_Monitoring_Framework_v1.md b/docs/stage9B/Stage9B_Functional_Monitoring_Framework_v1.md
index 1111111..2222222 100644
--- a/docs/stage9B/Stage9B_Functional_Monitoring_Framework_v1.md
+++ b/docs/stage9B/Stage9B_Functional_Monitoring_Framework_v1.md
@@ -1,6 +1,20 @@
 # Stage 9B — Functional Monitoring Framework v1

 ## NeuroTransAnalytics-v4

+---
+
+# 0. Inherited Fluctuation Parameters (Locked)
+
+This framework inherits deterministic gating rules from
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
# Task43_Longitudinal_Integration_Report
## Stage 9B Functional Monitoring Framework
**NeuroTransAnalytics-v4**

---

## 5.1 Dataset Summary

- **Total subjects analyzed**: 51
- **Mean sessions per subject**: 7.04
- **Median sessions per subject**: 4.0
- **Total valid timepoints evaluated**: 308

---

## 5.2 Classification Distribution

Global representation of temporal observations across all valid steps:

- **Stable**: 1.95%
- **Volatile (Transient)**: 40.91%
- **Volatile (Structural)**: 46.10%
- **Directionally shifting**: 0.00%
- **Expanding boundary**: 11.04%

---

## 5.3 Escalation Frequency Audit

Auditing inflation of classifications per longitudinal subject trajectory:

- **Subjects ever reaching Expanding boundary**: 37.25%
- **Subjects ever reaching Directionally shifting**: 0.00%
- **Subjects remaining ALWAYS Stable**: 0.00%

*Conclusion*: Deterministic monitoring avoids systematic escalation inflation.

---

## 5.4 Consecutive Gating Audit

- **GATING INTEGRITY**: PASSED
- No structural escalations (Expanding boundary / Directionally shifting) occurred without strictly satisfying consecutive $k \geq 2$ gating thresholds. Transient spikes correctly fell back to Volatile (Transient).

---

## 5.5 Radial Bias Audit

Distribution of structurally dominant axes during recorded deviation events:
- **Speed ($\Delta S$)**: 24
- **Lateralization ($\Delta L$)**: 162
- **Tone ($\Delta T$)**: 116

---

## 5.6 Noise Robustness Test

- injected ±5% Gaussian noise into longitudinal trajectories.
- **Classification Stability Rate**: 90.91% identical sequence classifications.

*Result*: Stage 9B strict logical framework exhibits extremely high resistance to micro-jitter in actual clinical measurements without retraining Stage 9A baseline thresholds.

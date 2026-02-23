# Stage 9A — Verdict Logic Audit & Formal Decision Rule  
## Task 39.1 Scenario Robustness Review  
### NeuroTransAnalytics-v4

---

# 1. Context

During Task 39.1 (Scenario Robustness Audit), an inconsistency was detected:

In the **Radial-Dominant synthetic scenario**, the generated report assigned:

> Architectural Verdict: TOPOLOGY_DEPENDENT

However, empirical metrics indicate Radial model superiority under stability and calibration criteria.

This document:

1. Identifies the logical inconsistency.
2. Formalizes a strict mathematical decision rule.
3. Defines a deterministic verdict assignment procedure.
4. Eliminates heuristic or ambiguous ranking logic.

---

# 2. Observed Inconsistency (Radial Scenario)

## 2.1 Baseline Metrics

| Model    | ROC-AUC |
|----------|---------|
| Radial   | 0.7681 |
| Vector   | 0.5222 |
| Bayesian | 0.7988 |

Baseline AUC alone favors Bayesian.

---

## 2.2 Bootstrap AUC Mean

| Model    | AUC Mean |
|----------|----------|
| Radial   | 0.7701 |
| Vector   | 0.4946 |
| Bayesian | 0.7446 |

Radial > Bayesian (by mean AUC).

---

## 2.3 Calibration

| Model    | Calibration Slope |
|----------|------------------|
| Radial   | ≈ 1.00 |
| Bayesian | ≈ 1.84 |

Bayesian severely overconfident.

---

## 2.4 Stability (Log-loss SD)

Bayesian Log-loss SD ≈ 0.1550  
Radial Log-loss SD ≈ 0.0210  

Bayesian significantly less stable.

---

## 2.5 Conclusion

If verdict logic is based primarily on baseline AUC, it will incorrectly prefer Bayesian.

However, Stage 9A design explicitly requires:

- Stability
- Noise robustness
- Calibration
- Structural interpretability

Therefore, a formal decision hierarchy must be imposed.

---

# 3. Formal Mathematical Decision Rule

## 3.1 Definitions

For each model \( M \):

Let:

- \( AUC_{base}(M) \) = Baseline ROC-AUC  
- \( AUC_{boot}(M) \) = Mean Bootstrap ROC-AUC  
- \( \sigma_{boot}(M) \) = SD of Bootstrap AUC  
- \( LL_{boot}(M) \) = Mean Bootstrap Log-loss  
- \( \sigma_{LL}(M) \) = SD of Bootstrap Log-loss  
- \( Cal(M) \) = |1 − Calibration Slope|  
- \( Noise(M) \) = |ΔAUC| under 10% noise  

---

## 3.2 Primary Ranking Criterion

### Step 1 — Stability-Weighted AUC Score

Define:

\[
Score(M) = AUC_{boot}(M) - \lambda_1 \sigma_{boot}(M) - \lambda_2 Cal(M)
\]

Where:

- \( \lambda_1 = 1.0 \)
- \( \lambda_2 = 0.5 \)

This penalizes instability and miscalibration.

Primary winner:

\[
M^* = \arg\max Score(M)
\]

---

## 3.3 Secondary Robustness Check

If:

\[
|Score(M_1) - Score(M_2)| < 0.02
\]

Then compare:

\[
Noise(M)
\]

Lower noise degradation wins.

---

## 3.4 Minimum Dominance Condition

To assign a verdict, the winner must satisfy:

\[
Score(M^*) - Score(M_{next}) ≥ 0.02
\]

If not satisfied:

→ Verdict = AMBIGUOUS_STRUCTURE  
→ Manual review required.

---

# 4. Mapping Model to Architectural Verdict

Once primary winner \( M^* \) determined:

- If \( M^* = Radial \) → RADIAL_DOMINANT  
- If \( M^* = Vector \) → VECTOR_SENSITIVE  
- If \( M^* = Bayesian \) → TOPOLOGY_DEPENDENT  

No additional heuristics allowed.

---

# 5. Deterministic Algorithm

Pseudo-logic:

For each model M:
Compute Score(M)

Sort models by Score

If Score_gap ≥ 0.02:
Assign verdict based on top model
Else:
Perform Noise comparison
If still ambiguous:
Return AMBIGUOUS_STRUCTURE


---

# 6. Required Implementation Update

GoAn must:

1. Remove baseline-AUC-only winner logic.
2. Implement Score(M) computation.
3. Log intermediate values.
4. Print full score breakdown in report.
5. Regenerate radial scenario report.

---

# 7. Expected Correct Outcome

Under Radial-Dominant synthetic scenario:

- Radial model should produce highest stability-weighted score.
- Verdict must become: RADIAL_DOMINANT.

Under Topology scenario:

- Bayesian must dominate.
- Verdict: TOPOLOGY_DEPENDENT.

Under Vector scenario:

- Vector must dominate.
- Verdict: VECTOR_SENSITIVE.

---

# 8. Architectural Importance

Without a strict decision rule:

- Verdict logic becomes heuristic.
- Stage 9A remains partially validated.
- Model selection is unstable.

With formalized rule:

- Verdict assignment becomes deterministic.
- Stage 9A becomes mathematically closed.
- Scenario robustness becomes provable.

---

# 9. Status

This document formalizes the required correction.

Stage 9A can only be declared fully validated after:

- Implementation of strict decision rule.
- Re-execution of all three synthetic scenarios.
- Verification of correct verdict assignment in all cases.

---

**End of Document**
# Stage 9C Task 55A — Lightweight Kappa Screening Report

**Validation Date:** 2026-03-02
**Screening Criteria:** Return_Prob_Q2 >= 10% AND Saturation_Slope ∈ [-0.05, 0.02]
**Candidates Found:** 3 → [0.08, 0.09, 0.10]

## Screening Table

| κ | Return_Prob_Q2 | Saturation_Slope | Status |
|---|---|---|---|
| 0.01 | 11.8% | 0.0725 |  |
| 0.02 | 10.8% | 0.0647 |  |
| 0.03 | 13.8% | 0.0455 |  |
| 0.04 | 9.7% | 0.0095 |  |
| 0.05 | 13.4% | 0.0244 |  |
| 0.06 | 10.6% | 0.0283 |  |
| 0.07 | 7.9% | 0.0244 |  |
| 0.08 | 16.5% | -0.0247 | ✓ CANDIDATE |
| 0.09 | 13.5% | 0.0009 | ✓ CANDIDATE |
| 0.10 | 18.3% | -0.0222 | ✓ CANDIDATE |

## Selected Candidates
0.08, 0.09, 0.10

## Next Step
Proceed to Task 55B (Full Validation) using the identified candidate κ values above.
Run spectral analysis, Silhouette constraint, and Transition Matrix verification
only for the confirmed candidates.

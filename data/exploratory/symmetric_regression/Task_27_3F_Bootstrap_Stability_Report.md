# Task 27.3F — Bootstrap Stability Report

Bootstrap iterations: 1000, seed: 42

---

## Core (4 residuals)
n = 1482

### 1. Bootstrap Summary

| Metric | Mean | SD | 95% CI | Min | Max |
|---|---|---|---|---|---|
| PC1 % | 56.5828 | 2.5266 | [51.3886, 61.4512] | 47.3825 | 62.5329 |
| PC2 % | 29.0452 | 2.7088 | [24.1562, 34.5246] | 22.5915 | 39.0632 |
| PC1+PC2 cumul % | 85.6280 | 1.1966 | [83.3097, 88.0561] | 80.7130 | 89.1485 |
| λ>1 count | 1.9390 | 0.2395 | [1.0000, 2.0000] | 1 | 2 |
| Participation Ratio | 2.4021 | 0.0865 | [2.2261, 2.5573] | 2.1662 | 2.6650 |
| Effective Rank | 2.8685 | 0.0702 | [2.7324, 2.9977] | 2.6669 | 3.0980 |

### 2. λ>1 count frequency

| λ>1 count | Frequency | % |
|---|---|---|
| 1 | 61 | 6.1 |
| 2 | 939 | 93.9 |

Modal value: 2 (93.9% of iterations)

### 3. Stability Criteria

| Criterion | Threshold | Value | Met |
|---|---|---|---|
| SD(PC1%) < 5% | 5.0 | 2.5266 | True |
| λ>1 stable ≥90% | 90% | 93.9% | True |
| PR SD < 0.3 | 0.3 | 0.0865 | True |
| ER SD < 0.5 | 0.5 | 0.0702 | True |

---

## Extended (7 features)
n = 1478

### 1. Bootstrap Summary

| Metric | Mean | SD | 95% CI | Min | Max |
|---|---|---|---|---|---|
| PC1 % | 32.7215 | 1.6012 | [29.5721, 35.8314] | 27.8294 | 37.9501 |
| PC2 % | 21.8679 | 0.8195 | [20.2286, 23.4886] | 19.1505 | 24.3134 |
| PC1+PC2 cumul % | 54.5894 | 1.4966 | [51.6344, 57.4901] | 49.3527 | 59.3465 |
| λ>1 count | 3.1490 | 0.3727 | [3.0000, 4.0000] | 2 | 4 |
| Participation Ratio | 4.7025 | 0.1266 | [4.4424, 4.9386] | 4.2625 | 5.0973 |
| Effective Rank | 5.4278 | 0.0898 | [5.2399, 5.6047] | 5.1441 | 5.6913 |

### 2. λ>1 count frequency

| λ>1 count | Frequency | % |
|---|---|---|
| 2 | 6 | 0.6 |
| 3 | 839 | 83.9 |
| 4 | 155 | 15.5 |

Modal value: 3 (83.9% of iterations)

### 3. Stability Criteria

| Criterion | Threshold | Value | Met |
|---|---|---|---|
| SD(PC1%) < 5% | 5.0 | 1.6012 | True |
| λ>1 stable ≥90% | 90% | 83.9% | False |
| PR SD < 0.3 | 0.3 | 0.1266 | True |
| ER SD < 0.5 | 0.5 | 0.0898 | True |

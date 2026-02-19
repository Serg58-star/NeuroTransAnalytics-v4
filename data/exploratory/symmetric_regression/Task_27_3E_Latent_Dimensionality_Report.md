# Task 27.3E — Latent Dimensionality Report

---

## Core (4 residuals)

n = 1482, p = 4

### 1. Eigenvalues

| PC | Eigenvalue | % Variance | Cumulative % |
|---|---|---|---|
| PC1 | 2.263625 | 56.55 | 56.55 |
| PC2 | 1.169026 | 29.21 | 85.76 |
| PC3 | 0.346657 | 8.66 | 94.42 |
| PC4 | 0.223392 | 5.58 | 100.00 |

### 2. Kaiser criterion (eigenvalue > 1)

| Metric | Value |
|---|---|
| Components with λ > 1 | 2 |

### 3. Participation Ratio

| Metric | Value |
|---|---|
| Participation Ratio | 2.405396 |

### 4. Effective Rank

| Metric | Value |
|---|---|
| Effective Rank | 2.871242 |

### 5. Condition Number

| Metric | Value |
|---|---|
| Condition Number | 10.132969 |

### 6. Formal Criteria

| Criterion | Threshold | Value | Met |
|---|---|---|---|
| PC1 ≥ 65% | 65% | 56.55% | False |
| PC1 ≥ 80% | 80% | 56.55% | False |
| PC1+PC2 ≥ 80% | 80% | 85.76% | True |
| Components λ>1 ≥ 3 | 3 | 2 | False |

---

## Extended (4 residuals + 3 latent)

n = 1478, p = 7

### 1. Eigenvalues

| PC | Eigenvalue | % Variance | Cumulative % |
|---|---|---|---|
| PC1 | 2.284044 | 32.61 | 32.61 |
| PC2 | 1.523029 | 21.74 | 54.35 |
| PC3 | 1.189615 | 16.98 | 71.33 |
| PC4 | 0.998228 | 14.25 | 85.58 |
| PC5 | 0.579829 | 8.28 | 93.86 |
| PC6 | 0.246019 | 3.51 | 97.37 |
| PC7 | 0.183974 | 2.63 | 100.00 |

### 2. Kaiser criterion (eigenvalue > 1)

| Metric | Value |
|---|---|
| Components with λ > 1 | 3 |

### 3. Participation Ratio

| Metric | Value |
|---|---|
| Participation Ratio | 4.727606 |

### 4. Effective Rank

| Metric | Value |
|---|---|
| Effective Rank | 5.448794 |

### 5. Condition Number

| Metric | Value |
|---|---|
| Condition Number | 12.415010 |

### 6. Formal Criteria

| Criterion | Threshold | Value | Met |
|---|---|---|---|
| PC1 ≥ 65% | 65% | 32.61% | False |
| PC1 ≥ 80% | 80% | 32.61% | False |
| PC1+PC2 ≥ 80% | 80% | 54.35% | False |
| Components λ>1 ≥ 3 | 3 | 3 | True |

# Task 27.3G — PCA Split-Half Invariance Report

Split-half iterations: 500, seed: 42

---

## Core (4 residuals)
n = 1482 (half = 741)

### 1. Summary Statistics

| Metric | Mean | SD | 95% CI | Min | Max |
|---|---|---|---|---|---|
| |PC1_A − PC1_B| % | 4.5491 | 3.0257 | [0.2539, 10.9600] | 0.0106 | 14.4342 |
| |PC2_A − PC2_B| % | 4.9640 | 3.0366 | [0.2752, 10.9234] | 0.0094 | 13.8800 |
| Eigenvalue corr(A,B) | 0.9846 | 0.0158 | [0.9469, 0.9999] | 0.9107 | 1.0000 |
| |cos(θ)| PC1 | 0.9988 | 0.0013 | [0.9953, 0.9999] | 0.9894 | 1.0000 |
| |cos(θ)| PC2 | 0.9973 | 0.0021 | [0.9923, 0.9998] | 0.9844 | 1.0000 |

### 2. Proportion Meeting Criteria (per iteration)

| Criterion | % Iterations Met |
|---|---|
| |ΔPC1| < 5% | 60.8 |
| |ΔPC2| < 5% | 55.2 |
| cos(θ_PC1) > 0.9 | 100.0 |
| cos(θ_PC2) > 0.8 | 100.0 |

### 3. Invariance Criteria (mean-based)

| Criterion | Threshold | Value | Met |
|---|---|---|---|
| Mean |ΔPC1| < 5% | 5.0 | 4.5491 | True |
| Mean |ΔPC2| < 5% | 5.0 | 4.9640 | True |
| Mean cos(θ_PC1) > 0.9 | 0.9 | 0.9988 | True |
| Mean cos(θ_PC2) > 0.8 | 0.8 | 0.9973 | True |

---

## Extended (7 features)
n = 1478 (half = 739)

### 1. Summary Statistics

| Metric | Mean | SD | 95% CI | Min | Max |
|---|---|---|---|---|---|
| |PC1_A − PC1_B| % | 2.4711 | 1.7861 | [0.1073, 6.2870] | 0.0036 | 10.2901 |
| |PC2_A − PC2_B| % | 1.1330 | 0.8917 | [0.0453, 3.3294] | 0.0007 | 4.8351 |
| Eigenvalue corr(A,B) | 0.9880 | 0.0105 | [0.9627, 0.9990] | 0.9193 | 0.9999 |
| |cos(θ)| PC1 | 0.9777 | 0.0194 | [0.9274, 0.9973] | 0.8480 | 0.9989 |
| |cos(θ)| PC2 | 0.9091 | 0.0695 | [0.7425, 0.9940] | 0.5995 | 0.9986 |

### 2. Proportion Meeting Criteria (per iteration)

| Criterion | % Iterations Met |
|---|---|
| |ΔPC1| < 5% | 89.6 |
| |ΔPC2| < 5% | 100.0 |
| cos(θ_PC1) > 0.9 | 99.0 |
| cos(θ_PC2) > 0.8 | 91.8 |

### 3. Invariance Criteria (mean-based)

| Criterion | Threshold | Value | Met |
|---|---|---|---|
| Mean |ΔPC1| < 5% | 5.0 | 2.4711 | True |
| Mean |ΔPC2| < 5% | 5.0 | 1.1330 | True |
| Mean cos(θ_PC1) > 0.9 | 0.9 | 0.9777 | True |
| Mean cos(θ_PC2) > 0.8 | 0.8 | 0.9091 | True |

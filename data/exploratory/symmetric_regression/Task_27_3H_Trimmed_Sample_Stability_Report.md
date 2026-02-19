# Task 27.3H — Trimmed Sample Stability Report

Trim percentage: 10%, seed: 42

---

## Core (4 residuals)

### 1. PCA Metrics by Sample

| Sample | n | PC1 % | PC2 % | Cumul % | λ>1 | PR | ER |
|---|---|---|---|---|---|---|---|
| Full sample | 1482 | 56.5524 | 29.2059 | 85.7584 | 2 | 2.4054 | 2.8712 |
| Remove top 10% | 1334 | 48.7877 | 29.0289 | 77.8166 | 2 | 2.8675 | 3.2825 |
| Remove bottom 10% | 1334 | 56.6954 | 29.2290 | 85.9244 | 2 | 2.3967 | 2.8618 |
| Remove random 10% | 1334 | 56.6105 | 28.8699 | 85.4804 | 2 | 2.4105 | 2.8811 |

### 2. Differences from Full Sample

| Sample | ΔPC1 | ΔPC2 | ΔPR | Δλ>1 |
|---|---|---|---|---|
| Remove top 10% | -7.76 | -0.18 | 0.4621 | 0 |
| Remove bottom 10% | 0.14 | 0.02 | -0.0087 | 0 |
| Remove random 10% | 0.06 | -0.34 | 0.0051 | 0 |

### 3. Robustness Criteria

| Sample | |ΔPC1|<5% | |ΔPC2|<5% | |ΔPR|<0.5 | Δλ>1=0 |
|---|---|---|---|---|
| Remove top 10% | False | True | True | True |
| Remove bottom 10% | True | True | True | True |
| Remove random 10% | True | True | True | True |

---

## Extended (7 features)

### 1. PCA Metrics by Sample

| Sample | n | PC1 % | PC2 % | Cumul % | λ>1 | PR | ER |
|---|---|---|---|---|---|---|---|
| Full sample | 1478 | 32.6071 | 21.7428 | 54.3500 | 3 | 4.7276 | 5.4488 |
| Remove top 10% | 1331 | 27.8879 | 23.0953 | 50.9832 | 3 | 5.2104 | 5.8397 |
| Remove bottom 10% | 1331 | 32.7034 | 21.6497 | 54.3532 | 3 | 4.7196 | 5.4393 |
| Remove random 10% | 1331 | 32.2484 | 21.6689 | 53.9172 | 3 | 4.7703 | 5.4798 |

### 2. Differences from Full Sample

| Sample | ΔPC1 | ΔPC2 | ΔPR | Δλ>1 |
|---|---|---|---|---|
| Remove top 10% | -4.72 | 1.35 | 0.4828 | 0 |
| Remove bottom 10% | 0.10 | -0.09 | -0.0081 | 0 |
| Remove random 10% | -0.36 | -0.07 | 0.0427 | 0 |

### 3. Robustness Criteria

| Sample | |ΔPC1|<5% | |ΔPC2|<5% | |ΔPR|<0.5 | Δλ>1=0 |
|---|---|---|---|---|
| Remove top 10% | True | True | True | True |
| Remove bottom 10% | True | True | True | True |
| Remove random 10% | True | True | True | True |

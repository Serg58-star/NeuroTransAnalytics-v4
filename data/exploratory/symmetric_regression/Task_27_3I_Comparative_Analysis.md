# Task 27.3I — Comparative Analysis

Full population vs First-visit only

## Sample

| | Full | First-visit |
|---|---|---|
| Sessions | 1886 | 1482 |
| Subjects | 1482 | 1482 |

## Regression

| Model | R²_full | R²_fv | ΔR² | Residual Ratio_full | Residual Ratio_fv | Direction |
|---|---|---|---|---|---|---|
| delta_v4_left | 0.0030 | 0.0024 | -0.0006 | 0.9970 | 0.9976 | ↓ |
| delta_v4_right | 0.0113 | 0.0089 | -0.0024 | 0.9887 | 0.9911 | ↓ |
| delta_v5_left | 0.0139 | 0.0122 | -0.0017 | 0.9861 | 0.9878 | ↓ |
| delta_v5_right | 4.375421e-05 | 0.0002 | 0.0001 | 1.0000 | 0.9998 | ↑ |

## PCA Core

| Metric | Full | First-visit | Δ | Δ% | Direction |
|---|---|---|---|---|---|
| PC1 % | 56.5524 | 56.7082 | 0.1557 | 0.3 | ↑ |
| PC2 % | 29.2059 | 29.0715 | -0.1344 | -0.5 | ↓ |
| Cumulative % | 85.7584 | 85.7797 | 0.0214 | 0.0 | ↑ |
| λ>1 | 2 | 2 | 0 | 0.0 | = |
| PR | 2.4054 | 2.4002 | -0.0052 | -0.2 | ↓ |
| ER | 2.8712 | 2.8683 | -0.0030 | -0.1 | ↓ |

## PCA Extended

| Metric | Full | First-visit | Δ | Δ% | Direction |
|---|---|---|---|---|---|
| PC1 % | 32.6071 | 32.9062 | 0.2991 | 0.9 | ↑ |
| PC2 % | 21.7428 | 21.4085 | -0.3344 | -1.5 | ↓ |
| Cumulative % | 54.3500 | 54.3147 | -0.0353 | -0.1 | ↓ |
| λ>1 | 3 | 3 | 0 | 0.0 | = |
| PR | 4.7276 | 4.7206 | -0.0070 | -0.1 | ↓ |
| ER | 5.4488 | 5.4503 | 0.0015 | 0.0 | ↑ |

## Bootstrap Core

| Metric | Full | First-visit | Direction |
|---|---|---|---|
| Mean PC1% | 56.5828 | 56.7204 | ↑ |
| SD PC1% | 2.5266 | 2.3350 | ↓ |
| λ>1 modal | 2 (93.9%) | 2 (94.4%) | = |

## Bootstrap Extended

| Metric | Full | First-visit | Direction |
|---|---|---|---|
| Mean PC1% | 32.7215 | 32.9746 | ↑ |
| SD PC1% | 1.6012 | 1.5292 | ↓ |
| λ>1 modal | 3 (83.9%) | 3 (86.3%) | = |

## Split-Half Core

| Metric | Full | First-visit | Direction |
|---|---|---|---|
| Mean |ΔPC1| | 4.5491 | 3.7533 | ↓ |
| cos(θ_PC1) | 0.9988 | 0.9989 | ↑ |
| cos(θ_PC2) | 0.9973 | 0.9973 | ↓ |

## Split-Half Extended

| Metric | Full | First-visit | Direction |
|---|---|---|---|
| Mean |ΔPC1| | 2.4711 | 2.5207 | ↑ |
| cos(θ_PC1) | 0.9777 | 0.9815 | ↑ |
| cos(θ_PC2) | 0.9091 | 0.9146 | ↑ |

## Changes > 5% (absolute)

None

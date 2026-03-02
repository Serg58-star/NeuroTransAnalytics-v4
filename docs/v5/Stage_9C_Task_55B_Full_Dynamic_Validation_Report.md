# Stage 9C Task 55B — Full Dynamic Validation Report

**Validation Date:** 2026-03-02
**N=400, T=10 | No bootstrap**
**Selected κ:** 0.08

## 1. Summary Table

| κ | No Absorb | Spec. Gap | Stat. Q2 | Entropy | Slope | Silhouette | Result |
|---|---|---|---|---|---|---|---|
| 0.08 | ✓ | 0.194 ✓ | 49.4% ✓ | 0.669 ✓ | 0.0077 ✓ | 0.102 ✓ | **PASS** |
| 0.09 | ✓ | 0.174 ✓ | 47.3% ✓ | 0.708 ✓ | -0.0283 ✓ | 0.084 ✓ | **PASS** |
| 0.10 | ✓ | 0.166 ✓ | 46.1% ✓ | 0.602 ✓ | -0.0029 ✓ | 0.061 ✓ | **PASS** |

## 2. Transition Matrices

### κ = 0.08

| Origin | Q1(Stable) | Q2(Radial) | Q3(Ortho) | Q4(Volatile) |
|---|---|---|---|---|
| **Q1(Stable)** | 0.784 | 0.100 | 0.087 | 0.029 |
| **Q2(Radial)** | 0.080 | 0.886 | 0.000 | 0.033 |
| **Q3(Ortho)** | 0.609 | 0.007 | 0.383 | 0.001 |
| **Q4(Volatile)** | 0.500 | 0.471 | 0.000 | 0.029 |
### κ = 0.09

| Origin | Q1(Stable) | Q2(Radial) | Q3(Ortho) | Q4(Volatile) |
|---|---|---|---|---|
| **Q1(Stable)** | 0.792 | 0.091 | 0.091 | 0.026 |
| **Q2(Radial)** | 0.076 | 0.902 | 0.000 | 0.022 |
| **Q3(Ortho)** | 0.607 | 0.003 | 0.383 | 0.007 |
| **Q4(Volatile)** | 0.588 | 0.265 | 0.029 | 0.118 |
### κ = 0.10

| Origin | Q1(Stable) | Q2(Radial) | Q3(Ortho) | Q4(Volatile) |
|---|---|---|---|---|
| **Q1(Stable)** | 0.817 | 0.081 | 0.084 | 0.017 |
| **Q2(Radial)** | 0.086 | 0.907 | 0.000 | 0.007 |
| **Q3(Ortho)** | 0.595 | 0.004 | 0.393 | 0.008 |
| **Q4(Volatile)** | 0.550 | 0.450 | 0.000 | 0.000 |

## 3. Eigenvalue Spectra

- **κ=0.08:** [1.0, 0.8064, 0.2822, 0.0057]
- **κ=0.09:** [1.0, 0.8257, 0.2803, 0.0886]
- **κ=0.10:** [1.0, 0.8344, 0.297, 0.0147]

## 4. 選択 Final Selected Kappa

**κ = 0.08** — minimum sufficient stabilization parameter identified.

# Stage 9C Task 56 — TPF Revalidation Report

**Validation Date:** 2026-03-02
**Locked κ:** 0.08 | **N=500, T=10**
**Final Status:** **REJECTED**

## 1. Validation Criteria Table

| # | Criterion | Target | Measured | Pass |
|---|---|---|---|---|
| 1.1 | Max Absorbing State ($P_{ii}$) | $\le 0.95$ | 0.924 | ✓ |
| 1.2 | Transition Matrix Row Sum | $= 1.0$ | Yes | ✓ |
| 2.1 | Max Eigenvalue ($\|\lambda_{max}\|$) | $= 1.0$ | 1.00000 | ✓ |
| 2.2 | Spectral Gap | $\ge 0.15$ | 0.2002 | ✓ |
| 3 | Max Stationary Mass | $\le 50\%$ | 67.9% | ✗ |
| 4.1 | Mean System Entropy | $\ge 0.60$ | 0.691 | ✓ |
| 4.2 | Min Quadrant Entropy | $\ge 0.10$ | 0.316 | ✓ |
| 5 | Longitudinal Silhouette | $< 0.20$ | 0.093 | ✓ |

## 2. Revalidated Transition Probability Field

| Origin | Q1(Stable) | Q2(Radial) | Q3(Ortho) | Q4(Volatile) |
|---|---|---|---|---|
| **Q1(Stable)** | 0.748 | 0.141 | 0.079 | 0.031 |
| **Q2(Radial)** | 0.052 | 0.924 | 0.000 | 0.023 |
| **Q3(Ortho)** | 0.617 | 0.017 | 0.359 | 0.007 |
| **Q4(Volatile)** | 0.393 | 0.541 | 0.000 | 0.066 |

## 3. Spectral & Stationary State

**Eigenvalues:** `[1.0, 0.7998, 0.263, 0.0342]`
**Stationary Distribution:**
- Q1 (Stable): 26.2%
- Q2 (Radial): 67.9%
- Q3 (Ortho): 3.2%
- Q4 (Volatile): 2.6%

## 4. Entropy by Quadrant

- Q1: 0.803
- Q2: 0.316
- Q3: 0.768
- Q4: 0.878

## 5. Conclusion

One or more TPF criteria failed. The Risk Layer remains unstable. Further dynamic correction required.

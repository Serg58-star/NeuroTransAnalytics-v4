# Task H5 — Implementation Plan (Correlated Baseline Generator Redesign)

**Version:** v1.0
**Date:** 2026-03-04
**Objective:** Redesign the Phase-1 Baseline Generator in `population_generator_v5.py` to produce a 1D-dominant geometry, correctly structured global latent factors, and explicit demographic scaling (Sex and Age).

## User Review Required

> [!IMPORTANT]
> **Approval Gate Check**: This is a mandatory Implementation Plan strictly following the project Governance Policy. GoAn is **BLOCKED** from writing or modifying any implementation code until explicit approval is granted by the User ("Approved for implementation. Task H5").

## Proposed Changes

---

### Phase 1: Correlated Baseline Generator Modification

#### [MODIFY] `population_generator_v5.py`

We will replace the existing simplistic `base_speed` allocation mechanism with the formal `G_i` model dictated by Stage H5 requirements.

1. **Global Latent Factor ($G_i$)**:
   - Replace `np.random.normal(250, 40)` with a `LogNormal` distribution.
   - Target $\mu, \sigma$ will be tuned so the final expected $G_i$ resembles physiological speeds (~250ms expected, heavy right tail).

2. **Demographic Assignments**:
   - Assign `Sex_i` (Male/Female) deterministically or strictly balanced. Apply scaling $\alpha_{sex}$ such that Male/Female $\lambda_1$ ratio $\approx 1.8 - 2.1$.
   - Assign `Age_i` (e.g., Uniform 20 to 80).
   - Apply non-linear function $f_{age}(\text{Age})$ to construct a U-shaped or non-monotonic age response to minimize Q2 variance at optimal age ranges and inflate at extremes.
   - Final Subject Base Speed: $G_{i} = G_{i} \times (1 + \alpha_{sex}) \times f_{age}(\text{Age}_i)$.

3. **Spatial Channels (L, C, R)**:
   - To guarantee that `Corr(L, C) >= 0.90` and `Effective Rank ≈ 1.2`, we will strictly model spatial channel means using shared $G_i$ offset plus small local perturbations $\epsilon_{pos, i}$.
   - The physiological variance (`std_dev` for each trial) will dynamically scale with $G_{i}$, guaranteeing 1D-dominant variance profile across subjects while maintaining localized noise.

---

### Phase 2: Generation and Validation Scripts

#### [NEW] `scripts/stage_H5_generator_validation.py`

A dedicated audit procedure to run the required verification checks over the newly generated baseline architecture.

- **Block 1: Spectral Geometry**: Computes Effective Rank, PC1 variance %, and Cross-Channel Correlations on the $F_1$ matrix. Output: `docs/redesign/H5_Block1_Baseline_Spectral_Geometry.md`
- **Block 2: Sex Scaling**: Verifies that the $\lambda_1$ variance subset ratio for Males vs Females is in the $[1.8, 2.1]$ window. Output: `docs/redesign/H5_Block2_Sex_Baseline_Scaling.md`
- **Block 3: Age Structure**: Validates the non-monotonic nature of the age factor relative to Q2 variance. Output: `docs/redesign/H5_Block3_Age_Baseline_Structure.md`
- **Block 4: Load Independence**: Projects phase-2 load using `generate_longitudinal_population()` and ensures base geometry generates properly and independent delta. Output: `docs/redesign/H5_Block4_Baseline_Load_Independence.md`
- **Block 5: System Compatibility**: Confirms $\kappa=0.08$ anchor stability for longitudinal sequences. Output: `docs/redesign/H5_Block5_v5_System_Compatibility.md`

---

## Verification Plan

### Automated Verification

After implementation, we will instruct execution of `PYTHONPATH=. python scripts/stage_H5_generator_validation.py` which will algorithmically verify all bounding constraints established by the Stage H5 audit requirement parameters. The script will output explicit `PASS`/`FAIL` markers for each geometrical and demographic requirement to the required deliverables.

### Manual Review

- User review of the generated logs and the 5 output documents.
- If necessary, tune distribution parameters (e.g., `LogNormal` variance or $f_{age}$ polynomial coefficients) to cleanly align with empiric geometry constraints.

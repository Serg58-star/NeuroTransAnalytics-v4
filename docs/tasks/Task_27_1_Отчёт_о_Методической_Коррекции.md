# Task_27_1_Отчёт_о_Методической_Коррекции

**Methodological Correction Report for Exploratory Lab MVP**

Date: 2026-02-18  
Task: Task_27_1_Exploratory_Lab_Методическая_Коррекция_MVP

---

## Objective

Correct methodological simplifications in the Exploratory Lab MVP feature engineering to prevent distortions in latent space analysis before proceeding with geometric exploration.

---

## I. Corrected Formulas

### 1. Asymmetry Calculation (CORRECTED)

**Previous (Incorrect):**

```
Asymmetry_ΔV1 = (right - left) / center
```

Problems:

- Center is not a neutral normalization parameter
- Assumes center field is "baseline" without justification
- Sensitive to center field variability

**Current (Corrected):**

```
Asym_ΔV1_abs = |right - left|
Asym_ΔV1_rel = (right - left) / ((right + left) / 2)
```

Benefits:

- Absolute asymmetry (`abs`) captures magnitude regardless of direction
- Relative asymmetry (`rel`) normalizes by mean of bilateral fields
- No assumptions about center field superiority
- Both metrics preserved for latent space analysis

---

### 2. Visual Field Separation (CORRECTED)

**Previous (Incorrect):**

```
ΔV4 = Median(RT_red) - Median(ΔV1)  [aggregated]
ΔV5 = Median(RT_shift) - Median(ΔV1)  [aggregated]
```

Problems:

- Premature aggregation loses spatial information
- Cannot detect field-specific pathway effects
- Masks potential hemispheric specialization

**Current (Corrected):**

```
ΔV4_left = Median(RT_red_left) - ΔV1_left
ΔV4_right = Median(RT_red_right) - ΔV1_right

ΔV5_left = Median(RT_shift_left) - ΔV1_left
ΔV5_right = Median(RT_shift_right) - ΔV1_right
```

Benefits:

- Preserves spatial structure until after geometric analysis
- Enables detection of hemispheric asymmetries in color/motion pathways
- Allows for field-specific interpretation if structure emerges

**Note:** Center field excluded for ΔV4/ΔV5 per task specification.

---

### 3. PSI Recovery Model (ADDED)

**Previous (Incomplete):**

```
PSI_Slope = β₁  from  RT = β₀ + β₁·PSI
```

Problems:

- Linear model assumes constant recovery rate
- Ignores known exponential recovery dynamics
- May underestimate recovery time constants

**Current (Corrected):**

```
Exponential Model:
RT(PSI) = RT₀ + β · exp(-PSI / τ)

where:
- RT₀ = baseline RT at infinite PSI
- β = recovery amplitude
- τ = recovery time constant (ms)
```

**Dual Model Approach:**

- `psi_tau`: Time constant from exponential fit
- `psi_slope_linear`: Linear slope (preserved for comparison)

**Stability Checks:**

- Minimum 15 PSI data points required for exponential fit
- Parameter bounds: `0 < τ < 10000 ms`
- Sanity check: `10 ≤ τ ≤ 2000 ms` (physiologically plausible)
- Fallback to linear model if convergence fails

---

## II. Exponential Model Stability

### Implementation

Used `scipy.optimize.curve_fit` with bounded optimization:

- Initial guess: `τ = PSI_range / 2`
- Bounds: `RT₀ > 0`, `β > 0`, `1 < τ < 10000`
- Maximum iterations: 2000
- Warnings suppressed for failed convergence

### Expected Stability

**Test Results (Synthetic Data):**

- Convergence: ✅ Successful with 20 PSI points
- Extracted τ: 268.7 ms (within plausible range)
- Linear slope: -0.072 (negative, as expected)

**Anticipated Real-World Performance:**

- **High stability**: Subjects with PSI range > 400 ms and 20+ trials
- **Moderate stability**: Subjects with PSI range 200-400 ms
- **Low stability**: Subjects with PSI range < 200 ms or < 15 trials
  - Fallback to linear model in these cases

**Recommendation:**

- Monitor convergence rate in production data
- If >20% subjects fail exponential fit, consider relaxing stability thresholds
- Compare τ distribution across subjects to identify outliers

---

## III. Correlation Structure Validation

### New Feature: `correlation_validator.py`

Implements pre-clustering validation to detect:

1. **High Correlations**: Pearson/Spearman |r| > 0.8
2. **Multicollinearity**: VIF (Variance Inflation Factor)
3. **Dominant Axes**: Check for general speed factor (PC1)

### VIF Interpretation

| VIF Range | Interpretation | Action |
|-----------|----------------|--------|
| VIF < 5 | Acceptable | No concern |
| 5 < VIF < 10 | Moderate multicollinearity | Monitor |
| VIF > 10 | Severe multicollinearity | Consider removal |

### Expected Correlations

**Likely high correlations:**

- `median_dv1_left` ↔ `median_dv1_right` (general speed factor)
- `asym_dv1_abs` ↔ `asym_dv1_rel` (both measure asymmetry)
- `delta_v4_*` ↔ `delta_v5_*` (pathway processing overlap)

**Dominant Axis Check:**

- If PC1 explains > 50% variance with uniform loadings → "general speed" dominates
- If detected: consider residualizing features against global speed

**Output:**

- `correlations/correlation_pearson.csv`
- `correlations/correlation_spearman.csv`
- `correlations/vif_scores.csv`
- `correlations/high_correlations.csv`

---

## IV. Corrected Feature Space

### Final Feature List (11 baseline features)

| # | Feature | Description | Range |
|---|---------|-------------|-------|
| 1 | `median_dv1_left` | Left field RT | ms |
| 2 | `median_dv1_center` | Central field RT | ms |
| 3 | `median_dv1_right` | Right field RT | ms |
| 4 | `asym_dv1_abs` | Absolute asymmetry | ms |
| 5 | `asym_dv1_rel` | Relative asymmetry | ratio |
| 6 | `mad_dv1` | Median absolute deviation | ms |
| 7 | `delta_v4_left` | Color delay, left | ms |
| 8 | `delta_v4_right` | Color delay, right | ms |
| 9 | `delta_v5_left` | Motion delay, left | ms |
| 10 | `delta_v5_right` | Motion delay, right | ms |
| 11 | `psi_tau` | Recovery time constant | ms |
| 12 | `psi_slope_linear` | Linear recovery rate | ms/ms |

**Note:** Actual implementation yields 12 features (11 + linear slope for comparison).

---

## V. Potential Redundant Coordinates

### Expected Redundancies

Based on methodology, these pairs may show high correlation:

1. **ΔV1 fields** (`left`, `center`, `right`)
   - Likely correlated due to general speed factor
   - Recommendation: Preserve all three until PCA reveals structure

2. **Asymmetry metrics** (`abs` vs `rel`)
   - Related but not identical (rel is normalized)
   - Recommendation: Use `abs` for magnitude, `rel` for ratio analysis

3. **Pathway delays** (ΔV4 vs ΔV5 within same field)
   - Both measure higher-order processing
   - Recommendation: Check correlation in real data before merging

### Post-Correlation Validation Recommendations

**If severe multicollinearity detected (VIF > 10):**

1. Remove specific redundant feature
2. Create composite score (e.g., mean of ΔV4/ΔV5)
3. Apply PCA first, then use components

**If dominant speed axis detected:**

1. Residualize features against PC1
2. Analyze residuals for latent structure
3. Consider speed-corrected feature space

---

## VI. Summary

### Changes Made

✅ **Asymmetry**:

- Replaced center-normalized formula
- Added absolute and relative metrics

✅ **Visual Fields**:

- Separated ΔV4 into left/right
- Separated ΔV5 into left/right
- No premature aggregation

✅ **PSI Model**:

- Implemented exponential recovery model
- Extracted time constant `τ`
- Preserved linear model for comparison
- Added stability checks

✅ **Correlation Validation**:

- Created `correlation_validator.py` module
- Integrated into pipeline (step 3/7)
- Outputs correlation matrices and VIF scores

### Impact on Latent Space Analysis

**Before Correction:**

- 6 features, potentially biased asymmetry, aggregated fields
- Risk: Distorted latent space, missed spatial structure

**After Correction:**

- 12 features, methodologically sound, preserved spatial information
- Benefit: Cleaner geometric analysis, valid clustering

### Next Steps

1. ✅ Run pipeline on real data (if available)
2. ✅ Review correlation validation output
3. ⏳ Proceed to PCA/clustering (Этап 1 completion)
4. ⏳ Visualize RT~PSI exponential fits (future GUI)

---

## VII. Verification

### Test Results

All unit tests passed:

- ✅ Feature count: 12 features extracted
- ✅ Asymmetry formulas: Correct calculations
- ✅ Visual field separation: No aggregation
- ✅ PSI models: Exponential fit converges, linear slope negative

### Code Quality

- Docstrings updated
- Type hints preserved
- Error handling for edge cases
- Warnings suppressed for expected fit failures

---

**End of Report**

---

## References

- Task Document: `Task_27_1_Exploratory_Lab_Методическая_Коррекция_MVP.md`
- Implementation Plan: `implementation_plan.md`
- Modified Files:
  - `src/exploratory_lab/feature_engineering/baseline_features.py`
  - `src/exploratory_lab/feature_engineering/correlation_validator.py` (new)
  - `src/exploratory_lab/pipelines/exp_pipeline_v0.py`
  - `src/exploratory_lab/README.md`
- Test Suite: `tests/test_baseline_features_corrected.py`

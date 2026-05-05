# Stage G — Legacy Stimulus Structure Investigation Report

Based on the execution of the 10-task package against the legacy SZR database, here are the empirical findings regarding the legacy stimulus generator's hidden structuring:

## Task 1: Positional Color Distribution

We tested the null hypothesis that `P(color | position)` is uniformly distributed.

- **Result:** Chi-square statistic: $3495.35$, $p$-value: $0.0000$
- **Probability Matrix:**
  - `center`: Blue (12.5%), Green (16.6%), Red (70.8%)
  - `left`: Blue (21.0%), Green (16.5%), Red (62.4%)
  - `right`: Blue (16.6%), Green (16.6%), Red (66.7%)
- **Conclusion:** **BIASED**. The legacy system heavily biases red towards the center and distributes non-target colors asymmetrically.

## Task 2: ContextTriple Sequence Structure

We tested for dependencies in the sequential masking context across lags 1-10.

- **Autocorrelations:**
  - Lag 1: $0.682$, Lag 2: $0.366$, Lag 3: $0.083$
  - Lag 4: $0.012$, Lag 5: $-0.056$ ...
- **Conclusion:** **Slow context dynamics**. There is a strong positive autocorrelation at lags 1 and 2, meaning context triples do not behave as independent coin tosses; they "stick" to specific states for multiple trials.

## Task 3: ContextTriple vs PSI

We tested if the generated PSI interval is structurally coupled with the masking context parameters constraint.

- **Result:** Chi-square (Dominant Color vs PSI Bin): $109421.47$, $p$-value: $0.0000$
- **Conclusion:** **Structured relationship**. The system intentionally adjusted the pre-stimulus interval parameters depending on the specific masking triples presented.

## Task 4: Color Balance Trajectory

We tracked the cumulative color balance (P vs K channels) across the sequence of 36 stimuli index.

- **Result:** Spearman correlation index vs dominant color: $-0.058$, $p$-value: $3.89 \times 10^{-286}$
- **Conclusion:** **P/K channel balance drift**. The sequence slowly drifts, altering the functional load on different channels over time rather than maintaining stationary balance.

## Task 5: Channel Balance Map

We mapped the context triples onto the clinical P, K, R coordinates to check the effect on $\Delta V_4$.

- **Result:** Median $\Delta V_4$:
  - Green Dominant (K-channel): $100.50$ ms
  - Blue Dominant (P-channel): $115.00$ ms
  - Correlation (Num Green vs $\Delta V_4$): $-0.190, p=0.0000$.
- **Conclusion:** Channel loading maps correctly. Shifts in green vs blue load correlate negatively with the speed shift.

## Task 6: Position-weighted Channel Model

We assessed if the central field of view (FOV) acts as a unique multiplier for channel load, or simply a spatial tag.

- **Result:** Median $\Delta V_4$: Left=$115$, Center=$109$, Right=$100$.
- **Conclusion:** **No central advantage found**. The central position did not exhibit a multiplier effect distinct from the lateral positions in terms of driving $\Delta V$.

## Task 7: Context Complexity Index

We computed the Shannon entropy for each test triple and checked its correlation to cognitive load recovery $\Delta V$.

- **Result:** Spearman correlation (Entropy vs $\Delta V_4$): $0.057$, $p$-value: $8.5 \times 10^{-93}$
- **Conclusion:** A small but statistically significant structural interaction exists between context complexity and load shift.

## Task 8: PSI–Context Interaction

We tested if recovery times varied according to the specific context triples displayed during that interval.

- **Result:** PSI vs $\Delta V_4$ correlation by dominance:
  - Green Dominant: $-0.058$
  - Blue Dominant: $-0.259$
- **Conclusion:** PSI interaction varies fundamentally depending on the active channel state. Blue contexts suppress recovery significantly faster than green.

## Task 9: Stimulus Index Drift

We compared distributions of parameters between the early, mid, and late parts of the test block.

- **Triple Dominance Drift:**
  - Early: Blue Dominant ($45.2\%$), Neutral ($21.0\%$), Green Dominant ($33.6\%$)
  - Mid:  Blue Dominant ($29.0\%$), Neutral ($37.4\%$), Green Dominant ($33.4\%$)
  - Late:  Blue Dominant ($41.6\%$), Neutral ($33.3\%$), Green Dominant ($24.9\%$)
- **Conclusion:** **Protocol drift confirmed**. The fundamental load distributions shift throughout the test sequence.

## Task 10: Perceptual Contrast Index

We approximated perceptual contrast against background and correlated it with load delay.

- **Result:** Spearman correlation (Contrast vs $\Delta V_4$): $-0.195, p=0.0000$
- **Conclusion:** Higher perceptual contrast strongly correlates with lower structural delays.

---

### Architectural Synthesis

The Legacy System **was not** structurally neutral. It featured:

1. **Built-in memory**: $AR(2)$ autocorrelation in masking triples means the sequence possessed localized momentum.
2. **Positional/Color Coupling**: The generator actively biased red targets to the center FOV while shifting P/K channels to the lateral edges.
3. **Drift**: The probability matrix inherently drifted over the 36-item index sequence, slowly varying the load curve without intervention.

These findings mandate that **Stimulus Generator v5 must NOT simply clone the legacy randomizer's mathematical profile.** Doing so would insert hidden structural coupling between PSI and Color back into the system, polluting clinical lateralization scores with protocol artifact dynamics.

v5 must ensure orthogonal separation of PSI, triple selection, and positional targeting.

# H3.1c Block 1 — Motor Model Definition

**Date**: 2026-03-04  
**Status**: COMPLETED  
**Basis**: Stage H3.1c — Correlated Motor Layer Simulation Audit

---

## Scope

Formal definition of the Monte Carlo parameters used to synthetically construct the latent Motor execution time `Motor_i` from the extracted baseline empirical PC1 Global Speed `G_i`.

## Parametric Model

We defined the total baseline reaction time as:
$$ RT_i = Neural_i + Motor_i $$

Given that Motor Execution is globally shared across left, center, and right channels, we anchored `Motor_i` entirely to the PC1 factor `G_i`, adding local physiological noise `η`.

$$ Motor_i = (\alpha \times \frac{\sigma(Baseline)}{\sigma(G)}) \times G_i + \eta_i $$

Where:

* **`G_i`**: The extracted empirical 1D speed score.
* **`α`**: The assumed Variance fraction that Motor execution is responsible for in the human population. Simulated from `0.60` (Motor is 60%) to `0.90` (Motor is 90% of global variance).
* **`η_i`**: Uncorrelated motor nerve velocity noise `N(0, 5ms)` or `N(0, 10ms)`.

This rigorous assumption allowed us to aggressively construct a "worst-case motor confound" scenario where up to 90% of the tightly-coupled empirical variance was attributed strictly to motor execution time, artificially forcing the mathematically isolated Neural estimates `Neural_i` away from their highly-correlated boundaries.

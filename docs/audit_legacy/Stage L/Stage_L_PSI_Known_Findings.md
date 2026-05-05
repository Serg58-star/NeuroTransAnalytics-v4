# Stage_L_PSI_Known_Findings

**Context:** Synthesis of historical repository findings, analysis models, and Stage-L/Stage-H architectural audits regarding the Pre-Stimulus Interval (PSI) and its interaction with RT / structural $\Delta$ components.

---

### 1. Existing analysis of PSI influence on RT or components

Extensive analysis has been performed to map how PSI influences isolated structural components ($\Delta V4$ and $\Delta V5/MT$), completely replacing parametric regression (mean) with robust statistics (median bins) during Task L6:

* **PSI Sensitivity Modeling (Stage L4):** Segregated components into distinct PSI bins (`short`, `medium`, `long`) to evaluate penalties of extended waiting windows (`psi_long_vs_short_ms`).
* **Optimal Temporal Readiness (Stage L5):** Identified a distinct biological "readiness window." The minimum median processing delays (88ms for V4, 118ms for V5/MT) systematically occurred within the `(2000.0, 2400.0]` ms PSI bin.
* **Architectural Standing (Stage H3 Audit):** The `H3 PSI Structural Contribution Audit` concluded that PSI acts as a "Parallel Independent Domain." It functions as an additive chronological load mapping expectation/readiness but **does not** create or alter the fundamental latent spectral geometry of the cognitive space.

### 2. Graphs or statistics of RT ~ PSI

Specific outputs mapping the RT/$\Delta$ to PSI relationship include:

* **Visual Plots:** Stage L3 specifically spawned `figures/rt_vs_psi.png`, which plots the strict robust `median` component timing ($\Delta V4, \Delta V5/MT$) mapped linearly against PSI values. The audit notes: *"RT values show visible spread and variation across the different PSI levels."*
* **Statistical Tables:**
  * `L4_results/psi_sensitivity_model.csv` contains binned median sensitivity metrics.
  * `L5_results/B1_optimal_psi.csv` defines the minimal $\Delta$ boundaries matching the 2000-2400ms bucket.
  * `L5_results/B3_subject_sensitivity.csv` defines intra-subject Spearman rhos mapping pure PSI to pure RT/$\Delta$ degradation.

### 3. Any discovered periodicity or structure in PSI sequence

Analyses exploring predictable structure within the deterministic sequence revealed:

* **Generator Predictability / Markov Bias (Stage L5 - B2):** Analyzed whether subjects build expectations over the chronological sequence. Evaluated Spearman correlation of current Component $\Delta$ against the *lagged* PSI (`spearman_delta_psi_prev`). There is a minor positive correlation (~0.08 to 0.09), indicating subjects attempt to "predict" the deterministic generator based on recent prior intervals.
* **Micro-Oscillatory Attention Cycles (Stage L5 - E1):** Found significant short-lag internal rhythmicity across lag-1 (~0.29) and lag-2 (~0.38) for $\Delta V5/MT$. The deterministic structure of legacy PSI timings combined with fixed bounds creates oscillatory anticipation curves.

### 4. Evidence that `stimulus_index` distribution interacts with PSI

While no massive cross-interaction term (e.g., $PSI \times stimulus\_index$) governs the core matrix geometry, the system handles them as two intersecting axes of temporal strain:

* `stimulus_index` rules **Progressive Cognitive Load / Sequential Exhaustion** (proven by escalating median $\Delta$ delays mapped from "Early -> Mid -> Late" sections in Stage L5 A2).
* `PSI` rules **Acute Intratrial Anticipation / Readiness** (proven bounded optimal readiness and peripheral degradation slopes during holding periods).
* **Interaction:** The short-lag predictability (Markov bias) proves that earlier segments of the `stimulus_index` train subjects on the legacy protocol's bounded PSI variation, cementing an expectation rhythm that drives the sequential oscillatory cycles detected in later `stimulus_index` events. As the global test progresses (higher `stimulus_index`), the base component $\Delta$ rises due to load/fatigue, while the PSI-driven variability sits directly on top of that elevated baseline.

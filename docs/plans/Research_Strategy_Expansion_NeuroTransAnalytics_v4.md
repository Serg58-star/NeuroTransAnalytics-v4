Research Strategy Expansion: NeuroTransAnalytics v4
1. Executive Summary: The 2D Residual Invariant
The most significant finding of the recent analytical cycle is the discovery of a stable, 2-dimensional latent structure within the residual space of the core regression model (ΔV1 = f(PSI, Position, Color)).

1.1 The Invariant
Core PCA Stability: Across 1000 bootstrap iterations and 500 split-half trials, the first two principal components explain ~40% and ~14% of residual variance respectively.
Population Robustness: This structure remains invariant when restricted to first visits only, confirming it is a population-level property rather than an artifact of repeated measurements.
Sensitivity: PC1 shows sensitivity to extreme residual outliers, suggesting that "axial drift" in the residual space is tied to specific high-variance sessions/subjects.
2. Subject and Session Categorization Strategy
The discovery of the 2D residual space allows for a transition from simple scalar metrics (Mean, SD) to Geometric Trajectory Analysis.

2.1 Trajectory Classification
We propose classifying subject evolution in the population PC space:

Stable (Anchor): Sessions clustered tightly near the population mean.
Axial Drift (Systematic): Chronological movement along PC1 (likely linked to fatigue/familiarization).
Chaotic (Attention-Driven): High-amplitude, non-systematic jumps between sessions.
2.2 Residual Norm as an Attention Metric
Current data shows that "outliers" are not random noise but structured signatures.

Strategic Change: Cease outlier removal. Replace with Residual Attention Index (RAI).
Implementation: The norm of the residual vector $|r|$ represents the "unexplained" portion of the RT. Large $|r|$ correlates with "Chaotic" trajectory classification, serving as a direct proxy for attentional lapses.
3. Untapped Analytical Opportunities
3.1 The "Gray-scale V1" Calibration
To further isolate the Glutamate/GABA component (V1) from the Acetylcholine (V4) component, we suggest a future calibration step:

Procedure: Implement a sub-test using gray-scale stimuli of varying luminance.
Goal: Establish the luminance-latency curve for V1 without the "color-pathway" overhead, providing a cleaner baseline for ΔV4 calculation.
3.2 Tapping Tests (Motor Convergence)
The current V1 contains an inseparable motor component.

Expansion: Integrate a pre-test tapping series (Left/Right hand).
Formula: $True\ V1 = V1_observed - Motor_Tapping_Time$.
3.3 Cognitive Load & Depletion Analysis (V5 Direction)
The current system measures "state". The next phase must measure "reserve".

Opportunity: Deploy a secondary task (e.g., n-back or audit-interference) immediately following the standard trial.
Metric: The delta in ΔV4 and ΔV5/MT under load defines the Neurotransmitter Depletion Rate (NDR).
4. Architectural Simplification & Redundancy
4.1 Unified Scenario Engine
The current proliferation of standalone scripts (Tasks 27.x) should be consolidated into a C3.4 Scenario Engine.

Redundancy: Remove legacy script-based data loading. Centralize via ExploratoryController.
Contract: All analytical outputs must conform to ScenarioResult or DistributionPack to ensure the C3.5 Visualization layer can render any exploratory result without modification.
4.2 C3.5 Visualization Autonomy
The GUI should transition from a "Fixed Dashboard" to a "Dynamic Renderer".

Rule: GUI must not know what it is plotting (RT vs ΔV4 vs PCA score). It should only know how to plot the contract-compliant objects provided by the engine.
5. Development Strategy for Testing Program (v5)
The ultimate goal of the v4 audit is the design of the NeuroTrans-v5 Testing System.

Feature	NeuroTrans-v4 (Current)	NeuroTrans-v5 (Future)
V1 Baseline	Estimated from PZR	Multi-luminance Gray-scale
Motor Component	Integrated (Unknown)	Separated (Tapping Test)
Attention	Outlier Removal	Residual Attention Index (RAI)
Dimension	Scalar (Mean/SD)	Vector (PCA Trajectory)
Load	Implicit (Positional)	Explicit (Cognitive Task)
6. Conclusion
The NeuroTransAnalytics-v4 project has moved beyond "measuring reaction times" to deciphering the geometry of neural response space. The path forward lies in integrating the motor-tapping baseline and transitioning to a depletion-based load model, while maintaining the architectural purity of the C-series layers.
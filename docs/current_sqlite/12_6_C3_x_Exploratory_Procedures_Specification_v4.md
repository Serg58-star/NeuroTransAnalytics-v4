# C3.x — Exploratory Analysis Procedures Specification v4

## 1. Introduction

This document specifies the **C3.x Exploratory Analysis Procedures** for the NeuroTransAnalytics-v4 project. C3.x is a formal exploratory computation layer located between C3 (Core Computation) and C3.5 (Visualization).

### 1.1 Architectural Position

- **C2**: Data Storage (SQLite).
- **C3**: Core Computation (Invariant, Deterministic).
- **C3.x**: Exploratory Procedures (Flexible but Reproducible) — **THIS LAYER**.
- **C3.5**: Visualization (Read-only GUI).
- **C4**: Interpretation (Human-driven, External).

### 1.2 Core Principles

1. **Explicit Specification**: Every procedure must be parameterized and versioned.
2. **Reproducibility**: Identical parameters and data must yield identical results.
3. **Non-Interpretation**: No algorithmic decision-making or psychological inference is encoded.
4. **Passive Visualization**: C3.5 displays C3.x results without further computation.

---

## 2. Mandatory Procedure Template

Every exploratory procedure in this specification follows this template:

1. **Procedure Name**: Technical identifier.
2. **Exploratory Goal**: Structural regularity being explored.
3. **Input Data**: Required entities from C2 or C3.
4. **Parameters**: Explicit, recorded constants/settings.
5. **Output Artifact**: Data structure stored in or referenced by SQLite.
6. **Reproducibility Notes**: Specific requirements for identical output.
7. **Non-Interpretation Clause**: Standard disclaimer.

---

## 3. Exploratory Domain I — Distribution Shape Analysis

### 3.1 Procedure: Multimodality Detection (Dip Test)

- **Exploratory Goal**: Identify deviations from unimodality in RT or ΔV distributions.
- **Input Data**: `DistributionPack` (C3.5 source) or `ResponseEvent` RT values.
- **Parameters**: `significance_alpha` (default 0.05), `n_bootstraps` (default 2000).
- **Output Artifact**: `DistributionStructureResult` (contains Dip statistic and p-value).
- **Reproducibility Notes**: Fix random seed for bootstrap iterations.
- **Non-Interpretation Clause**: *“This procedure is exploratory and descriptive. It produces structural representations only and does not imply interpretation, inference, or evaluation.”*

### 3.2 Procedure: Wasserstein Distance Comparison

- **Exploratory Goal**: Quantify the "cost" of transforming one distribution shape into another across conditions.
- **Input Data**: Pairs of `DistributionPack` artifacts (e.g., PSI_short vs PSI_long).
- **Parameters**: `p_norm` (default 1).
- **Output Artifact**: `GeometryComparisonResult` (contains EMD value).
- **Reproducibility Notes**: Standard Earth Mover's Distance algorithm.
- **Non-Interpretation Clause**: *“This procedure is exploratory and descriptive. It produces structural representations only and does not imply interpretation, inference, or evaluation.”*

---

## 4. Exploratory Domain II — Temporal & Sequential Structure

### 4.1 Procedure: Trial-to-Trial Autocorrelogram

- **Exploratory Goal**: Detect sequential dependencies in the trial stream.
- **Input Data**: Series of `ResponseEvent` ordered by `stimulus_position_index`.
- **Parameters**: `max_lag` (default 10).
- **Output Artifact**: `TemporalStructureResult` (array of coefficients per lag).
- **Reproducibility Notes**: Ensure strictly chronological ordering.
- **Non-Interpretation Clause**: *“This procedure is exploratory and descriptive. It produces structural representations only and does not imply interpretation, inference, or evaluation.”*

### 4.2 Procedure: Change-Point Detection (Pelt)

- **Exploratory Goal**: Locate structural breaks in the mean or variance of RT over time.
- **Input Data**: Chronological series of `ResponseEvent.rt`.
- **Parameters**: `penalty_value` (default 'AIC'), `model_type` (default 'l2').
- **Output Artifact**: `RegimeSequenceResult` (indices of detected points).
- **Reproducibility Notes**: Use fixed cost functions and penalties.
- **Non-Interpretation Clause**: *“This procedure is exploratory and descriptive. It produces structural representations only and does not imply interpretation, inference, or evaluation.”*

---

## 5. Exploratory Domain III — Geometric Structure of Feature Space

### 5.1 Procedure: Nonlinear Embedding (t-SNE)

- **Exploratory Goal**: Map high-dimensional feature vectors (RT, ΔV1, ΔV4, ΔV5) to 2D for visual cluster inspection.
- **Input Data**: Matrix of `ComponentTiming` values for a `TestSession`.
- **Parameters**: `perplexity` (default 30), `learning_rate` (default 200), `random_seed` (fixed).
- **Output Artifact**: `EmbeddingResult` (2D coordinate matrix).
- **Reproducibility Notes**: **CRITICAL**: The random seed must be stored to regenerate the same layout.
- **Non-Interpretation Clause**: *“This procedure is exploratory and descriptive. It produces structural representations only and does not imply interpretation, inference, or evaluation.”*

### 5.2 Procedure: Procrustes Alignment

- **Exploratory Goal**: Compare the multidimensional "shape" of session results after removing translational and rotational differences.
- **Input Data**: Two `EmbeddingResult` matrices.
- **Parameters**: `scaling` (boolean, default true).
- **Output Artifact**: `GeometryComparisonResult` (disparity measure).
- **Reproducibility Notes**: Standard Procrustes superimposition.
- **Non-Interpretation Clause**: *“This procedure is exploratory and descriptive. It produces structural representations only and does not imply interpretation, inference, or evaluation.”*

---

## 6. Exploratory Domain IV — Dependency & Relationship Analysis

### 6.1 Procedure: Quantile Regression Map

- **Exploratory Goal**: Examine how relationships between components vary across different parts of the RT distribution (e.g., fast vs. slow responses).
- **Input Data**: `ComponentTiming` values.
- **Parameters**: `quantiles` (list: [0.1, 0.25, 0.5, 0.75, 0.9]).
- **Output Artifact**: `DependencyStructureResult` (matrix of coefficients per quantile).
- **Reproducibility Notes**: Use standard simplex or interior point solvers.
- **Non-Interpretation Clause**: *“This procedure is exploratory and descriptive. It produces structural representations only and does not imply interpretation, inference, or evaluation.”*

### 6.2 Procedure: Partial Correlation Graph

- **Exploratory Goal**: Represent direct dependencies between components while controlling for the influence of other variables.
- **Input Data**: Table of `ComponentTiming` and session metadata.
- **Parameters**: `threshold` (default 0.1 for edge visualization).
- **Output Artifact**: `DependencyStructureResult` (adjacency matrix).
- **Reproducibility Notes**: Inversion of the covariance matrix with fixed regularization.
- **Non-Interpretation Clause**: *“This procedure is exploratory and descriptive. It produces structural representations only and does not imply interpretation, inference, or evaluation.”*

---

## 7. Exploratory Domain V — Information-Theoretic Measures

### 7.1 Procedure: Permutation Entropy

- **Exploratory Goal**: Measure the complexity/predictability of the temporal sequence of responses.
- **Input Data**: Sequence of `ResponseEvent.rt`.
- **Parameters**: `order` (default 3), `delay` (default 1).
- **Output Artifact**: `InformationStructureResult` (entropy value).
- **Reproducibility Notes**: Bandt-Pompe algorithm implementation.
- **Non-Interpretation Clause**: *“This procedure is exploratory and descriptive. It produces structural representations only and does not imply interpretation, inference, or evaluation.”*

---

## 8. Exploratory Domain VI — Scenario-Level Meta-Analysis

### 8.1 Procedure: Scenario Similarity Graph

- **Exploratory Goal**: Discover clusters of similar experimental scenarios based on their outcome profiles.
- **Input Data**: Collection of `ScenarioResult` objects.
- **Parameters**: `metric` (default 'euclidean'), `linkage` (default 'ward').
- **Output Artifact**: `ScenarioSimilarityResult` (distance matrix and clustering tree).
- **Reproducibility Notes**: Scaling of input metrics must be standardized.
- **Non-Interpretation Clause**: *“This procedure is exploratory and descriptive. It produces structural representations only and does not imply interpretation, inference, or evaluation.”*

---

## 9. GUI Interaction Constraints (C3.5)

To maintain architectural integrity, the following rules apply to implementation:

1. **Selection only**: The GUI may allow the user to select *which* precomputed `C3.x` artifact to view.
2. **Display templates**: Every `C3.x` artifact type must have a corresponding read-only display template in C3.5.
3. **No 'Compute' Button**: The GUI must not contain buttons that trigger `C3.x` calculations. Calculations are handled by the C3 Pipeline runner.
4. **Metadata Visibility**: All visualization of `C3.x` results must display the associated parameters and random seeds used for generation.

---

## 10. Verification of Compliance

Following the **Architecture Guardian** protocol:

- **Boundary Integrity**: COMPLIANT. GUI is read-only.
- **Storage Discipline**: COMPLIANT. All results refer to `neuro_data.db` entities.
- **Versioning**: COMPLIANT. Every procedure requires explicit parameters and versioned output.
- **Non-Interpretation**: COMPLIANT. Every procedure includes a mandatory non-interpretation clause.

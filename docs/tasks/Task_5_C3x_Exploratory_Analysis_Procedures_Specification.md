# Task 5 — Specification of C3.x Exploratory Analysis Procedures  
## NeuroTransAnalytics-v4

---

## 1. Context

Tasks 1–4 have established a stable and validated architecture:

- Task 1: Data Contracts — canonical SQLite storage.
- Task 2: C2 Data Architecture — logical vs physical separation.
- Task 3: C3 Computation — deterministic, non-interpretative computation.
- Task 4: C3.5 Visualization — strictly read-only GUI.

The project now introduces **C3.x — Exploratory Analysis Procedures** to support
advanced, research-oriented analyses aimed at discovering novel structural
regularities in the data.

---

## 2. Architectural Position of C3.x

C3.x is a **formal exploratory computation layer** located between C3 and C3.5.

C2 — Data Architecture
C3 — Core Computation (invariant, deterministic)
C3.x — Exploratory Analysis Procedures ← THIS TASK
C3.5 — Visualization (read-only)
C4 — Interpretation (human-driven, outside code)


Principles:
- C3.x enables broad analytical freedom.
- All procedures are explicit, parameterized, and reproducible.
- No interpretation, inference, or decision-making is encoded.

---

## 3. Objective

Produce a **formal specification** of exploratory analysis procedures that:

- are applicable to the existing NeuroTransAnalytics data,
- enable discovery of previously unknown regularities,
- remain fully reproducible and versionable,
- can be safely visualized without GUI-side computation.

This task is:
- ✅ specification-only,
- ❌ NOT implementation,
- ❌ NOT algorithm selection or optimization,
- ❌ NOT interpretation or hypothesis testing.

---

## 4. Scope (STRICT)

### Included

Specification of **ALL exploratory procedures listed in Sections 6–11**.

### Excluded

- Any code or pseudocode implementation.
- Any claims about psychological, clinical, or cognitive meaning.
- Any GUI logic or interaction design.

---

## 5. Source of Truth (READ-ONLY)

docs/current_sqlite/RT_PSI_Data_Contract_v4.md
docs/current_sqlite/11_1_C2_1_Data_Model_v4.md
docs/current_sqlite/12_0_Карта_уровня_C3_Computation_&_Pipelines_v4.md
docs/current_sqlite/12_5_C3_5_Visualization_v4.md


---

## 6. Exploratory Domain I — Distribution Shape Analysis

### Procedures to Specify
- Multimodality detection (e.g. dip tests, mixture models).
- Shape comparison between conditions (Wasserstein, energy distances).
- Tail behavior and asymmetry analysis.

### Specification Must Include
- Input data requirements.
- Parameters (if any).
- Output artifact type (e.g. `DistributionStructureResult`).
- Notes on exploratory (non-inferential) status.

---

## 7. Exploratory Domain II — Temporal & Sequential Structure

### Procedures to Specify
- Trial-to-trial autocorrelation analysis.
- Change-point detection.
- Sliding-window dynamics (fixed windows).
- Regime/state detection (e.g. HMM-like formulations).

### Output Artifacts
- `TemporalStructureResult`
- `RegimeSequenceResult`

---

## 8. Exploratory Domain III — Geometric Structure of Feature Space

### Procedures to Specify
- Pairwise distance structure analysis.
- Procrustes alignment across conditions.
- Neighborhood preservation metrics.
- Nonlinear embeddings (t-SNE, UMAP, Isomap).

### Mandatory Notes
- Embeddings are exploratory representations only.
- Parameters and random seeds must be fixed and recorded.
- No embedding replaces the original feature space.

### Output Artifacts
- `EmbeddingResult`
- `GeometryComparisonResult`

---

## 9. Exploratory Domain IV — Dependency & Relationship Analysis

### Procedures to Specify
- Linear and mixed-effects dependency analysis.
- Quantile regression.
- Generalized additive relationships.
- Correlation and partial correlation structures.
- Graph-based dependency representations.

### Output Artifacts
- `DependencyStructureResult`

---

## 10. Exploratory Domain V — Information-Theoretic Measures

### Procedures to Specify
- Entropy-based complexity measures.
- Mutual and conditional mutual information.
- Regularity vs variability metrics.

### Output Artifacts
- `InformationStructureResult`

---

## 11. Exploratory Domain VI — Scenario-Level Meta-Analysis

### Procedures to Specify
- Distance metrics between ScenarioResult objects.
- Similarity graphs between scenarios.
- Hierarchical or relational grouping of scenarios.

### Output Artifacts
- `ScenarioSimilarityResult`

---

## 12. Mandatory Specification Template (for EACH procedure)

For every exploratory procedure, the specification MUST include:

1. **Procedure Name**
2. **Exploratory Goal** (what structure it explores, not what it proves)
3. **Input Data**
4. **Parameters** (explicit, fixed)
5. **Output Artifact**
6. **Reproducibility Notes**
7. **Explicit Non-Interpretation Clause**

Example clause:
> “This procedure is exploratory and descriptive. It produces structural representations only and does not imply interpretation, inference, or evaluation.”

---

## 13. GUI Interaction Constraint

- GUI (C3.5) may only:
  - select among precomputed C3.x artifacts,
  - display their visual representations.
- GUI MUST NOT:
  - trigger exploratory computation,
  - modify parameters,
  - recompute results.

---

## 14. Architectural Validation

Before finalizing the specification:

- Invoke **architecture-guardian**.
- Verify:
  - no interpretation (C4) language,
  - no GUI computation,
  - clear boundary between C3, C3.x, and C3.5.

If ambiguity arises:
- STOP
- REPORT
- DO NOT PROCEED silently.

---

## 15. Deliverable

A complete **C3.x Exploratory Analysis Procedures Specification** document
that can serve as:

- a research contract,
- a basis for future implementation tasks,
- a foundation for reproducible exploratory discovery.

---

End of Task 5.

# Task 6 — GUI Specification for C3.x Exploratory Results  
## NeuroTransAnalytics-v4

---

## 1. Context

Tasks 1–5 have established a complete and validated analytical architecture:

- Task 1: Data Contracts (SQLite canonical storage)
- Task 2: C2 Data Architecture
- Task 3: C3 Computation (deterministic, non-interpretative)
- Task 4: C3.5 Visualization (strictly read-only)
- Task 5: C3.x Exploratory Analysis Procedures (formal specification)

This task defines the **GUI contract** for presenting C3.x exploratory results.

The GUI must function strictly as a **window into exploratory computation**,  
not as a computation or interpretation environment.

---

## 2. Architectural Role of the GUI

The GUI implements **C3.5 Visualization** and MUST:

- display precomputed C3.x artifacts,
- preserve full reproducibility,
- expose parameters and provenance,
- avoid any hidden computation or inference.

The GUI MUST NOT:

- execute exploratory procedures,
- modify parameters,
- recompute results,
- access SQLite directly,
- interpret results.

---

## 3. Primary Screen: “Exploratory Results”

### 3.1. Screen Purpose

The “Exploratory Results” screen provides structured access to all
precomputed C3.x exploratory artifacts.

It enables:
- navigation across procedures,
- comparison of results,
- visual inspection of structural patterns.

---

### 3.2. Screen Structure

Mandatory sections:

1. **Procedure Selector**
   - List of exploratory procedures (from Task 5).
   - Grouped by exploratory domain.

2. **Artifact Selector**
   - Available result instances.
   - Displays metadata:
     - procedure name,
     - parameters,
     - algorithm version,
     - computation timestamp,
     - random seed (if applicable).

3. **Visualization Panel**
   - Renders the selected artifact using allowed templates.

4. **Provenance Panel**
   - Read-only display of:
     - inputs,
     - parameters,
     - constraints,
     - non-interpretation clause.

5. **Export Panel**
   - Export currently displayed representation only.

---

## 4. Visualization Templates by Result Type

The GUI MUST implement the following **template mappings**.

### 4.1. DistributionStructureResult
Allowed:
- histogram (precomputed bins),
- density curves (precomputed),
- modality markers.

Forbidden:
- recomputation of density,
- bin size manipulation.

---

### 4.2. TemporalStructureResult
Allowed:
- time-series plots,
- autocorrelation plots (precomputed),
- change-point markers.

Forbidden:
- dynamic window adjustment,
- recomputation of statistics.

---

### 4.3. RegimeSequenceResult
Allowed:
- segmented timeline,
- categorical color bands.

Forbidden:
- state merging or relabeling.

---

### 4.4. EmbeddingResult
Allowed:
- scatter plot (fixed coordinates),
- color/group overlays.

Mandatory:
- visible parameters,
- fixed random seed display.

Forbidden:
- recomputation,
- axis redefinition,
- interactive re-embedding.

---

### 4.5. DependencyStructureResult
Allowed:
- correlation heatmaps,
- dependency graphs (static).

Forbidden:
- recalculation,
- threshold manipulation.

---

### 4.6. InformationStructureResult
Allowed:
- bar plots,
- profile plots.

Forbidden:
- recomputation,
- normalization changes.

---

### 4.7. ScenarioSimilarityResult
Allowed:
- distance heatmaps,
- similarity graphs,
- dendrograms (precomputed).

Forbidden:
- dynamic clustering,
- similarity threshold tuning.

---

## 5. Interaction Rules (STRICT)

The GUI MAY:
- select procedures and artifacts,
- switch between visualization templates (if predefined),
- zoom and pan for inspection,
- export visible representations.

The GUI MUST NOT:
- expose sliders for algorithm parameters,
- trigger any computation,
- hide provenance or parameters,
- display interpretative language.

---

## 6. Language and Semantics

Allowed UI language:
- “shows”
- “displays”
- “represents”
- “corresponds to”

Forbidden UI language:
- “indicates”
- “suggests”
- “means”
- “implies”
- “reveals”

---

## 7. Acceptance Criteria

The GUI specification is correct if:

1. No exploratory computation can be triggered from the UI.
2. All visualized values match stored C3.x artifacts.
3. All parameters and seeds are visible.
4. No interpretative language is used.
5. SQLite is not accessed directly.
6. The GUI is fully reproducible.

---

## 8. Deliverable

A **GUI Specification Document** that serves as:

- a contract for frontend implementation,
- a reference for GoAn-based code generation,
- a basis for GUI acceptance testing.

---

End of Task 6.

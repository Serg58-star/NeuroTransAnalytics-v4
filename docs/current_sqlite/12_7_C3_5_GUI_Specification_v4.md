# C3.5 — GUI Specification for C3.x Exploratory Results v4

## 1. Introduction

This document defines the GUI contract for the **Exploratory Results** screen in the NeuroTransAnalytics-v4 project. It specifies how C3.x exploratory artifacts are presented, ensuring architectural compliance with the C3.5 Visualization layer.

---

## 2. Screen: “Exploratory Results”

### 2.1 Component Layout

1. **Sidebar: Procedure & Artifact Selection**
   - **Procedure Tree**: Hierarchical list of exploratory procedures grouped by domain (e.g., "Domain I: Distribution Shape Analysis" -> "Multimodality Detection").
   - **Artifact List**: Filterable list of available precomputed results for the selected procedure, sorted by timestamp.

2. **Main Area: Visualization Panel**
   - Renders the selected artifact using a type-specific template.
   - Includes standard zoom, pan, and hover-inspect tools.

3. **Footer: Provenance & Compliance**
   - **Metadata Bar**: Displays algorithm version, computation timestamp, and random seed.
   - **Parameters Display**: Non-editable table of all input parameters used for the computation.
   - **Non-Interpretation Box**: Permanent display of the mandatory clause: *“This representation is exploratory and descriptive. It does not imply interpretation, inference, or evaluation.”*

---

## 3. Visualization Template Mappings

The GUI MUST map `C3.x` Result Types to these allowed templates:

| Result Type | Allowed Visual Templates | Prohibited Actions |
| :--- | :--- | :--- |
| `DistributionStructureResult` | Histograms (fixed bins), Density Curves, Modality Markers | Re-binning, Kernel Density re-estimation |
| `TemporalStructureResult` | Autocorrelograms, Time-Series plots with Change-Points | Window size adjustment, dynamic smoothing |
| `RegimeSequenceResult` | Segmented Timelines, State Color Bands | State merging, manual label modification |
| `EmbeddingResult` | 2D/3D Scatter Plots (fixed coords), Cluster Overlays | Re-embedding, axis re-scaling, point deletion |
| `DependencyStructureResult`| Heatmaps, Static Dependency Graphs, Partial Correlation Networks | Threshold tuning, recalculating coefficients |
| `InformationStructureResult`| Entropy Bar Charts, Complexity Profiles | Normalization changes, re-computation |
| `ScenarioSimilarityResult` | Dendrograms, Similarity Networks, Distance Matrices | Linkage method changes, dynamic clustering |

---

## 4. Interaction & Implementation Constraints

### 4.1 "Read-Only" Enforcement

- No interactive sliders for algorithm parameters (e.g., no "Perplexity" slider for t-SNE).
- No "Run" or "Recompute" buttons.
- GUI state must be derived entirely from the selected artifact.

### 4.2 Language Policy

- UI labels MUST use neutral, descriptive terms:
  - **YES**: "Visualizes", "Represents", "Coordinates", "Structure found".
  - **NO**: "Indicates", "Suggests", "Reveals", "Determines", "Normal/Abnormal".

### 4.3 Data Access

- The GUI MUST NOT access `neuro_data.db` directly.
- All data for visualization must be loaded from exported C3.x/C3.4 JSON or binary artifacts.

---

## 5. Acceptance Checklist

1. [ ] Can the user change any algorithm parameters from the UI? (Must be NO)
2. [ ] Are all random seeds and versions visible? (Must be YES)
3. [ ] Is the non-interpretation clause always visible? (Must be YES)
4. [ ] Does the UI use any inferential language? (Must be NO)
5. [ ] Is the visualization strictly a reflection of precomputed data? (Must be YES)

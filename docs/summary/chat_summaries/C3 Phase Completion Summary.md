# C3 Phase Completion Summary

**Project:** NeuroTransAnalytics-v4  
**Phase:** Real Dataset Research — C3 Stabilization  
**Scope:** ETL → Component → QC → Scenario → Visualization  
**Storage Format:** Parquet (engine="fastparquet")  
**Project Layout:** Canonical `src` structure  
**Status:** Stable, Deterministic, Observable  

---

## 1. Overview

This phase completed the full implementation and stabilization of the C3 computational subsystem using real production data (`neuro_data.db`).

All computation layers (C3.1–C3.5) are now:

- Deterministic
- Non-interpretative
- Architecturally isolated
- Observably rendered via GUI
- Persisted in canonical Parquet format

The derived data layer is fully restored and stabilized.

---

## 2. C3.1 — Real SQLite ETL (etl_v4.1.2)

### Characteristics

- Source: `neuro_data.db`
- Strict read-only mode
- 36 × 3 stimulus normalization → EventFrame
- Includes subject-level metadata:
  - `age`
  - `sex`
- Technical QC flag introduced
- Architectural invariant:

MIN_RT_MS = 135


### Dataset Statistics

- Sessions: 1,892
- Total Events: 204,336
- Technical QC flagged: 648 rows
- No row deletion at ETL level

### Output

`EventFrame` (in-memory only, passed downstream)

Status: Stable

---

## 3. C3.2 — Component Timing (component_v4.0.0)

### Canonical Definitions

ΔV1 = RT_Tst1(session_id, stimulus_index)
ΔV4 = RT_Tst2 − ΔV1
ΔV5_MT = RT_Tst3 − ΔV1


### Methodological Clarification

- ΔV1 equals baseline RT from Tst1.
- No tapping-test integration yet.
- ΔV1 naming preserved for forward compatibility.

### Properties

- Deterministic
- No aggregation
- No interpretation
- No mutation of RT values

Status: Stable

---

## 4. C3.3 — QC & Robust Aggregation (qc_aggregation_v4.0.0)

### QC Policy

- Uses `technical_qc_flag`
- No recomputation of QC
- No row deletion
- Exclusion only at aggregation stage

### Metrics

- Median
- MAD
- IQR

### Grouping Level

subject_id
session_id
test_type


### Valid Aggregated Sessions

~1,886 valid Tst1 sessions

Status: Stable

---

## 5. C3.4 — Scenario Engine (scenario_v4.0.0)

### Implemented Scenarios

- A0.0 — ΔV1 Baseline Stability
- A0.1 — ΔV1 Variability Profile

### Design Constraints

- No new calculations
- No thresholds
- No interpretation
- Pure structural mapping of C3.3 aggregates

### Export

data/derived/scenarios/A0_0.parquet
data/derived/scenarios/A0_1.parquet


Status: Stable

---

## 6. C3.5 — GUI Visualization (A0)

### Structural Improvements

- Canonical `src` layout migration completed
- Absolute path resolution using `pathlib`
- No computational calls from GUI

### Features

- Displays scenario tables
- Displays version and timestamp
- Mandatory disclaimer present
- No recomputation
- No hidden logic

Status: Stable

---

## 7. Parquet Restoration & Engine Stabilization (Task 23)

### Problem

- `pyarrow 19.0.0` caused silent crashes on Windows + Python 3.13.5.

### Resolution

- Canonical engine switched to:

fastparquet

- Explicit engine specification enforced:

engine="fastparquet"

- CSV fallback fully removed
- No dual-format storage
- Dependencies updated and documented

### Derived Layer Format

Parquet only


Architectural integrity restored.

---

## 8. Canonical Architecture (Post-Stabilization)

Pipeline:

→ ETL
→ Component Timing
→ QC & Aggregation
→ Scenario Engine
→ Parquet (fastparquet)
→ GUI


All transitions are:

- Deterministic
- Layer-isolated
- Explicit
- Non-interpretative

---

## 9. Architectural Invariants Established

1. ΔV1 equals Tst1 baseline (until tapping integration).
2. Derived layer uses Parquet only.
3. Engine explicitly fixed (`fastparquet`).
4. GUI performs zero computation.
5. Canonical `src` layout mandatory.
6. QC is applied only in C3.3.
7. C3.4 adds no new metrics.
8. CSV fallback prohibited.

---

## 10. System Status

| Layer | Status |
|--------|--------|
| C3.1 | Stable |
| C3.2 | Stable |
| C3.3 | Stable |
| C3.4 | Stable |
| C3.5 | Stable |
| Storage | Parquet (fastparquet) |
| Layout | Canonical src |

The C3 subsystem is now production-grade and fully observable.

---

## 11. Next Strategic Options

1. Implement A1 Scenarios
2. Develop C4 Interpretation Layer
3. Integrate Tapping-Test (future ΔV1 revision)
4. Add comparative scenario layers

---

## 12. Phase Conclusion

The C3 stabilization phase is complete.

The system has transitioned from:
- conceptual architecture
to:
- operational, stable, observable real-data computation.

This summary serves as the baseline context for the next project phase.

# NeuroTransAnalytics-v4  
## Phase Transition — Post C3 Stabilization

We are starting a new architectural phase of the project.

Before proceeding, use the following document as canonical baseline:

📄 C3 Phase Completion Summary  
(Location: /docs/architecture/C3_Phase_Completion_Summary.md)

This document defines:

- The finalized C3 architecture (C3.1–C3.5)
- Canonical ΔV1 definition
- QC policy
- Parquet restoration (engine="fastparquet")
- src layout as mandatory
- GUI computation isolation principle
- Established architectural invariants

The C3 subsystem is considered:

✔ Stable  
✔ Deterministic  
✔ Observable  
✔ Parquet-restored  
✔ Layout-canonical  

No refactoring of C3 layers is allowed unless explicitly approved.

---

## Current System State

Pipeline:

SQLite  
→ ETL  
→ Component Timing  
→ QC Aggregation  
→ Scenario Engine (A0)  
→ Parquet (fastparquet)  
→ GUI  

All scenario results are now observable via GUI.

---

## Architectural Guardrails for the Next Phase

1. Do not modify ΔV1 semantics.
2. Do not reintroduce CSV fallback.
3. Do not allow GUI-side computation.
4. Do not break src layout.
5. Preserve explicit Parquet engine.

---

## Strategic Decision Required

We now choose the next architectural direction:

A) Implement A1 scenario layer  
B) Develop C4 Interpretation layer  
C) Integrate Tapping-test (future ΔV1 revision)  
D) Expand Scenario comparative framework  
E) Other (explicitly defined)

Awaiting architectural direction.

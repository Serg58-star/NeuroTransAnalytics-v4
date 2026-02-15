# Task 23 — C3.4 / C3.5 Parquet Restoration & Engine Stabilization

**Project:** NeuroTransAnalytics-v4  
**Current Branch:** main  
**New Branch to create:** feature/task-23-parquet-restoration  
**Layers:**  
- C3.4 — Scenario Engine (Export)  
- C3.5 — Scenario Visualization (Load)  
**Executor:** Google Antigravity (GoAn)  
**Priority:** High  
**Type:** Format Stabilization (No Logic Changes)

---

## 1. Context

Due to environment instability (pyarrow crash), C3.4 export and C3.5 load were temporarily switched to CSV.

CSV mode is a fallback and **not canonical**.

Canonical derived-layer format must be:

Parquet


This task restores Parquet as the only supported format.

---

## 2. Objectives

1. Restore Parquet export in C3.4.
2. Fix Parquet engine instability.
3. Remove all CSV fallback logic.
4. Ensure stable Parquet loading in GUI.
5. Preserve canonical src-layout.
6. Do not modify computation logic.

---

## 3. Architectural Constraints

You MUST NOT:

- Modify ETL
- Modify ComponentTiming
- Modify QC logic
- Modify Scenario logic
- Add new metrics
- Change schema
- Change GUI logic beyond loader
- Introduce dual-format storage

Single canonical format only.

---

## 4. Root Cause Investigation (Mandatory)

Before implementation:

1. Identify why pyarrow failed.
2. Confirm installed versions:
   - pandas
   - pyarrow
3. Verify architecture compatibility:
   - Python version
   - 64-bit environment
4. Reproduce minimal Parquet write/read test:

```python
df.to_parquet("test.parquet", engine="pyarrow")
pd.read_parquet("test.parquet", engine="pyarrow")

Provide explanation of failure if it still occurs.

5. Engine Policy

Explicitly fix engine:

engine="pyarrow"

Do NOT rely on default resolution.

If pyarrow proves unstable:

Attempt fastparquet

Document reason

Choose one engine and freeze it

Final decision must be deterministic and documented.

6. C3.4 Export Requirements

Replace CSV export with:

df.to_parquet(path, engine="pyarrow", index=False)

Requirements:

No CSV generation

No dual export

Overwrite allowed

Schema consistent

Output path:

data/derived/scenarios/A0_0.parquet
data/derived/scenarios/A0_1.parquet

7. C3.5 Load Requirements

Replace CSV load with:

pd.read_parquet(path, engine="pyarrow")

Path resolution must remain absolute via:

Path(__file__).resolve().parents[3]

No relative string paths.

8. Remove CSV Fallback

You MUST:

Remove all .to_csv

Remove all .read_csv

Remove CSV path handling

Remove conditional format switching

No fallback mode allowed.

9. Validation Checklist

After restoration:

Export produces valid Parquet files.

GUI loads Parquet successfully.

Row count matches expected (≈1886).

No crash.

No CSV files in derived directory.

Full pipeline C3.1 → C3.5 works.

10. Dependency Freeze

Add explicit dependency to requirements:

pyarrow==<stable_version>

Document chosen version in:

docs/technical/Dependency_Notes.md

11. Definition of Done

Parquet fully restored

Engine fixed explicitly

CSV removed

GUI stable

src-layout intact

No regression in C3 pipeline

Commit message:

"Restore Parquet as canonical format; stabilize engine"

12. Deliverables

Provide:

Root cause explanation.

Engine decision rationale.

Version numbers.

Code diff summary.

Confirmation of GUI load success.

Confirmation CSV removed.

This task restores architectural integrity of the derived data layer.



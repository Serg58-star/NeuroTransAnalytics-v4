# Task 4 — Editorial Synchronization of C3.5 Visualization  
## NeuroTransAnalytics-v4 (Excel → SQLite)

---

## 1. Context

Tasks 1–3 have been completed and validated:

- Task 1: Data Contracts — SQLite fixed as canonical storage.
- Task 2: C2 Data Architecture — logical vs physical separation clarified.
- Task 3: C3 Computation & Pipelines — computation described as mechanical and non-interpretative.

The remaining documentation risk area before implementation is **C3.5 (Visualization)**.

Visualization is the most common source of architectural boundary violations:
- hidden computation in UI,
- implicit interpretation,
- coupling GUI behavior to analytical logic.

This task ensures that **visualization is strictly passive and read-only**.

---

## 2. Scope (STRICT)

### Files in scope (ONLY):

docs/12_5_C3_5_Visualization_v4.md


No other documentation files are included in this task.

---

## 3. Objective

Perform a **STRICTLY EDITORIAL synchronization** of the visualization documentation so that:

- visualization is described as a **passive presentation layer**,
- all computations are explicitly delegated to C3,
- interpretation (C4) is explicitly excluded,
- data is read from SQLite or precomputed outputs only.

This task is:
- ✅ editorial only,
- ❌ NOT a rewrite,
- ❌ NOT a redesign,
- ❌ NOT a UI/UX enhancement,
- ❌ NOT an interpretation layer.

---

## 4. Source of Truth

### Canonical References (READ-ONLY)

docs/current_sqlite/RT_PSI_Data_Contract_v4.md
docs/current_sqlite/11_0_C2_Data_Architecture_v4_Map.md
docs/current_sqlite/12_0_Карта_уровня_C3_Computation_&_Pipelines_v4.md


These documents define:
- what data exists,
- where it is stored,
- where and how it is computed.

Visualization must not contradict these boundaries.

---

## 5. Allowed Changes (ONLY)

You MAY:

- Replace outdated references to Excel or file-based outputs
  with references to SQLite-backed or precomputed results.
- Clarify that visualization:
  - reads data only,
  - does not transform or aggregate data,
  - does not trigger computation.
- Rephrase descriptions to emphasize:
  - read-only access,
  - passive rendering,
  - neutral presentation.
- Fix inconsistencies caused solely by the Excel → SQLite transition.

---

## 6. Forbidden Changes (CRITICAL)

You MUST NOT:

- Introduce computation, aggregation, filtering, or metric calculation in the GUI.
- Introduce interpretative or explanatory language
  (e.g. “indicates”, “suggests”, “reveals”, “means”).
- Describe visualization as making decisions or assessments.
- Move any C3 logic into the visualization layer.
- Add new visualization-driven metrics or derived values.
- Apply global search-and-replace or algorithmic mappings.

If a passage implies that the GUI:
- computes,
- evaluates,
- interprets,
- or influences results,

then:
- STOP
- ASK for confirmation.

---

## 7. Output Rules

### 7.1. Do NOT modify original files

Original files in `docs/` must remain unchanged.

---

### 7.2. Save synchronized version here

docs/current_sqlite/12_5_C3_5_Visualization_v4.md


---

## 8. Editorial Report (MANDATORY)

Provide a short report including:

- File name
- List of editorial changes (bullet points)
- Explicit confirmation:
  > “Visualization remains strictly read-only. No computation or interpretation was introduced.”

---

## 9. Architectural Validation

Before finalizing:

- Invoke the **architecture-guardian** skill.
- Confirm:
  - GUI never computes,
  - GUI never interprets,
  - GUI only renders precomputed data,
  - no C3 or C4 logic leaks into visualization.

If any architectural boundary risk is detected:
- STOP
- REPORT
- DO NOT proceed silently.

---

## 10. Working Mode

- Use **Planning mode**.
- Generate:
  - Task List
  - Implementation Plan
- Await explicit approval before execution.

---

End of Task 4.

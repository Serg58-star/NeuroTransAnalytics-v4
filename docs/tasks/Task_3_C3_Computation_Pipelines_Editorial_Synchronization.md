# Task 3 — Editorial Synchronization of C3 Computation & Pipelines  
## NeuroTransAnalytics-v4 (Excel → SQLite)

---

## 1. Context

Tasks 1 and 2 have been completed and validated:

- Task 1: Data Contracts — SQLite storage fixed as canonical.
- Task 2: C2 Data Architecture — logical vs physical separation clarified.

The remaining risk area is **C3 (Computation & Pipelines)**, where:
- legacy Excel-oriented assumptions,
- implicit interpretation,
- or GUI-related logic  
may still be present in documentation.

This task focuses on **editorial synchronization only**, ensuring that
C3 documentation accurately reflects:
- SQLite-based data access,
- computation as a neutral, mechanical process,
- strict separation from interpretation (C4).

---

## 2. Scope (STRICT)

### Files in scope (ONLY):

docs/12_0_Карта_уровня_C3_Computation_&_Pipelines_v4.md
docs/12_1_C3_1_ETL_Pipeline_v4.md
docs/12_2_C3_2_Component_Timing_Computation_v4.md
docs/12_3_C3_3_QC_and_Aggregation_v4.md
docs/12_4_C3_4_Scenario_Computation_v4.md


No other documentation files are included in this task.

---

## 3. Objective

Perform a **STRICTLY EDITORIAL synchronization** of C3 documentation so that:

- all references to data sources reflect SQLite (`neuro_data.db`),
- computation is described as deterministic and mechanical,
- no interpretative, inferential, or explanatory logic is implied.

This task is:
- ✅ editorial only,
- ❌ NOT a rewrite,
- ❌ NOT a redesign,
- ❌ NOT a methodological revision,
- ❌ NOT an interpretation layer.

---

## 4. Source of Truth

### Canonical References (READ-ONLY)

docs/current_sqlite/RT_PSI_Data_Contract_v4.md
docs/current_sqlite/Маппинг_ полей_исходные Excel-файлы_SQLite_база_ neuro_data_db.md
docs/current_sqlite/11_0_C2_Data_Architecture_v4_Map.md
docs/current_sqlite/11_1_C2_1_Data_Model_v4.md


These documents define:
- physical storage,
- data entities,
- boundaries between layers.

---

## 5. Allowed Changes (ONLY)

You MAY:

- Replace outdated references to Excel, spreadsheets, or file-based pipelines
  with SQLite-based descriptions **when referring to data access**.
- Clarify that C3 computations:
  - read data from SQLite,
  - apply deterministic algorithms,
  - write results back to SQLite or intermediate tables/files.
- Adjust wording to emphasize:
  - mechanical computation,
  - absence of interpretation,
  - absence of hypothesis evaluation.
- Fix inconsistencies caused solely by the Excel → SQLite transition.

---

## 6. Forbidden Changes (CRITICAL)

You MUST NOT:

- Introduce interpretation, inference, or hypothesis language
  (e.g. “indicates”, “suggests”, “reveals”, “explains”).
- Encode decision logic about subject state, cognitive condition, or meaning.
- Move computation responsibilities into GUI or visualization layers.
- Change or reinterpret research methodology.
- Add new metrics, indices, or derived constructs.
- Apply global search-and-replace or algorithmic mappings.

If a passage appears to cross into interpretation:
- STOP
- ASK for confirmation.

---

## 7. Output Rules

### 7.1. Do NOT modify original files

Original files in `docs/` must remain unchanged.

---

### 7.2. Save synchronized versions here

For each processed file:

docs/current_sqlite/<original_filename>

docs/12_1_C3_1_ETL_Pipeline_v4.md
→ docs/current_sqlite/12_1_C3_1_ETL_Pipeline_v4.md


---

## 8. Editorial Report (MANDATORY)

For EACH file, provide a short report:

- File name
- List of editorial changes (bullet points)
- Explicit confirmation:
  > “No computational logic was altered and no interpretative meaning was introduced.”

---

## 9. Architectural Validation

Before finalizing:

- Invoke the **architecture-guardian** skill.
- Confirm:
  - C3 remains purely computational,
  - no C4 interpretation leaks into C3,
  - GUI is not assigned any computational responsibility.

If any architectural risk is detected:
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

End of Task 3.

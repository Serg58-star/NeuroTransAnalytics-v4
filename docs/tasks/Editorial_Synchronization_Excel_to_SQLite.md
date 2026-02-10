# Task 1 — Editorial Synchronization of Data Contracts  
## NeuroTransAnalytics-v4 (Excel → SQLite)

---

## 1. Context

The project **NeuroTransAnalytics-v4** has transitioned its physical data storage  
from **Excel-based files** to a **SQLite database (`neuro_data.db`)**.

The documentation located in:

docs/data_contracts/


defines **data contracts**, field mappings, and storage assumptions used by:
- ETL pipelines,
- C3 computation,
- scenario processing.

These documents must be **editorially synchronized** to reflect SQLite as the canonical storage.

---

## 2. Scope (STRICT)

### Files in scope (ONLY):

docs/data_contracts/RT_PSI_Data_Contract_v4.md
docs/data_contracts/Маппинг_ полей_исходные Excel-файлы_SQLite_база_ neuro_data_db.md


No other files or directories are included in this task.

---

## 3. Objective

Perform a **STRICTLY EDITORIAL synchronization** of the data contract documents.

This task is:
- ✅ an editorial update,
- ❌ NOT a rewrite,
- ❌ NOT a methodological revision,
- ❌ NOT an architectural redesign.

The goal is to align terminology and references with the **SQLite-based storage**  
while preserving **exact semantic meaning**.

---

## 4. Source of Truth

### Semantic Reference (READ-ONLY)

docs/Consolidated documentation_in_v4/


Use these documents ONLY to:
- verify correct terminology,
- confirm intended meaning.

They must NOT be treated as rewrite targets or templates.

---

## 5. Allowed Changes (ONLY)

You MAY:

- Replace references to:
  - Excel files,
  - spreadsheets,
  - sheets  
  with SQLite equivalents **when referring to physical storage**.
- Update field names **only where a direct mapping already exists**.
- Clarify that `neuro_data.db` is the canonical storage.
- Fix outdated references caused solely by the Excel → SQLite transition.

---

## 6. Forbidden Changes (CRITICAL)

You MUST NOT:

- Change or reinterpret methodological meaning.
- Introduce new fields, metrics, or entities.
- Remove or add sections.
- Normalize or “improve” wording beyond storage alignment.
- Apply global or mechanical replacements.
- Infer mappings not explicitly defined.

If a passage is ambiguous:
- STOP
- ASK for confirmation.

---

## 7. Output Rules

### 7.1. Do NOT modify original files

Original files in `docs/data_contracts/` must remain unchanged.

---

### 7.2. Save synchronized versions here

For each processed file:

docs/current_sqlite/<original_filename>

Example:

docs/data_contracts/RT_PSI_Data_Contract_v4.md
→ docs/current_sqlite/RT_PSI_Data_Contract_v4.md


---

## 8. Editorial Report (MANDATORY)

For EACH file, provide a short report:

- File name
- List of editorial changes (bullet points)
- Explicit confirmation:
  > “No methodological or semantic changes were made.”

---

## 9. Architectural Validation

Before finalizing:

- Invoke the **architecture-guardian** skill.
- Confirm:
  - SQLite is referenced as canonical storage.
  - No interpretation logic is introduced.
  - No computation is implied.

If any architectural risk is detected:
- STOP
- REPORT
- DO NOT PROCEED silently.

---

## 10. Working Mode

- Use **Planning mode**.
- Generate:
  - Task List
  - Implementation Plan
- Await confirmation before execution if uncertainty arises.

---

End of Task 1.


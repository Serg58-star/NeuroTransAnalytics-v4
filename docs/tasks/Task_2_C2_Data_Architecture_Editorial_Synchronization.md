# Task 2 — Editorial Synchronization of C2 Data Architecture Documentation  
## NeuroTransAnalytics-v4 (Excel → SQLite)

---

## 1. Context

Task 1 (Data Contracts) has been successfully completed and validated.

The documents in:

docs/current_sqlite/

now define the **canonical physical data storage layer** for NeuroTransAnalytics-v4:
- SQLite database `neuro_data.db`
- canonical tables (`users`, `trials`, `metadata_*`)
- explicit legacy vs v4 separation

The next step is to align **C2-level documentation** (Data Architecture) with this
already-validated data contract layer.

---

## 2. Scope (STRICT)

### Files in scope (ONLY):

docs/11_0_C2_Data_Architecture_v4_Map.md
docs/11_1_C2_1_Data_Model_v4.md
docs/11_2_C2_2_Physical_Storage_Design.md


No other documentation files are included in this task.

---

## 3. Objective

Perform a **STRICTLY EDITORIAL synchronization** of C2 documentation so that:

- descriptions of data architecture,
- references to physical storage,
- mentions of data sources and persistence

are **fully consistent** with the already synchronized
`docs/current_sqlite/data_contracts`.

This task is:
- ✅ editorial only,
- ❌ NOT a rewrite,
- ❌ NOT a redesign,
- ❌ NOT a methodological revision.

---

## 4. Source of Truth

### Canonical Reference (READ-ONLY)

docs/current_sqlite/


In particular:
- `RT_PSI_Data_Contract_v4.md`
- `Маппинг_ полей_исходные Excel-файлы_SQLite_база_ neuro_data_db.md`

These documents define:
- what data exists,
- where it is stored,
- how legacy fields map to SQLite.

---

## 5. Allowed Changes (ONLY)

You MAY:

- Replace outdated references to:
  - Excel files,
  - spreadsheets,
  - file-based storage  
  with SQLite equivalents **when referring to physical storage**.
- Align descriptions of:
  - data entities,
  - tables,
  - persistence mechanisms  
  with the validated data contracts.
- Clarify that `neuro_data.db` is the canonical storage backend.
- Fix inconsistencies caused **solely** by the Excel → SQLite transition.

---

## 6. Forbidden Changes (CRITICAL)

You MUST NOT:

- Change architectural layer responsibilities.
- Introduce new entities, tables, or fields.
- Modify research logic or computation semantics.
- Add interpretation or analytical meaning.
- Apply global search-and-replace rules.
- Normalize or “improve” conceptual descriptions.

If a passage is ambiguous:
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


Example:
docs/11_1_C2_1_Data_Model_v4.md
→ docs/current_sqlite/11_1_C2_1_Data_Model_v4.md


---

## 8. Editorial Report (MANDATORY)

For EACH file, provide a short report:

- File name
- List of editorial changes (bullet points)
- Explicit confirmation:
  > “No architectural, methodological, or semantic changes were made.”

---

## 9. Architectural Validation

Before finalizing:

- Invoke the **architecture-guardian** skill.
- Confirm:
  - C2 remains descriptive, not computational.
  - Storage responsibility remains in C3.
  - Interpretation (C4) is not introduced.

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
- Await confirmation before execution if uncertainty arises.

---

End of Task 2.

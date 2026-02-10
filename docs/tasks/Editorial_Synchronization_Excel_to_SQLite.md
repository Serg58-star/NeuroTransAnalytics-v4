Файл: docs/tasks/Editorial_Synchronization_Excel_to_SQLite.md

Назначение: редакционная синхронизация документации
Исполнитель: Google Antigravity (GoAn)
Тип задачи: editorial-only (без изменения смысла)

# Editorial Synchronization of NeuroTransAnalytics-v4 Documentation  
## (Excel → SQLite)

---

## 1. Context

The project **NeuroTransAnalytics-v4** has transitioned its primary data source  
from **Excel-based files** to a **SQLite database (`neuro_data.db`)**.

A consolidated set of documents located in:

docs/Consolidated documentation_in_v4/

has already been **editorially adapted** to reflect this transition and represents the  
**current semantic and methodological state** of the project documentation.

However, the fragmented documentation located in:

docs/
docs/data_contracts/

still contains outdated references to Excel-based data sources and requires  
**editorial synchronization**.

---

## 2. Objective

Perform a **STRICTLY EDITORIAL synchronization** of documentation files.

This task is:
- ✅ an editorial update,
- ❌ NOT a rewrite,
- ❌ NOT a methodological revision,
- ❌ NOT an architectural redesign.

The goal is to align terminology and data-source references with the existing  
SQLite-based implementation **without changing meaning**.

---

## 3. Source of Truth

### Semantic / Methodological Reference (READ-ONLY)

docs/Consolidated documentation_in_v4/


These documents define:
- research logic,
- architectural meaning,
- interpretation boundaries.

---

### Target Files to Process

docs/
docs/data_contracts/


These files must be synchronized **against the consolidated documentation**.

---

## 4. Allowed Changes (ONLY)

You MAY perform the following changes:

- Replace references to **Excel files / sheets / tables**  
  with **SQLite database / tables**.
- Update terminology:
  - “Excel table” → “SQLite table”
  - “spreadsheet” → “database”
- Align descriptions of:
  - data flow,
  - storage,
  - ETL steps  
  with a SQLite-based backend.
- Fix outdated filenames, field names, or source references
  **only when required by the Excel → SQLite transition**.
- Apply minimal editorial corrections required for consistency.

---

## 5. Forbidden Changes (CRITICAL)

You MUST NOT:

- Change methodological meaning.
- Introduce new concepts or interpretations.
- Modify research logic or scenario definitions.
- Alter architectural layer responsibilities.
- Add or remove sections.
- Rephrase text beyond what is strictly required for data-source alignment.
- “Improve”, “clarify”, or “optimize” wording unless necessary for source correction.

If a change may affect meaning, **STOP and ASK for confirmation**.

---

## 6. Output Rules (VERY IMPORTANT)

### 6.1. Do NOT modify original files in place

Original files must remain unchanged.

---

### 6.2. Save edited versions to a new location

For each processed file:

- Preserve the original filename.
- Save the updated version to:

docs/current_sqlite/


Example:

docs/11_1_C2_1_Data_Model_v4.md
→ docs/current_sqlite/11_1_C2_1_Data_Model_v4.md

---

### 6.3. Legacy handling

Original (unchanged) files may later be archived to:

docs/legacy_excel/


Do NOT move or delete files automatically.

---

## 7. Verification & Reporting

For each processed file, provide a **short editorial report** including:

- File name
- List of changes performed (bullet points)
- Explicit confirmation:
  > “No methodological or semantic changes were made.”

---

## 8. Mandatory Architectural Check

Before finalizing any changes:

- Invoke the **architecture-guardian** skill.
- Ensure:
  - no interpretation logic is introduced,
  - no computation is implied in GUI or documentation,
  - SQLite remains the canonical storage.

If architectural or methodological ambiguity is detected:
- STOP
- REQUEST clarification

---

## 9. Working Mode Requirements

- Use **Planning mode**.
- Generate:
  - Task List
  - Implementation Plan
- Await confirmation before proceeding if uncertainty arises.

---

## 10. Success Criteria

The task is considered successful if:

- All processed documents are editor\-synchronized to SQLite.
- Original files remain intact.
- No semantic or methodological drift occurs.
- Editorial reports confirm the above.

---

End of task description.

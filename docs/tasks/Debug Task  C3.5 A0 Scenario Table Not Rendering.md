# Debug Task — C3.5 A0 Scenario Table Not Rendering

**Project:** NeuroTransAnalytics-v4  
**Layer:** C3.5 — Scenario Visualization  
**Branch:** main  
**Executor:** Google Antigravity (GoAn)  
**Priority:** High  
**Type:** Data Binding / Path Resolution Fix  
**Scope:** GUI Data Loading Only (No Computation Changes)

---

## 1. Problem Statement

GUI launches successfully.

Observed behavior:

- A0.0 screen loads.
- Disclaimer and version metadata display correctly.
- Central table renders but contains **no rows**.

C3 pipeline is confirmed operational.
Parquet files exist.

This indicates a **data loading or path resolution failure inside GUI layer.**

---

## 2. Constraints

You MUST NOT:

- Modify ETL
- Modify ComponentTiming
- Modify QC Aggregation
- Modify ScenarioEngine
- Recompute data in GUI
- Add new calculations
- Add temporary hardcoded values

This is strictly a visualization-layer issue.

---

## 3. Mandatory Diagnostics

### 3.1 Verify Working Directory

Insert temporary debug log inside ScenarioLoader:

```python
import os
print("CWD:", os.getcwd())

Expected:

.../NeuroTransAnalytics-v4

If not root — fix path handling.

3.2 Verify Parquet Existence at Runtime

Add:

from pathlib import Path

print("Scenario path exists:",
      Path("data/derived/scenarios/A0_0.parquet").exists())

If False → path resolution bug.

3.3 Verify Parquet Read

Add temporary debug:

import pandas as pd

df = pd.read_parquet("data/derived/scenarios/A0_0.parquet")
print("Rows loaded:", len(df))

If rows > 0 but GUI table empty → binding issue.

4. Most Likely Root Cause

After src migration, relative paths now resolve relative to:

src/gui/

Instead of project root.

Therefore:

data/derived/scenarios/...

resolves incorrectly.

5. Required Architectural Fix

All GUI data loading must use project-root absolute resolution.

Implement:

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[3]
SCENARIO_DIR = BASE_DIR / "data" / "derived" / "scenarios"

a0_path = SCENARIO_DIR / "A0_0.parquet"

DO NOT use relative string paths.

DO NOT rely on working directory.

6. Validate Data Binding

After loading DataFrame:

Confirm df.shape > 0

Confirm table model receives df

Confirm model rowCount() > 0

Confirm view.setModel() called after load

If DataFrame non-empty but table empty:

Debug QAbstractTableModel implementation

Verify data() method returns values

Verify rowCount and columnCount are correct

7. Verification Checklist

After fix:

A0.0 displays 1,886 rows (or expected count)

A0.1 displays same session count

No recomputation triggered

No ETL call from GUI

No additional imports from C3 layers

8. Definition of Done

GUI table populated

No path-related errors

No computation inside GUI

No architecture violations

Commit message:
"Fix scenario path resolution and GUI data binding (C3.5)"

9. Deliverables

Provide:

Explanation of root cause.

Code diff.

Confirmation of displayed row count.

Confirmation that no computational layers were modified.

This is a pure visualization-layer correction.
Do not modify C3.x.

# Refactor Task — Full Migration to Canonical src Layout

**Project:** NeuroTransAnalytics-v4  
**Branch:** main  
**Executor:** Google Antigravity (GoAn)  
**Priority:** High (Structural Consistency Fix)  
**Type:** Architectural Refactor (No Functional Changes)

---

## 1. Problem Statement

Current repository state mixes two layouts:

- legacy flat layout (`gui/`)
- canonical src layout (`src/gui/`)

This causes:

ModuleNotFoundError: No module named 'gui.scenario_viewer'


The project must migrate fully to canonical **src layout**.

No hybrid structure is allowed.

---

## 2. Target Architecture (Canonical)

Final structure must be:

NeuroTransAnalytics-v4/
│
├── main.py
├── src/
│ ├── init.py
│ ├── c3_core/
│ └── gui/
│ ├── init.py
│ └── scenario_viewer/
│ ├── init.py
│ ├── a0_views.py
│ └── scenario_viewer.py
│
├── data/
├── docs/
└── ...


All Python imports must begin with:

from src....


---

## 3. Required Actions

### 3.1 Update main.py

Replace:

```python
from gui.app import run_app

With:

from src.gui.app import run_app

3.2 Update ALL GUI Imports

Inside src/gui/:

Replace any import of form:

from gui....

With:

from src.gui....

Verify:

app.py

a0_views.py

scenario_viewer.py

table_model.py

any other GUI file

No relative imports to root gui are allowed.

3.3 Ensure Package Initialization

Confirm presence of:

src/__init__.py
src/gui/__init__.py
src/gui/scenario_viewer/__init__.py

Create empty files if missing.

3.4 Remove Legacy Root-Level gui Directory

If directory exists:

/gui

Remove it entirely from repository:

delete directory

remove from git

ensure no imports depend on it

This must not delete src/gui.

3.5 Do NOT Modify:

C3 computation layers

ScenarioEngine

Data logic

GUI functionality

Parquet export logic

This is structural-only refactor.

4. Validation Steps (Mandatory)

After refactor:

Run:

python main.py

Verify:

No ModuleNotFoundError

GUI loads A0 screens

Scenario data loads from parquet

No recomputation triggered from GUI

Verify imports resolve:

python -c "import src.gui.scenario_viewer"

Must not fail.

5. Definition of Done

All imports use src. prefix.

No legacy gui/ at root.

Application starts without module errors.

GUI displays A0 scenarios correctly.

No functional regression.

Commit message:
"Refactor to canonical src layout (structural only)"

6. Constraints

No logic changes.

No reformatting unrelated files.

No architectural redesign.

No feature additions.

This is a pure structural migration.

After completion, provide:

Updated tree structure

Confirmation of successful run

Confirmation that GUI loads A0 views.



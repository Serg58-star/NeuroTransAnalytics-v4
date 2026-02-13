# Task 12 — PySide6 Desktop Application Bootstrap

## Objective

Implement a fully runnable desktop GUI application using **PySide6** for the NeuroTransAnalytics-v4 project.

The application must:

- Launch via `main.py`
- Instantiate `QApplication`
- Create a `QMainWindow`
- Integrate the existing C3.5 Exploratory Results layer
- Render precomputed artifacts using Matplotlib (Qt backend)
- Preserve strict architectural separation (C2 / C3.x / C3.5)

The GUI must remain strictly read-only.

No computation logic may be introduced.

---

## Architectural Constraints (Mandatory)

The GUI layer must:

- NOT import `sqlite3`
- NOT import anything from `src/c2_data`
- NOT import exploratory procedure implementations (e.g., multimodality, change_point)
- NOT recompute statistics
- NOT modify artifact files
- NOT write to disk

The GUI must ONLY:

- Load persisted artifacts
- Use adapters for transformation
- Render already-computed data

---

## Scope

Create and/or modify the following:

# Task 12 — PySide6 Desktop Application Bootstrap

## Objective

Implement a fully runnable desktop GUI application using **PySide6** for the NeuroTransAnalytics-v4 project.

The application must:

- Launch via `main.py`
- Instantiate `QApplication`
- Create a `QMainWindow`
- Integrate the existing C3.5 Exploratory Results layer
- Render precomputed artifacts using Matplotlib (Qt backend)
- Preserve strict architectural separation (C2 / C3.x / C3.5)

The GUI must remain strictly read-only.

No computation logic may be introduced.

---

## Architectural Constraints (Mandatory)

The GUI layer must:

- NOT import `sqlite3`
- NOT import anything from `src/c2_data`
- NOT import exploratory procedure implementations (e.g., multimodality, change_point)
- NOT recompute statistics
- NOT modify artifact files
- NOT write to disk

The GUI must ONLY:

- Load persisted artifacts
- Use adapters for transformation
- Render already-computed data

---

## Scope

Create and/or modify the following:

main.py
src/app/main_window.py
gui/widgets/exploratory_widget.py
gui/widgets/matplotlib_canvas.py


Do NOT modify:

src/c2_data/
src/c3_core/
src/c3x_exploratory/


No changes to computation layers are allowed.

---

# 1. Install Dependencies

Ensure the environment contains:

- PySide6
- matplotlib

Install if missing.

---

# 2. Application Bootstrap

## main.py

Implement:

- QApplication initialization
- MainWindow instantiation
- Event loop execution

Structure:

- Define `main()` function
- Instantiate `QApplication`
- Create `MainWindow`
- Call `window.show()`
- Execute `app.exec()`
- Standard `if __name__ == "__main__":` guard

No logic beyond bootstrapping.

---

# 3. Main Window

## src/app/main_window.py

Implement:

- QMainWindow subclass
- Window title: `"NeuroTransAnalytics v4"`
- Minimum size: 1200x800
- Central widget set to `ExploratoryWidget`

No computation logic allowed.

---

# 4. Exploratory Widget

## gui/widgets/exploratory_widget.py

Responsibilities:

- Procedure selector (QComboBox)
- Artifact selector (QComboBox)
- Visualization panel (Matplotlib canvas)
- Provenance panel (QTextEdit, read-only)

Behavior:

1. Discover available procedures from:

artifacts/exploratory/


2. Populate procedure dropdown.

3. On procedure selection:
- List artifacts in that directory.
- Populate artifact dropdown.

4. On artifact selection:
- Load artifact via persistence layer.
- Pass artifact through existing exploratory adapters.
- Render plot via Matplotlib canvas.
- Display provenance (parameters, version, non-interpretation clause).

The widget must never recompute statistics.

---

# 5. Matplotlib Canvas

## gui/widgets/matplotlib_canvas.py

Use:

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure


Implement reusable canvas class:

- Create Figure
- Add single Axes
- Provide method to:
  - Clear axes
  - Plot provided data
  - Redraw canvas

Allowed plotting:

- Line plots
- Scatter plots
- Vertical lines (change points)
- Titles
- Legends

Forbidden:

- Any statistical computation
- Any parameter recalculation
- Any model fitting

---

# 6. Data Flow (Must Be Preserved)


Implement reusable canvas class:

- Create Figure
- Add single Axes
- Provide method to:
  - Clear axes
  - Plot provided data
  - Redraw canvas

Allowed plotting:

- Line plots
- Scatter plots
- Vertical lines (change points)
- Titles
- Legends

Forbidden:

- Any statistical computation
- Any parameter recalculation
- Any model fitting

---

# 6. Data Flow (Must Be Preserved)

artifacts/exploratory/*.json
↓
persistence.load_artifact()
↓
exploratory_adapters.prepare_for_plot()
↓
MplCanvas.render(data)


No other data flow allowed.

---

# 7. Error Handling

The GUI must:

- Gracefully handle empty artifact directory
- Handle corrupted JSON safely
- Show QMessageBox on load error
- Never crash due to missing files
- Never modify timestamps

---

# 8. UI Language Policy

All UI text must be strictly descriptive.

Allowed examples:

- "Detected peaks"
- "Change points"
- "Distribution density"

Forbidden language:

- suggest
- reveal
- diagnose
- indicates pathology
- implies

The non-interpretation clause must be visibly displayed for each artifact.

---

# 9. Verification Requirements

Before completion, verify:

- No forbidden imports
- GUI does not access SQLite
- GUI does not call computation procedures
- GUI does not write to disk
- Application launches via:


No other data flow allowed.

---

# 7. Error Handling

The GUI must:

- Gracefully handle empty artifact directory
- Handle corrupted JSON safely
- Show QMessageBox on load error
- Never crash due to missing files
- Never modify timestamps

---

# 8. UI Language Policy

All UI text must be strictly descriptive.

Allowed examples:

- "Detected peaks"
- "Change points"
- "Distribution density"

Forbidden language:

- suggest
- reveal
- diagnose
- indicates pathology
- implies

The non-interpretation clause must be visibly displayed for each artifact.

---

# 9. Verification Requirements

Before completion, verify:

- No forbidden imports
- GUI does not access SQLite
- GUI does not call computation procedures
- GUI does not write to disk
- Application launches via:

python main.py


---

# 10. Deliverables

After implementation provide:

1. List of created files.
2. Confirmation that application launches successfully.
3. Description of the main window layout.
4. Confirmation:

   > "GUI remains strictly read-only. No computation or interpretation logic introduced."

---

# Final Instruction

Switch to Planning Mode.
Generate Implementation Plan.
Wait for approval before coding.

# Task 13 — Real Matplotlib Rendering in PySide6

## Objective

Upgrade the PySide6 desktop GUI from placeholder visualization to real
Matplotlib-based rendering of exploratory artifacts.

The GUI must:

- Render multimodality (KDE + detected peaks)
- Render change-point time series (signal + detected change points)
- Remain strictly read-only
- Perform zero statistical computation
- Use only precomputed artifact data

No recomputation logic is allowed.

---

## Architectural Constraints (MANDATORY)

The GUI layer must:

- NOT import multimodality.py
- NOT import change_point.py
- NOT compute statistics
- NOT compute KDE
- NOT detect peaks
- NOT detect change points
- NOT access SQLite
- NOT write to disk

The GUI must ONLY:

- Load artifact via persistence
- Transform via exploratory_adapters
- Plot provided arrays

Any violation of this boundary is forbidden.

---

## Scope

Modify or implement:

gui/widgets/matplotlib_canvas.py
gui/widgets/exploratory_widget.py


Do NOT modify:

src/c3x_exploratory/
src/c3_core/
src/c2_data/


---

# 1. Matplotlib Canvas Implementation

## matplotlib_canvas.py

Implement reusable Qt-integrated canvas:

Use:

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure


Create class:

class MplCanvas(FigureCanvasQTAgg):


Requirements:

- Single Figure
- Single Axes
- Method clear()
- Method render_multimodality(data)
- Method render_change_point(data)
- Automatic redraw after plotting

Axes must be cleared before each new render.

No statistics allowed.

---

# 2. Multimodality Rendering

Given adapter output:

Expected fields:

- x_values
- density_values
- peak_positions

Render:

- Line plot (x vs density)
- Vertical lines at peak_positions
- Title: "Distribution Density"
- Legend: ["Density", "Detected Peaks"]

Do NOT compute peaks.
Only plot provided values.

---

# 3. Change-Point Rendering

Given adapter output:

Expected fields:

- time_index
- signal_values
- change_points

Render:

- Line plot (time_index vs signal)
- Vertical lines at change_points
- Title: "Time Series with Change Points"
- Legend: ["Signal", "Change Points"]

Do NOT compute change points.

---

# 4. Integration in exploratory_widget.py

Replace placeholder visualization block with:

- Instance of MplCanvas
- On artifact selection:
    - Detect artifact type
    - Call appropriate render_* method
    - Display provenance in separate panel

Ensure:

- Canvas resizes correctly
- No crashes when switching artifacts
- No crashes when artifact is malformed

---

# 5. Error Handling

If artifact lacks required fields:

- Show QMessageBox
- Do NOT crash
- Do NOT attempt fallback computation

---

# 6. Resize Stability

The Matplotlib canvas must:

- Expand with window resizing
- Not duplicate axes
- Not leak memory
- Not create multiple figures per selection

---

# 7. Verification Requirements

Before completion verify:

- GUI does not import computation modules
- No NumPy statistical functions used
- No peak detection in GUI
- No change-point detection in GUI
- No file writes performed

Test:

1. Switch between 5 artifacts repeatedly
2. Resize window
3. Switch procedure type
4. Confirm no crash
5. Confirm no console errors

---

# 8. Deliverables

Provide:

1. List of modified files
2. Confirmation that plots render correctly
3. Confirmation:

   > "GUI renders only precomputed data. No computation introduced."

4. Screenshot description of:
   - Multimodality plot
   - Change-point plot

---

# Final Instruction

Switch to Planning Mode.
Generate Implementation Plan.
Wait for approval before coding.

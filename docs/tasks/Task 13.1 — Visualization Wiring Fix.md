# Task 13.1 — Visualization Wiring Fix

## Objective

Fix the wiring between:

artifact → adapter → canvas rendering

Current symptom:
Matplotlib canvas displays empty axes (0–1 range) with no plotted data.

This indicates that:

- render_* methods may not be called
OR
- adapter functions not imported
OR
- incorrect function names
OR
- empty data passed to canvas

This task must NOT introduce computation logic.

---

## 1. Remove Unused Imports

File:
gui/widgets/matplotlib_canvas.py

Remove:

# Task 13.1 — Visualization Wiring Fix

## Objective

Fix the wiring between:

artifact → adapter → canvas rendering

Current symptom:
Matplotlib canvas displays empty axes (0–1 range) with no plotted data.

This indicates that:

- render_* methods may not be called
OR
- adapter functions not imported
OR
- incorrect function names
OR
- empty data passed to canvas

This task must NOT introduce computation logic.

---

## 1. Remove Unused Imports

File:
gui/widgets/matplotlib_canvas.py

Remove:

import numpy as np


It is unused and unnecessary.

---

## 2. Verify Adapter Imports

File:
gui/widgets/exploratory_widget.py

Ensure correct imports exist:


It is unused and unnecessary.

---

## 2. Verify Adapter Imports

File:
gui/widgets/exploratory_widget.py

Ensure correct imports exist:

from gui.adapters.exploratory_adapters import (
get_distribution_plot_data,
get_temporal_plot_data,
)


If missing — add them.

---

## 3. Validate Adapter Function Names

Confirm that:

- get_distribution_plot_data returns:
    x_values
    density_values
    peak_positions

- get_temporal_plot_data returns:
    time_index
    signal_values
    change_points

Ensure naming matches exactly what render_* expects.

If mismatch — align names.

---

## 4. Ensure render_* is Actually Called

In exploratory_widget.py verify:

if isinstance(artifact, DistributionStructureResult):
data = get_distribution_plot_data(artifact)
self.canvas.render_multimodality(data)
elif isinstance(artifact, TemporalStructureResult):
data = get_temporal_plot_data(artifact)
self.canvas.render_change_point(data)


Add temporary debug print before render call:

print("Rendering multimodality")
print("Rendering change point")


This is temporary diagnostic output.

---

## 5. Verify Non-Empty Data

Before calling render_* add:

print(len(data["x_values"]))
print(len(data["density_values"]))


Or equivalent for time series.

If lengths are zero — report problem.

---

## 6. Do NOT:

- Modify persistence
- Modify computation layer
- Add statistical logic
- Add fallback calculations

---

## 7. Deliverables

Provide:

1. List of changes made
2. Confirmation that render_* methods are called
3. Confirmation that arrays passed to canvas are non-empty
4. Confirmation that plot is now visible
5. Remove temporary debug prints before finalizing

---

End of Task 13.1

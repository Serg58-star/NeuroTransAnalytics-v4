# Task 11 — C3.5 GUI Integration (Read-Only Artifacts)
## NeuroTransAnalytics-v4
## Branch: feature/task-11-gui-integration

---

## 1. Objective

Integrate C3.x exploratory artifacts into the GUI layer (C3.5).

The GUI must:

- Read precomputed artifacts from artifacts/exploratory/
- Display results in a read-only manner
- Never compute statistics
- Never access SQLite
- Never modify artifacts

This task establishes the first operational bridge between C3.x and C3.5.

---

## 2. Scope

Modify only:

    gui/
    src/c35_visualization/

Do NOT modify:
    c3x_exploratory procedures
    persistence logic
    c2_data
    main branch

---

## 3. GUI Screen: Exploratory Results

Implement a new screen:

    gui/screens/exploratory_results.py

The screen must contain:

1. Procedure Selector
   - Dropdown listing available procedures
   - Based on folders in artifacts/exploratory/

2. Artifact List
   - List saved JSON files for selected procedure
   - Sorted by timestamp (newest first)

3. Visualization Panel
   - Display visualization depending on artifact type

4. Provenance Panel
   - Show:
       - procedure_version
       - input_parameters
       - timestamp
       - non_interpretation_clause

No editing allowed.

---

## 4. Visualization Rules

Strict template mapping:

DistributionStructureResult →
    - Histogram (raw distribution)
    - KDE curve overlay
    - Mark detected peaks

TemporalStructureResult →
    - Time-series plot
    - Overlay detected change points
    - Optional statistic curve (secondary axis)

No dynamic parameter adjustment.
No recomputation.
No statistical inference.

---

## 5. Data Flow

GUI must:

- Use load_artifact() from persistence layer
- Convert list fields to numpy arrays only inside visualization layer
- Never mutate loaded artifact

All rendering must depend only on artifact content.

---

## 6. Language Policy

UI text must use descriptive language only:

Use:
    "Detected peaks at indices..."
    "Detected change points..."

Never use:
    "indicates"
    "suggests"
    "reveals"
    "implies"

Non-interpretation clause must be visibly displayed.

---

## 7. Architecture Constraints

- No direct SQLite calls
- No cross-import to computation logic
- No calls to detection classes
- No recomputation on GUI interaction

GUI = Passive observer.

---

## 8. Deliverable

Working exploratory_results screen capable of:

- Listing saved artifacts
- Loading artifact
- Rendering appropriate visualization
- Displaying provenance metadata

---

End of Task 11

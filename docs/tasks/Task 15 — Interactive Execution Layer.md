# Task 15 — Interactive Execution Layer
Objective

Upgrade the GUI from a passive artifact viewer to an interactive research interface while preserving strict architectural boundaries.

The GUI must:

Allow parameter configuration per procedure

Trigger execution via Controller

Receive computed artifact

Persist artifact

Refresh artifact list automatically

Remain computation-free

The GUI must NOT:

Perform statistical calculations

Directly import or execute C3.x algorithms

Access SQLite

Interpret results

1. Architectural Model

Required flow:

GUI (Parameters + Run Button)
    ↓
Exploratory Controller
    ↓
C3.x Procedure (Multimodality / ChangePoint)
    ↓
Artifact Object
    ↓
Persistence Layer
    ↓
Saved JSON
    ↓
GUI refresh

GUI never computes.
Controller orchestrates.
C3.x computes.
Persistence saves.

2. GUI Parameter Panels

Each procedure must have a dynamic parameter panel.

2.1 MultimodalityDetection

Add the following controls:

bandwidth → QComboBox
Options: ["scott", "silverman"]

prominence_ratio → QDoubleSpinBox
Range: 0.01 – 0.5
Default: 0.05

n_grid → QSpinBox
Range: 50 – 500
Default: 100

2.2 ChangePointDetection

Add:

window_size → QSpinBox
Range: 5 – 200

threshold → QDoubleSpinBox
Range: 0.01 – 5.0

normalize → QCheckBox

search_radius → QSpinBox

3. Run Button

Add:

[ Run Procedure ]

Behavior:

Collect parameters from GUI

Pass parameter dict to Controller

Disable button during execution

Re-enable after completion

Automatically select newly created artifact

No threading required for now (procedures are lightweight).

4. Controller Implementation

Create:

src/c35_visualization/exploratory_controller.py

Responsibilities:

Validate parameter types

Call appropriate C3.x procedure

Call persistence.save_artifact()

Return artifact metadata

Controller is the ONLY bridge between GUI and C3.x.

GUI must not import C3.x modules directly.

5. Artifact Auto-Refresh

After successful run:

Re-scan artifacts folder

Update procedure dropdown if needed

Update artifact list

Auto-select newly created artifact

No manual refresh button required.

6. Non-Interpretation Block Refactor

Current large warning block must be redesigned.

Replace large beige block with:

Compact info panel

Neutral styling

Collapsible section (QGroupBox expandable)

Text must be concise:

“This procedure identifies structural features of the data.
It does not perform interpretation or diagnosis.”

This space is reserved for future C4 interpretative layer integration.

7. Strict Boundary Enforcement

The following must be verified:

GUI does not import multimodality.py or change_point.py

GUI only imports Controller

Controller imports C3.x

No statistical logic inside GUI

No direct SQLite access

8. UI Behavior Requirements

Parameter panel changes dynamically based on selected procedure

Run button only enabled when parameters valid

Errors shown via QMessageBox

No crashes on invalid inputs

9. Deliverables

Updated exploratory_results.py

New exploratory_controller.py

Updated parameter widgets

Refactored non-interpretation block

Working Run flow

Confirmation report including architecture compliance

10. Success Criteria

After completion:

User can modify parameters from GUI

User can click Run

New artifact appears automatically

Graph updates

No architectural violations

GUI remains computation-free

End of Task 15

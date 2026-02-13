# Task 13.2 — Root Entry Point Refactor
Objective

Refactor the desktop application bootstrap so that:

main.py in the project root becomes the single canonical entry point

gui/app.py can no longer be executed directly

artifact paths resolve correctly using project-root working directory

no temporary path hacks remain in the codebase

This task is purely architectural and must NOT introduce computation logic.

1. Architectural Goal

Current problem:

The GUI is being launched via:

gui/app.py

This causes the working directory to be:

<project_root>/gui/

Which breaks relative artifact paths:

artifacts/exploratory

Correct model:

<project_root>/main.py
    ↓
gui/app.py → run_app()

The project root must always be the runtime working directory.

2. Required Refactor
2.1 Modify gui/app.py
A. Remove direct execution capability

If this block exists:

if __name__ == "__main__":
    ...

It must be removed.

B. Introduce a callable entry function

Add:

def run_app():
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

There must be NO execution logic outside this function.

gui/app.py must behave as a pure module.

2.2 Implement canonical entry in main.py (project root)

Replace content of main.py with:

from gui.app import run_app

if __name__ == "__main__":
    run_app()

No other logic allowed.

3. Artifact Path Validation

After refactor, confirm:

Working directory is project root

artifacts/exploratory resolves correctly

No absolute path hacks

No Path(__file__) based root calculations

No temporary debug prints

We rely purely on correct entrypoint discipline.

4. Remove Temporary Workarounds

Search entire project for:

Hardcoded project-root calculations

Debug prints related to artifact path

Temporary diagnostic code

Remove them.

The system must work using clean relative paths:

artifacts/exploratory

5. Verification Checklist

GoAn must confirm:

python main.py launches GUI

Artifact list is populated (if JSON exists)

No import errors

No relative path issues

No execution block in gui/app.py

No architectural boundary violations

6. Architectural Constraints

Must preserve:

No GUI computation

No direct SQLite access in GUI

No C3.x imports in GUI layer

Persistence remains the only data access bridge

7. Deliverables

Updated gui/app.py

Updated main.py

Confirmation report

Explicit statement:

“gui/app.py can no longer be executed directly. main.py is the single canonical entry point.”

End of Task 13.2
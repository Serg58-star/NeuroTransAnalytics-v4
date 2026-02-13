# Task 12.1 — PySide6 Environment Synchronization & Launch Fix

## Context

The desktop application fails to launch with:

ModuleNotFoundError: No module named 'PySide6'

The application is executed via:

C:\NeuroTransAnalytics-v4\.venv\Scripts\python.exe

This indicates that PySide6 was installed in a different environment
and is missing inside the project's local virtual environment (.venv).

---

## Objective

Fix the Python environment so that:

- PySide6 is installed inside `.venv`
- matplotlib is installed inside `.venv`
- The GUI launches successfully via:
# Task 12.1 — PySide6 Environment Synchronization & Launch Fix

## Context

The desktop application fails to launch with:

ModuleNotFoundError: No module named 'PySide6'

The application is executed via:

C:\NeuroTransAnalytics-v4\.venv\Scripts\python.exe

This indicates that PySide6 was installed in a different environment
and is missing inside the project's local virtual environment (.venv).

---

## Objective

Fix the Python environment so that:

- PySide6 is installed inside `.venv`
- matplotlib is installed inside `.venv`
- The GUI launches successfully via:

.venv\Scripts\python gui\app.py

- A `requirements.txt` file is generated and committed

No manual user intervention required.

---

## Steps to Perform

### 1. Detect Python Executable

Confirm active interpreter:

C:\NeuroTransAnalytics-v4.venv\Scripts\python.exe


Ensure all installations use this interpreter.

---

### 2. Install Missing Dependencies Into .venv

Execute using project interpreter:

.venv\Scripts\python -m pip install --upgrade pip
.venv\Scripts\python -m pip install PySide6 matplotlib


Do NOT use global pip.

---

### 3. Validate Installation

Run:

.venv\Scripts\python -m pip list


Confirm presence of:

- PySide6
- PySide6-Addons
- PySide6-Essentials
- shiboken6
- matplotlib

---

### 4. Launch Verification

Attempt to run:

.venv\Scripts\python gui\app.py


Expected result:
- Main window appears
- No ModuleNotFoundError
- No DLL load failure

If DLL load failure occurs:
- Reinstall PySide6 cleanly
- Confirm matching Python architecture (64-bit)

---

### 5. Create requirements.txt

Generate dependency snapshot:

.venv\Scripts\python -m pip freeze > requirements.txt


Add file to repository.

---

### 6. Architectural Validation

Confirm:

- No code modifications were required
- Only environment correction performed
- No architecture changes introduced

---

## Deliverables

Provide:

1. Confirmation that GUI launches successfully.
2. Confirmation that requirements.txt was generated.
3. Output of pip list showing PySide6 inside .venv.
4. Explicit confirmation:

   > "Environment synchronized. GUI launches successfully using project .venv interpreter."

---

End of Task 12.1

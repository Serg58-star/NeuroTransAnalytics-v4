# Task 11.1 — GUI Stability & Boundary Audit
## NeuroTransAnalytics-v4
## Branch: feature/task-11-gui-integration

---

## 1. Objective

Perform a full architectural and runtime audit of the GUI integration (C3.5).

You must verify:

- GUI performs no computation
- GUI does not access SQLite
- GUI does not call exploratory procedures
- GUI does not mutate artifacts
- GUI is robust to invalid files
- GUI respects non-interpretation policy

If any violation is found:
STOP and report.
Do not silently fix.

---

## 2. Static Architecture Audit

Search for forbidden imports inside gui/ and src/c35_visualization/:

Forbidden:
- c3x_exploratory.multimodality
- c3x_exploratory.change_point
- sqlite
- c2_data
- direct numpy statistics beyond presentation

Allowed:
- persistence.load_artifact
- exploratory_adapters

Report:
- Any forbidden import
- Any computation beyond visualization transforms

---

## 3. Runtime Stability Tests

Automatically perform:

### Test A — Empty Folder

Simulate empty artifacts/exploratory/ directory.

GUI must:
- Not crash
- Show empty state gracefully

---

### Test B — Corrupted JSON

Create invalid JSON file inside a procedure folder.

GUI must:
- Catch error
- Continue running
- Not crash

---

### Test C — High Volume

Create 30–50 artifacts (mix of multimodality and change-point).

GUI must:
- List all
- Sort by timestamp
- Not freeze
- Not recompute anything

---

## 4. Artifact Integrity Test

Load artifact via GUI.

Verify:
- File content unchanged
- Timestamp unchanged
- Hash unchanged
- No file write occurred

Confirm no mutation of artifact data.

---

## 5. Non-Interpretation Language Audit

Scan GUI strings.

Forbidden words:
- suggest
- reveal
- imply
- significant
- abnormal
- diagnose
- infer

Allowed:
- detected
- identified
- index
- value
- count

Report any violation.

---

## 6. Boundary Validation

Ensure:

GUI never:
- calls detection classes
- triggers recomputation
- modifies parameters
- creates new artifacts

GUI must be strictly read-only.

---

## 7. Deliverable

Produce:

GUI Stability Report including:

- Architecture Compliance: PASS / FAIL
- Runtime Stability: PASS / FAIL
- Artifact Integrity: PASS / FAIL
- Language Policy: PASS / FAIL

If all PASS:
Recommend merge.

If any FAIL:
List exact violation and location.

---

End of Task 11.1

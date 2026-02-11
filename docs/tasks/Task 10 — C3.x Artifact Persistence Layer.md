# Task 10 — C3.x Artifact Persistence Layer
## NeuroTransAnalytics-v4
## Branch: feature/task-10-artifact-persistence

---

## 1. Objective

Implement a deterministic artifact persistence layer for C3.x exploratory procedures.

The persistence layer must:

- Save artifacts to artifacts/exploratory/
- Use structured JSON serialization
- Preserve full reproducibility metadata
- Avoid SQLite
- Avoid GUI logic
- Avoid recomputation

---

## 2. Scope

Create new module:

    src/c3x_exploratory/persistence.py

Do NOT modify existing procedures.

Minimal changes allowed in artifacts.py
ONLY if needed for serialization.

---

## 3. Artifact Storage Requirements

Artifacts must be saved as:

    artifacts/exploratory/{procedure_name}/{timestamp}_{hash}.json

Where:

- procedure_name = class name (e.g., ChangePointDetection)
- timestamp = ISO format without microseconds
- hash = short deterministic hash of input_parameters

Example:

    artifacts/exploratory/ChangePointDetection/
        2026-02-11T15-40-12_3f8a9b.json

---

## 4. Serialization Rules

Artifacts must be JSON-serializable.

Rules:

- numpy arrays → convert to list
- datetime → ISO string
- no binary formats
- no pickle
- no joblib

Reproducibility > performance.

---

## 5. Persistence API

Implement:

def save_artifact(artifact) -> str
def load_artifact(filepath) -> object

save_artifact must:

- create directories if needed
- compute parameter hash
- write JSON
- return filepath

load_artifact must:

- reconstruct artifact dataclass
- validate procedure_version exists
- validate required fields

---

## 6. Parameter Hash

Compute SHA256 over:

- sorted JSON of input_parameters

Use first 6 characters.

No randomness.

---

## 7. Integrity Requirements

- Loading saved artifact must reproduce identical field values.
- No silent type changes.
- No mutation of original artifact.

---

## 8. Architecture Constraints

- No imports from GUI
- No imports from SQLite
- No calls to detection logic
- Pure infrastructure

---

## 9. Deliverable

Working persistence module capable of:

- Saving Multimodality artifacts
- Saving ChangePoint artifacts
- Reloading both types correctly

---

End of Task 10

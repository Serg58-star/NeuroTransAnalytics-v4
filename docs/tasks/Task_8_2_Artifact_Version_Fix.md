# Task 8.2 — Artifact Version Fix
## NeuroTransAnalytics-v4

---

## 1. Context

In Multimodality v1.1.0 the procedure version is defined explicitly
inside multimodality.py:

    PROCEDURE_VERSION = "1.1.0"

However, DistributionStructureResult still defines a default value:

    procedure_version: str = "1.0.0"

This creates a potential version mismatch and violates the
single-source-of-truth principle.

---

## 2. Objective

Remove the default procedure_version value from
DistributionStructureResult to ensure that:

- version is always explicitly provided by the procedure,
- no silent fallback occurs,
- no version drift is possible.

---

## 3. Scope (STRICT)

Modify only:

    src/shared/artifacts.py

No other file must be changed.

---

## 4. Required Change

Replace:

    procedure_version: str = "1.0.0"

With one of the following (preferred option A):

Option A (preferred):
    procedure_version: str

Option B:
    procedure_version: str = ""

No default version value must remain.

---

## 5. Verification

Before completion:

- Confirm DistributionStructureResult requires explicit version assignment.
- Confirm MultimodalityDetection still passes PROCEDURE_VERSION.
- Confirm no other code relies on the old default.

---

## 6. Deliverable

Artifact definition aligned with single-source version control.

No new functionality introduced.

---

End of Task 8.2

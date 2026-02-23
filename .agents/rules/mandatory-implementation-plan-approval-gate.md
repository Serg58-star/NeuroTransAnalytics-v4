---
trigger: always_on
---

# Project Rule — Mandatory Implementation Plan Approval Gate

## NeuroTransAnalytics-v4 Governance Policy

---

# 1. Purpose

To prevent premature implementation and architectural drift,  
no development work may proceed without explicit approval of the current Implementation Plan.

This rule overrides any prior conceptual agreement.

---

# 2. Scope

This rule applies to:

- All new Tasks
- All Task extensions (e.g., 40.1 → 40.2 → 40.3)
- All refactors
- All new directories
- All new computational modules
- Any modification affecting:
  - Statistical logic
  - Geometry layer
  - Clinical translation layer
  - Core invariants

---

# 3. Approval Gate Definition

Before ANY code is written, the following must occur:

1. An Implementation Plan document is created (.md).
2. The plan is reviewed.
3. Explicit approval is given.
4. Approval is documented in writing.

Only after written approval may implementation begin.

Conceptual agreement in discussion does NOT constitute approval.

---

# 4. Definition of Explicit Approval

Approval must include:

- Clear statement: "Approved for implementation."
- Reference to specific Task number and version.
- Confirmation that architectural boundaries are respected.

Absence of objection ≠ approval.

---

# 5. Prohibited Actions Before Approval

GoAn must NOT:

- Create new modules
- Modify directory structure
- Introduce new files
- Refactor existing logic
- Add synthetic test scaffolding
- Begin implementation of described functions

Even if:

- Mathematical logic seems finalized
- Corrections appear minor
- Prior versions were previously approved

Every iteration requires renewed approval.

---

# 6. Iterative Version Lock

Each Implementation Plan must include:

- Version tag (e.g., v1, v1.1, v2)
- Date
- Explicit delta from previous version

Implementation must reference the exact approved version.

No silent modifications allowed.

---

# 7. Architectural Safety Clause

If at any point:

- New mathematical assumptions are introduced
- Statistical thresholds are changed
- Decision logic hierarchy is modified

A new Implementation Plan must be drafted and approved.

---

# 8. Enforcement Principle

The development flow is:

Specification  
→ Implementation Plan  
→ Explicit Approval  
→ Implementation  
→ Validation  
→ Closure  

Skipping steps invalidates the task.

---

# 9. Current Status

This rule becomes active immediately.

All future Tasks (including Task 40.x series) must comply.

---

Status: Active Governance Rule

---
name: architecture-boundary-guard
description: Enforces strict architectural boundaries between C2, C3, C3.x, C3.5, and GUI layers. Triggers on code creation, imports, or cross-layer references.
---

# Architecture Boundary Guard

This skill enforces the architectural invariants of NeuroTransAnalytics-v4
at the filesystem and code level.

## When to use this skill
- When creating or modifying `.py` files.
- When adding imports.
- When introducing new modules or packages.

## Architectural Rules

### Layer Responsibilities

- **C2 (`src/c2_data`)**
  - Data access abstractions only.
  - No computation.
  - No exploratory logic.

- **C3 (`src/c3_core`)**
  - Deterministic core computation.
  - No exploratory procedures.
  - No GUI references.

- **C3.x (`src/c3x_exploratory`)**
  - Exploratory computation only.
  - No SQLite access.
  - No GUI code.
  - No interpretation.

- **C3.5 (`src/c35_visualization`)**
  - Visualization adapters only.
  - No computation.
  - No exploratory logic.

- **GUI (`gui/`)**
  - UI components only.
  - No computation.
  - No database access.
  - No exploratory logic.

## Forbidden Actions

- Importing C3.x from GUI.
- Importing GUI modules into C3 or C3.x.
- Performing calculations inside visualization or GUI.
- Accessing SQLite outside C2.
- Mixing exploratory and core computation logic.

## Enforcement

If a violation is detected:
- STOP immediately.
- Report the violation.
- Do NOT attempt to auto-fix silently.

This skill has absolute priority.

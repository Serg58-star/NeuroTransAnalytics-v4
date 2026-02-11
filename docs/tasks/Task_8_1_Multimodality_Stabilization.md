# Task 8.1 — Stabilization Patch (Multimodality v1.1)
## NeuroTransAnalytics-v4

---

## 1. Context

The initial implementation of C3.x Multimodality Detection (Task 8)
is functionally correct and architecture-compliant.

This task introduces stabilization improvements to:

- strengthen reproducibility,
- formalize hyperparameter control,
- eliminate silent defaults,
- reduce risk of version drift.

This task is a refinement only.
No new functionality is introduced.

---

## 2. Objective

Upgrade Multimodality Detection from v1.0.0 to v1.1.0 by:

1. Making peak detection prominence an explicit parameter.
2. Explicitly defining KDE bandwidth method.
3. Removing duplicated version definitions.
4. Ensuring artifact reproducibility completeness.

---

## 3. Scope (STRICT)

### Included

- Modification of multimodality.py
- Minor adjustment to artifacts.py (if required)

### Excluded

- No new exploratory logic
- No new synthetic generators
- No GUI changes
- No database access

---

## 4. Required Modifications

---

## 4.1 Explicit Peak Prominence Parameter

### Current State
Prominence ratio (0.05) is hard-coded inside `find_peaks`.

### Required Change

In `MultimodalityDetection.__init__`:

Add parameter:

```python
prominence_ratio: float = 0.05

Store in:

self.parameters["prominence_ratio"]

Modify peak detection:

peak_indices, _ = signal.find_peaks(
    density,
    prominence=max_density * self.parameters["prominence_ratio"]
)

4.2 Explicit KDE Bandwidth Method
Current Risk

bw_method=None relies on implicit SciPy default.

Required Change

Set explicit default:

bandwidth: str | float = "scott"

Store explicitly in parameters.

Do NOT leave bandwidth undefined.

4.3 Single Source of Version Definition

Remove duplicated version definitions.

Procedure version MUST be defined in one place only:

PROCEDURE_VERSION = "1.1.0"

Artifact must receive:

procedure_version=PROCEDURE_VERSION

Do NOT store version separately in parameters.

4.4 Artifact Completeness Check

Ensure artifact stores:

number_of_modes

density_curve

density_grid

detected_peaks

input_parameters (including prominence_ratio and bandwidth)

seed

procedure_version

timestamp

All hyperparameters must be present.

No implicit values allowed.

5. Reproducibility Validation

Before completion:

Confirm same seed + same parameters produce identical number_of_modes.

Confirm artifact contains all relevant parameters.

Confirm no hidden defaults remain.

6. Non-Interpretation Integrity

Verify non-interpretation clause remains unchanged.

No new descriptive or inferential language added.

7. Deliverable

MultimodalityDetection v1.1.0

Fully reproducible

Hyperparameter-explicit

Version-consistent

Architecture-compliant

End of Task 8.1

# Task 9.1 — Change-Point Stabilization Patch (v1.1.0)
## NeuroTransAnalytics-v4
## Branch: feature/task-9-change-point

---

## 1. Context

The initial implementation of Change-Point Detection (v1.0.0)
is functionally correct and architecture-compliant.

This task introduces stabilization improvements to:

- improve robustness,
- strengthen reproducibility,
- remove implicit design assumptions,
- reduce false detections in scaled data.

No new exploratory functionality is introduced.

---

## 2. Objective

Upgrade ChangePointDetection from v1.0.0 to v1.1.0 by:

1. Adding validation to synthetic generator.
2. Introducing optional scale normalization.
3. Making search_radius explicit.
4. Improving parameter transparency.
5. Preserving strict non-interpretation policy.

---

## 3. Scope (STRICT)

Modify only:

    src/c3x_exploratory/change_point.py
    src/c3x_exploratory/synthetic_time_series.py

Do NOT modify other procedures.
Do NOT modify multimodality.
Do NOT modify GUI.
Do NOT touch main branch.

---

## 4. Required Changes

---

## 4.1 Synthetic Generator Validation

In synthetic_time_series.py:

Add explicit validation:

- Ensure all change_points:
    - are >= 0
    - are < n_samples
    - are strictly increasing
- Raise ValueError if invalid.

This prevents silent segmentation errors.

---

## 4.2 Explicit search_radius Parameter

In ChangePointDetection.__init__:

Add parameter:

    search_radius: int | None = None

If None:
    search_radius = window_size // 2

Store explicitly in parameters.

Remove implicit derivation inside detection loop.

---

## 4.3 Optional Normalization

Add parameter:

    normalize: bool = False

If True:

    statistic_curve = statistic_curve / np.std(data)

Store normalize flag in input_parameters.

This makes threshold scale-aware.

Default must remain deterministic and backward-compatible.

---

## 4.4 Version Update

Set:

    PROCEDURE_VERSION = "1.1.0"

Ensure artifact receives explicit version.

No default version allowed.

---

## 4.5 Parameter Completeness

Ensure artifact.input_parameters includes:

- window_size
- threshold
- minimum_segment_length
- search_radius
- normalize

No implicit hyperparameters allowed.

---

## 5. Reproducibility Validation

Before completion:

- Same seed + same parameters → identical output.
- Different normalize values produce predictable differences.
- No real data access introduced.
- No cross-layer imports introduced.

---

## 6. Non-Interpretation Integrity

Non-interpretation clause must remain unchanged.

No inferential language added.

---

## 7. Deliverable

Stabilized ChangePointDetection v1.1.0

- Explicit hyperparameters
- Validation hardened
- Scale-aware option
- Architecture-compliant

---

End of Task 9.1

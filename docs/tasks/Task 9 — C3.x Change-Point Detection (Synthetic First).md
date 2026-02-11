We are working in branch: feature/task-9-change-point.
All changes must remain inside this branch.
Do not modify main.
Do not touch other procedures.

# Task 9 — C3.x Change-Point Detection (Synthetic First)

## 1. Objective

Implement a deterministic change-point detection procedure
for 1D synthetic time-series data.

The procedure must:

- detect structural mean shifts,
- be fully reproducible,
- contain explicit hyperparameters,
- produce a structured artifact,
- contain no interpretation,
- access no real data.

---

## 2. Files to Create

Inside:

    src/c3x_exploratory/

Create:

    change_point.py
    synthetic_time_series.py

If needed, extend:

    src/shared/artifacts.py

Do NOT modify other exploratory procedures.

---

## 3. Synthetic Generator Requirements

File: synthetic_time_series.py

Implement:

def generate_piecewise_series(
    n_samples: int,
    change_points: list[int],
    means: list[float],
    std: float,
    seed: int
) -> np.ndarray:

Requirements:

- deterministic RNG (np.random.default_rng(seed))
- piecewise constant segments
- explicit parameter validation
- no hidden randomness
- no real data

---

## 4. Change-Point Detection

File: change_point.py

Define:

PROCEDURE_VERSION = "1.0.0"

Class:

ChangePointDetection

Parameters must include:

- window_size: int
- threshold: float
- minimum_segment_length: int

No implicit defaults allowed beyond constructor signature.

---

## 5. Detection Logic (Deterministic)

Implement simple rolling mean difference:

1. For each t:
   compute mean(data[t-window:t]) and mean(data[t:t+window])
2. Compute absolute difference
3. If difference > threshold → candidate change point
4. Enforce minimum_segment_length

Store:

- statistic_curve (difference values)
- detected_change_points (indices)

No p-values.
No inference.
No probabilistic interpretation.

---

## 6. Artifact Definition

Add new class:

TemporalStructureResult

Fields:

- detected_change_points
- statistic_curve
- input_parameters
- seed
- procedure_version
- timestamp
- non_interpretation_clause

No default version.
No interpretation language.

---

## 7. Non-Interpretation Clause

Must include:

"This procedure identifies structural changes in time-series data.
It is exploratory and descriptive, and does not imply interpretation
or evaluation."

---

## 8. Reproducibility Validation

Before completion:

- Same seed + same parameters → identical change points
- All parameters stored in artifact
- No hidden randomness
- No SQLite imports

If violations detected:
STOP and report.

---

## 9. Deliverable

Working change-point detection module
operating strictly on synthetic time-series.

# Stage G — Legacy Stimulus Structure Investigation

**Task Package for GoAn**

**Project:** NeuroTransAnalytics v4
**Stage:** G — Stimulus Generator Architecture
**Purpose:** Extract latent structural properties of the legacy stimulus system to inform the design of **Stimulus Generator v5**.

---

# 1. Objective

The legacy testing system was manually designed and may contain **hidden structural properties** affecting neural response measurements.

The purpose of this task package is to identify **measurable structural characteristics** of the legacy stimulus sequence that could influence:

* perceptual contrast
* channel adaptation
* context dynamics
* temporal readiness

These properties will inform the **Stimulus Generator v5 architecture**.

All analyses must rely strictly on **empirical computation**, not theoretical speculation.

---

# 2. Data Sources

Primary inputs:

```
core/test_metadata.py
codebook_for_SZR.xlsx
```

Relevant variables:

```
stimulus_index
test_type
position
color
psi
context triples
ΔV4
ΔV5
reaction_time
```

Context triples must be reconstructed exactly as used in the legacy system.

---

# 3. Task 1 — Positional Color Distribution

## Goal

Determine whether color distribution across spatial positions is uniform.

Hypothesis:

```
P(color | position)
```

may be biased.

---

## Required computations

Compute frequencies:

```
P(red | left)
P(red | center)
P(red | right)

P(green | left)
P(green | center)
P(green | right)

P(blue | left)
P(blue | center)
P(blue | right)
```

---

## Statistical test

Perform:

```
Chi-square test for independence
```

---

## Deliverables

1. Probability table
2. Chi-square statistics
3. Conclusion:

```
uniform / biased
```

---

# 4. Task 2 — ContextTriple Sequence Structure

## Goal

Determine whether the sequence of context triples is random or structured.

---

## Required analyses

1. Transition matrix

```
P(triple_j | triple_i)
```

2. Autocorrelation of context sequence

```
lag = 1..10
```

3. Run-length distributions for:

```
blue-dominant triples
green-dominant triples
```

---

## Deliverables

Identify whether:

```
slow context dynamics
```

exists.

---

# 5. Task 3 — ContextTriple vs PSI

## Goal

Test whether PSI values correlate with specific context triples.

---

## Required computation

```
P(ContextTriple | PSI)
```

for each PSI level.

---

## Statistics

```
Mutual Information
Chi-square independence test
```

---

## Deliverables

Conclusion:

```
independent / structured relationship
```

---

# 6. Task 4 — Color Balance Trajectory

## Goal

Investigate temporal dynamics of channel activation across stimulus sequence.

---

## Procedure

For each stimulus_index compute color counts in a sliding window of previous context triples.

Suggested window sizes:

```
N = 3
N = 5
N = 7
```

Compute:

```
blue_count
green_count
red_count
```

---

## Deliverables

Determine whether:

```
P/K channel balance drift
```

exists across stimulus sequence.

---

# 7. Task 5 — Channel Balance Map

## Goal

Map context triples into channel activation space.

Each triple must be transformed into:

```
P = number_of_green
K = number_of_blue
R = number_of_red
```

---

## Analysis

For each triple group compute:

```
median ΔV4
median ΔV5
```

---

## Deliverables

Test relationship:

```
ΔV ~ channel_balance
```

---

# 8. Task 6 — Position-weighted Channel Model

## Goal

Evaluate whether central position contributes stronger perceptual weight.

---

## Model

```
activation =
wL * channel(left)
+
wC * channel(center)
+
wR * channel(right)
```

Where:

```
wC > wL
wC > wR
```

---

## Deliverables

Determine whether weighted channel model explains additional variance in:

```
ΔV
```

---

# 9. Task 7 — Context Complexity Index

## Goal

Quantify perceptual complexity of context triples.

---

## Metric

Compute Shannon entropy for each triple:

```
entropy(triple)
```

Examples:

```
ЖЖЖ → low entropy
СЖЖ → medium entropy
СЖК → high entropy
```

---

## Analysis

Test:

```
ΔV ~ context_entropy
```

---

# 10. Task 8 — PSI–Context Interaction

## Goal

Investigate interaction effects between PSI and context triples.

---

## Model

```
ΔV = f(PSI, ContextTriple)
```

---

## Required test

Two-way interaction analysis.

---

## Deliverables

Determine presence of:

```
PSI × Context interaction
```

---

# 11. Task 9 — Stimulus Index Drift

## Goal

Check whether stimulus properties drift during the test.

---

## Procedure

Divide stimulus sequence into:

```
early block
mid block
late block
```

Compare distributions:

```
ContextTriple
PSI
color distribution
```

---

## Deliverables

Identify:

```
protocol drift / stable distribution
```

---

# 12. Task 10 — Perceptual Contrast Index

## Goal

Compute perceptual contrast of stimuli relative to background.

---

## Known RGB values

```
red   = (254,0,0)
green = (10,222,16)
blue  = (6,0,254)

background = (43,149,255)
```

---

## Procedure

Convert colors to CIELAB space.

Compute:

```
ΔE(color, background)
```

---

## For each triple

Compute:

```
contrast_sum
```

---

## Analysis

Test relationship:

```
ΔV ~ perceptual_contrast
```

---

# 13. Output Requirements

All results must be saved in:

```
docs/audit_legacy/stage_G/
```

Each task must produce:

```
analysis report (.md)
tables (.csv)
figures (.png)
```

---

# 14. Final Deliverable

GoAn must produce a consolidated report:

```
Stage_G_Legacy_Stimulus_Structure_Report.md
```

This report will provide empirical evidence for:

* stimulus structure
* channel dynamics
* contextual influence

and will directly inform the architecture of **Stimulus Generator v5**.

---

**End of Task Package**

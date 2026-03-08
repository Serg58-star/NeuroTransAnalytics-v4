# Task_6_Stage-L Reconstruction
## NeuroTransAnalytics v4
### Legacy Runtime Reconstruction with Robust Statistics (Median + MAD)

Status: Implementation specification  
Executor: GoAn  
Stage: L (Legacy Reconstruction Layer)

---

# 1. Purpose

Stage-L reconstructs the behaviour of the historical Visual Reaction Time testing system.

The objective is to extract deterministic behavioural patterns embedded in the legacy runtime logic and transform them into analyzable structures compatible with the NeuroTransAnalytics v4 architecture.

The reconstruction must be **behaviourally faithful**, but **statistically modernized**.

---

# 2. Mandatory Statistical Rule

All statistical estimations in Stage-L MUST follow the project robust statistics standard.

The following rule is mandatory:

Only the following statistics are permitted:

- **Median**
- **MAD (Median Absolute Deviation)**

The following statistics are **strictly prohibited**:

- Mean
- Standard Deviation
- Coefficient of Variation
- Any derivative metrics based on mean or SD

The purpose of this restriction:

- ensure stability on small samples
- avoid sensitivity to outliers
- remove ambiguity in metric selection
- simplify analytical reproducibility

---

# 3. Historical Runtime Context

The legacy system:

- generated deterministic stimulus sequences
- captured exactly **36 valid reactions**
- discarded premature and late responses
- repeated trials until valid responses accumulated

Legacy algorithms used **Mean + SD + CV thresholds**.

These must be **reconstructed but replaced by Median + MAD equivalents**.

The behavioural logic of the system must be preserved.

---

# 4. Stage-L Input Sources

All reconstruction must rely exclusively on legacy documentation indexed in:

LEGACY_ANALYSIS_CONTEXT_INDEX.md :contentReference[oaicite:1]{index=1}

Primary source categories include:

- stimulus configuration files
- runtime algorithm description
- Delphi source code extracts
- result processing logic
- config parameter sets

---

# 5. Reconstruction Scope

Stage-L must reconstruct the following aspects:

1. stimulus design matrix
2. trial structure
3. PSI scheduling
4. response validation logic
5. outlier filtering logic
6. session completion rules
7. derived reaction-time vectors

---

# 6. Reconstruction Tasks

---

# Task L-1  
## Reconstruct Trial Structure

Goal:

Recreate the exact structure of each test session.

Requirements:

- warmup phase reconstruction
- main trial loop reconstruction
- 36 valid trials rule
- deterministic trial order

Output:

TrialStructure schema.

---

# Task L-2  
## Reconstruct Stimulus Event Matrix

Goal:

Extract the full deterministic stimulus matrix used by the legacy program.

Required fields:

- trial index
- PSI
- stimulus color
- spatial position
- stimulus pattern
- masking pattern

Output:

StimulusDesignMatrix.

---

# Task L-3  
## Reconstruct Response Classification Logic

Goal:

Reproduce legacy response validation rules.

Rules:

Valid reaction:

135 ms ≤ RT ≤ 2000 ms

Invalid reactions:

Premature:
RT < 135 ms

Late / timeout:
RT > 2000 ms

Output:

ResponseClassification model.

---

# Task L-4  
## Replace Legacy CV-Filtering with Robust Filtering

Legacy behaviour:

The historical system rejected trials when

CV = SD / Mean exceeded threshold.

This behaviour must be **reconstructed conceptually but implemented using robust statistics**.

New rule:

Outlier detection uses:

MAD-based deviation.

Definition:

Robust deviation score:

|RT − Median(RT)| / MAD(RT)

A reaction is considered unstable when:

RobustDeviation > Threshold

Threshold must be configurable.

Recommended default:

3.5 MAD

Output:

RobustOutlierFilter specification.

---

# Task L-5  
## Reconstruct Valid Reaction Vector

Goal:

Reconstruct the vector of valid RT values per test.

Requirements:

- exactly 36 valid reactions
- preserve chronological order
- record discarded trials

Output:

RTVector[36].

---

# Task L-6  
## Implement Robust Session Stability Check

Legacy runtime used CV stabilization.

Stage-L must replace this mechanism with:

Median/MAD stability control.

Procedure:

1. Compute median(RTVector)
2. Compute MAD(RTVector)
3. Evaluate deviation of each RT

If excessive deviations occur:

mark session as unstable.

Output:

SessionStabilityFlag.

---

# Task L-7  
## Extract Reaction Time Distribution Pack

Goal:

Generate distribution descriptors required by downstream analysis.

Mandatory metrics:

median_rt

mad_rt

Additional derived metrics permitted:

- IQR
- percentile distribution

Forbidden metrics:

- mean
- SD
- CV

Output:

DistributionPack.

---

# Task L-8  
## Reconstruct Error Metrics

Errors must be reconstructed exactly as in legacy logic.

Required counts:

- early reactions
- late reactions
- repeated trials

Output:

ErrorMetrics structure.

---

# Task L-9  
## Build Stage-L Session Artifact

Goal:

Produce a unified reconstruction artifact.

Artifact structure:

StageLSessionArtifact:

- session_id
- test_type
- stimulus_matrix_reference
- RTVector
- median_rt
- mad_rt
- error_counts
- stability_flag

---

# Task L-10  
## Document Reconstruction Algorithms

Goal:

Produce a technical specification of all reconstructed algorithms.

The document must include:

- filtering algorithm
- deviation thresholds
- RT extraction logic
- session completion rules

Output:

Stage_L_Reconstruction_Algorithms.md

---

# 7. Output Layer

Stage-L produces datasets compatible with the NeuroTransAnalytics v4 architecture.

Primary outputs:

- StimulusDesignMatrix
- RTVector
- DistributionPack
- ErrorMetrics
- StageLSessionArtifact

These outputs will be used by:

C3.2 Component Timing Computation  
Scenario Engine (C3.4)

---

# 8. Implementation Constraints

The following constraints are mandatory:

1. no modification of raw legacy data
2. deterministic reconstruction
3. full reproducibility
4. version tagging of algorithms
5. strict use of median and MAD statistics

---

# 9. Completion Criteria

Stage-L reconstruction is considered complete when:

- all legacy runtime behaviours are reproduced
- robust statistical replacements are implemented
- outputs are compatible with v4 data model
- reconstruction algorithms are documented

---
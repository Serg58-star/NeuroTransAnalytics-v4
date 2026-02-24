# Task 44.2 — Amendment to Implementation Plan (Frozen Geometry Enforcement)
## Stage 9C Population-Level Longitudinal Geometry Audit  
**NeuroTransAnalytics-v4**

**Version:** v1  
**Date:** 2026-02-23  
**Target File:** docs/tasks/Task 44.1 — Implementation Plan.md  
**Status:** Mandatory Architectural Correction — No Implementation Permitted Until Updated  

---

# 1. Context

During architectural review of **Task 44.1 — Implementation Plan**,  
a violation of the Frozen Geometry Principle was identified.

The current plan specifies:

- Re-running ETLPipeline
- Re-running BaselineFeatureExtractor
- Re-standardizing features
- Re-mapping to the 3D latent space

This is incompatible with Stage 9C constraints.

---

# 2. Architectural Principle (Locked)

Stage 9A established:

- Frozen 3D latent geometry
- Frozen covariance structure
- Frozen mapping logic

Stage 9B used:

- Precomputed 3D coordinates derived from the frozen system.

Stage 9C must:

> Operate strictly on already computed frozen 3D coordinates.

No re-extraction.
No re-mapping.
No re-standardization.
No re-projection.

---

# 3. Identified Violation

The following section in Task 44.1 must be removed:

> 1. Loads real trial metadata using ETLPipeline  
> 2. Extracts session-level baseline features via BaselineFeatureExtractor  
> 3. Standardizes features to align with the locked 3D space  

These steps constitute a re-computation of geometry and violate:

- Immutable Geometry Rule
- Stage Separation Principle
- Single-Source-of-Truth constraint

---

# 4. Required Amendment

In `population_audit_run.py`, replace steps 1–3 with:

> Load precomputed frozen 3D coordinates (Speed, Lateralization, Tone) from the Stage 9B integration dataset.  
> No feature extraction, no standardization, and no latent mapping is permitted.

Add explicitly:

> Stage 9C must consume existing 3D coordinates as immutable inputs.  
> Under no circumstances may the geometry be recomputed, reconstructed, or rederived from raw data.

---

# 5. Clarification of Data Source

Permitted inputs:

- Session-level 3D coordinates already generated in Stage 9B.
- Stored coordinate tables or cached dataset.

Prohibited inputs:

- Raw trial-level RT data
- Feature extraction pipelines
- Any transformation logic that recreates latent geometry

---

# 6. Constraints

This amendment:

- Does not authorize code execution.
- Does not authorize new data processing.
- Only updates the Implementation Plan.
- Must be applied before approval can be granted.

---

# 7. Governance Reminder

Per Governance Rule:

No implementation may proceed until the corrected Implementation Plan is reviewed and explicitly approved.

---

Status: Awaiting Corrected Task 44.1 Submission.
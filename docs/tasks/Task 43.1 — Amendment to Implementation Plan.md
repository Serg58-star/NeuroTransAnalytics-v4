# Task 43.1 — Amendment to Implementation Plan (Variance Lock Clarification)
## Stage 9B Real Longitudinal Dataset Integration  
**NeuroTransAnalytics-v4**

**Version:** v1  
**Date:** 2026-02-23  
**Target File:** docs/tasks/Task 43 — Implementation Plan.md  
**Status:** Mandatory Correction — No Code Execution Permitted Until Updated  

---

# 1. Context

During methodological review of **Task 43 — Implementation Plan v1**,  
a violation risk was identified in the wording of the fluctuation computation logic.

The current plan contains the phrase:

> "using empirical variance estimations"

This wording introduces ambiguity and potentially violates previously locked architectural constraints.

---

# 2. Problem

Stage 9B must strictly inherit:

- Locked normative variance structures from Stage 9A v1
- Locked covariance matrix from C3-Core
- Locked fluctuation model parameters
- `k_min_consecutive = 2`

The phrase "empirical variance estimations" may imply:

- Re-estimation of variance on longitudinal subset
- Local variance recalculation
- Dynamic threshold adjustment

All of the above are **explicitly prohibited**.

---

# 3. Required Amendment

In `docs/tasks/Task 43 — Implementation Plan.md`:

Locate the sentence:

> Compute the required fluctuation metrics (...) using empirical variance estimations.

Replace it with:

> Compute the required fluctuation metrics strictly using the locked normative variance structures inherited from Stage 9A v1.  
> No variance re-estimation, no covariance recalculation, and no threshold adaptation is permitted.

---

# 4. Additional Clarification Requirement

Immediately after the replacement sentence, insert:

> All fluctuation Z-scores must reference the original frozen normative parameters defined in Stage 9A.  
> The longitudinal subset must not be used to derive or adjust statistical scale parameters.

---

# 5. Constraints

This task:

- Does not authorize code changes.
- Does not authorize database interaction.
- Does not authorize script creation.
- Only updates the Implementation Plan wording.

After this amendment, the plan will be eligible for approval review.

---

# 6. Governance Reminder

Per our Governance Rule, no code may be written until the amended plan is re-reviewed and receives explicit written approval.

---

Status: Awaiting Corrected Plan Submission for Re-Review.
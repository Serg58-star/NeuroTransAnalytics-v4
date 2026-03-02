# Stage 9C — Memory Allocation Plan

**Status:** Pre-Stage 9C Memory Optimization

To transition cleanly into **Stage 9C (Risk Modeling Layer)** while respecting the 25-file active memory limit, the documentation has been categorized to preserve only the necessary structural invariants (Z-space, Anchored Projection, EIT triggers, Quadrants) and discard deprecated exploratory drafts.

---

## 1. KEEP (Testing_RT Memory)

*Keep these files actively loaded to maintain architectural boundaries and rules.*
**(Total Count: 8)**

1. `v5_Synthetic_Architecture_Completion_Summary.md` (Core v5 summary)
2. `Task_49_1A_Robust_Standardization_Amendment.md` (Z-Space math)
3. `Task_50A_Z_Space_Geometric_Validation_Criteria_Update.md` (Continium invariants)
4. `Task_51A_Z_Space_Severity_Centering_Correction.md` (Severity math)
5. `Task_52A_Anchored_Projection_Framework_for_Phase_2_Dynamics.md` (Anchored Load math)
6. `Stage_9B_Functional_Monitoring_Framework_v5.md` (Monitoring structure & Envelopes)
7. `.agent/skills/architecture-guardian/SKILL.md` (Active Guardian Rule)
8. `.agent/skills/architecture-boundary-guard/SKILL.md` (C2/C3 separation Rule)

*(Justification: These define the exact mathematical and architectural state required for transition probabilities and risk accumulation without bringing in redundant walkthroughs).*

---

## 2. INCLUDE IN NEW CHAT (Context Opening Block)

*Paste the contents or summaries of these documents into the very first prompt of the new Chat.*

1. `docs/v5/v5_Synthetic_Architecture_Completion_Summary.md` (The full locked status of all previous modules)
2. `docs/v5/Stage_9B_Functional_Monitoring_Report.md` (The final metric baselines: Condition 6.08, EIT thresholds, Quadrant distributions)
3. `docs/v5/Task_52A_Anchored_Projection_Framework_for_Phase_2_Dynamics.md` (The Anchored Projection formula is specifically critical for $\Delta Severity$ calculations)

*(Justification: Providing the locked metrics and the summary of v5 components acts as a "cold start" initialization for predictive modeling).*

---

## 3. REMOVE (From Active Memory)

*Do not load these in the new context. They are redundant or superseded.*

1. `Task 40.*` / `Task 48.*` / `Task 39.*` (All legacy v4 documents)
2. `Walkthrough_*.md` (Implementation details are no longer needed; we only need the architecture)
3. `Task_49_2_Implementation_Clarification_Review.md` (Resolved QA)
4. `Task_51_Severity_Calibration_v5_Robust_Z_Space.md` (Superseded by 51A)
5. `Task_52_Phase_2_Dynamics_Modeling_Z_Space_Load_Geometry.md` (Superseded by 52A)
6. Old `Implementation Plan` documents from finished tasks.

*(Justification: Removing these eliminates thousands of words of deprecated context, leaving strict focus on the final v5 formulas).*

---

## 4. ARCHIVE

*Persist these in the filesystem for reference, but ignore for active modeling.*

1. `docs/v5/Task_50_Population_Geometry_v5_Post_Z_Revalidation.md`
2. `docs/v5/Task_50_Population_Geometry_v5_Report.md`
3. `docs/v5/Task_51_Severity_Calibration_v5_Report.md`
4. `docs/v5/Task_52_Phase_2_Dynamics_Modeling_Report.md` (The failed Phase 2 report)

*(Justification: Historical reports that prove past completion but don't inform future Risk Layer calculations).*

---

## Technical Summary

Transitioning to the new chat with just the **8 KEEP files** and explicitly posting the **3 INCLUDE files** will leave the Stage 9C Risk Modeling Agent with ample token memory to write transition matrices and complex hazard envelope probability models without hallucinating legacy v4 features.

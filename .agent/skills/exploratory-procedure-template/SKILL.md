---
name: exploratory-procedure-template
description: Enforces the mandatory template for C3.x exploratory analysis procedures. Triggers when new exploratory modules are created.
---

# Exploratory Procedure Template Guard

This skill enforces the formal structure of all exploratory procedures
in `src/c3x_exploratory`.

## When to use this skill
- When creating a new exploratory procedure.
- When modifying an existing exploratory module.

## Mandatory Procedure Structure

Each exploratory procedure MUST explicitly define:

1. **Procedure Name**
2. **Exploratory Goal**
3. **Input Data Description**
4. **Parameters (explicit and fixed)**
5. **Output Artifact Type**
6. **Reproducibility Notes**
7. **Explicit Non-Interpretation Clause**

## Required Non-Interpretation Clause

Each procedure MUST include a statement equivalent to:

> "This procedure is exploratory and descriptive. It produces structural representations only and does not imply interpretation, inference, or evaluation."

## Forbidden Content

- Clinical, psychological, or cognitive interpretations.
- Claims of significance, meaning, or diagnosis.
- Implicit parameter tuning.
- Hidden defaults.

## Enforcement

If the template is incomplete:
- STOP.
- Request clarification.
- Do NOT generate implementation code.

This skill enforces research reproducibility.

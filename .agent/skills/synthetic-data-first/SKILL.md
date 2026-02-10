---
name: synthetic-data-first
description: Requires exploratory procedures to be developed and validated using synthetic or mock data before real data integration.
---

# Synthetic Data First

This skill enforces a synthetic-data-first development strategy
for exploratory analysis.

## When to use this skill
- When implementing a new exploratory procedure.
- When writing tests or validation code.

## Mandatory Requirements

Before any real data is allowed:

- Synthetic data generation MUST be implemented.
- Data generation parameters MUST be explicit.
- The separation between:
  - data generation,
  - exploratory computation
  MUST be clear.

## Synthetic Data Must

- Cover expected data shapes.
- Allow controlled variation.
- Enable reproducibility.

## Forbidden

- Writing exploratory logic directly against real data.
- Tuning procedures based on observed real data behavior.

## Enforcement

If no synthetic data stage is present:
- STOP.
- Request synthetic data design.
- Do NOT proceed with implementation.

This skill ensures generality and transferability.

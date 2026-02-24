# Task 44.1 — Implementation Plan for Population-Level Longitudinal Geometry Audit

## Stage 9C Longitudinal Geometry Layer

## NeuroTransAnalytics-v4

**Version**: v1
**Date**: 2026-02-23

---

# 1. Goal Description

This document outlines the implementation strategy for the Population-Level Longitudinal Geometry Audit (Task 44). The goal is to analyze the geometric organization of real longitudinal trajectories at the population level, strictly adhering to the frozen 3D latent space established in Stage 9A.

This is a descriptive audit layer (Stage 9C) designed to evaluate radial distribution, trajectory length, axis dominance, convergence/divergence, and geometric shape, without any recalculation or modification of the core architecture. Stage 9C must consume existing 3D coordinates as immutable inputs. Under no circumstances may the geometry be recomputed, reconstructed, or rederived from raw data.

## User Review Required

> [!IMPORTANT]
> **Governance Rule Active**: No code will be written or execution performed until explicit written approval is received. Please review this plan and respond with "Approved for implementation. Reference: Task 44.1 v1" if satisfactory.

## Proposed Changes

---

### Stage 9C: Population-Level Longitudinal Geometry Audit

The implementation will reside entirely within the new `src/stage9C_population_longitudinal_geometry_audit/` directory.

#### [NEW] `src/stage9C_population_longitudinal_geometry_audit/__init__.py`

Initializes the Stage 9C package.

#### [NEW] `src/stage9C_population_longitudinal_geometry_audit/trajectory_metrics.py`

A pure computation module containing functions for descriptive statistics only:

- **Radial Distribution**: Compute $M_t$, $\Delta M_t$, heavy-tail properties, and skewness across the population.
- **Trajectory Length**: Total 3D path length, mean step length, maximum radial excursion, and cumulative displacement per subject.
- **Axis Dominance**: Identify the dominant axis ($|\Delta S|$, $|\Delta L|$, $|\Delta T|$) per step and compute population proportions.
- **Convergence vs Divergence**: Net displacement from baseline, frequency of returns toward centroid, proportion of oscillating vs drifting behaviors.
- **Geometric Shape**: Curvature index, angular dispersion, and directional persistence.

*Architectural Constraint*: No clustering algorithms, no PCA/covariance recalculation, no risk modeling, and no threshold adaptation.

#### [NEW] `src/stage9C_population_longitudinal_geometry_audit/population_audit_run.py`

The execution script that glues components together:

1. Loads precomputed frozen 3D coordinates (Speed, Lateralization, Tone) from the Stage 9B integration dataset (e.g., from the output or cached tables of Task 43). No feature extraction, no standardization, and no latent mapping is permitted.
2. Filters to generate step-wise sequence metrics for subjects with $\geq 3$ valid sessions.
3. Computes requested statistics through `trajectory_metrics.py`.
4. Generates the final descriptive report.

#### [NEW] `docs/stage9C/Task44_Population_Longitudinal_Geometry_Audit_Report.md`

The final generated Markdown report, containing histograms/statistical tables and interpreting results purely geometrically without any diagnostic language.

---

## Verification Plan

### Automated Tests

- Running `python -m src.stage9C_population_longitudinal_geometry_audit.population_audit_run`.
- The execution output will be validated against rules prohibiting modification to the established distributions or adding layers/clusters.

### Manual Verification

- Reviewing the generated `Task44_Population_Longitudinal_Geometry_Audit_Report.md` to ensure all five target domains (Radial, Length, Dominance, Convergence, Shape) are covered and contain exclusively geometrical properties.
- Guaranteeing complete separation from C3-Core, Stage 9A, and Stage 9B execution paths.

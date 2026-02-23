# Stage 9A — Repository Structure & Reporting Standards  
## NeuroTransAnalytics-v4

This document defines:

1. Folder naming conventions  
2. Directory structure for Stage 9A  
3. Mandatory report template for GoAn  

These standards are binding for Task 39 implementation.

---

# 1. Folder Naming Standards

All Stage 9A components must follow strict naming conventions.

## 1.1 Top-Level Directory

stage9A_geometric_risk_modeling/


Lowercase, snake_case, no spaces.

---

## 1.2 Model Directories

Each model must have its own isolated directory:

radial_model/
vector_model/
bayesian_model/


No mixing of code across models.

Shared utilities must be placed only in:

common/


---

## 1.3 File Naming Conventions

- snake_case only
- No abbreviations without documentation
- No version numbers inside filenames

Examples:

radial_model.py
vector_model.py
bayesian_kde_model.py
evaluation_metrics.py
bootstrap_validation.py
noise_stability.py

---

# 2. Required Directory Structure

stage9A_geometric_risk_modeling/
│
├── README.md
├── config.yaml
│
├── common/
│ ├── data_loader.py
│ ├── evaluation_metrics.py
│ ├── bootstrap_validation.py
│ ├── noise_injection.py
│ └── reporting_utils.py
│
├── radial_model/
│ ├── radial_model.py
│ └── radial_evaluation.py
│
├── vector_model/
│ ├── vector_model.py
│ └── vector_evaluation.py
│
├── bayesian_model/
│ ├── bayesian_kde_model.py
│ ├── voxel_model.py (optional)
│ └── bayesian_evaluation.py
│
├── experiments/
│ ├── baseline_run.py
│ ├── bootstrap_run.py
│ └── noise_stability_run.py
│
└── reports/
└── task39_comparative_report.md


---

# 3. Architectural Rules

- No mutation of C3-Core.
- No recomputation of PCA.
- No clustering modules.
- No data transformations beyond allowed noise injection.
- All models must use identical input coordinates.

All experiments must be reproducible via a single command entry point.

---

# 4. Mandatory Report Template  
## File: reports/task39_comparative_report.md

GoAn must generate the report in Markdown format using the structure below.

---

# Task 39 — Comparative Geometric Risk Modeling  
## Execution Report

---

# 1. Dataset Description

- Number of subjects:
- Condition type:
- Class balance:
- Synthetic or real labels:

---

# 2. Model Implementations

## 2.1 Radial Model

Specification:
Risk ~ Mahalanobis Distance

Implementation details:
- Model type:
- Regularization:
- Threshold selection:

---

## 2.2 Vector Model

Specification:
Risk ~ (ΔSpeed, ΔLateral, ΔTone)

Implementation details:
- Model type:
- Interaction terms:
- Regularization:

---

## 2.3 Bayesian Model

Specification:
P(Condition | Position)

Implementation details:
- KDE bandwidth:
- Grid resolution (if voxelized):
- Smoothing parameters:

---

# 3. Baseline Performance Comparison

| Model    | ROC-AUC | Log-loss | Brier | Calibration Slope |
|----------|---------|----------|--------|------------------|
| Radial   |         |          |        |                  |
| Vector   |         |          |        |                  |
| Bayesian |         |          |        |                  |

---

# 4. Bootstrap Stability (n = 100)

| Model    | AUC Mean | AUC SD | Log-loss Mean | Log-loss SD |
|----------|----------|--------|---------------|-------------|
| Radial   |          |        |               |             |
| Vector   |          |        |               |             |
| Bayesian |          |        |               |             |

---

# 5. Noise Stability Test

## 5% Noise Injection

| Model    | ΔAUC | ΔLog-loss |
|----------|------|-----------|

## 10% Noise Injection

| Model    | ΔAUC | ΔLog-loss |

---

# 6. Comparative Analysis

- Performance ranking:
- Stability ranking:
- Noise robustness ranking:

---

# 7. Architectural Verdict

One of:

- RADIAL_DOMINANT
- VECTOR_SENSITIVE
- TOPOLOGY_DEPENDENT

Verdict must be supported strictly by quantitative metrics.

No clinical interpretation allowed.

---

# 8. Compliance Confirmation

GoAn must confirm:

- No PCA recomputation
- No clustering
- No geometry mutation
- Identical coordinate inputs across models

---

# Completion Status

Task 39 considered complete when:

- All models implemented
- Metrics computed
- Stability validated
- Noise sensitivity assessed
- Architectural verdict assigned

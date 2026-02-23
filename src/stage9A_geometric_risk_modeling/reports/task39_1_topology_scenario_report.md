# Task 39 — Comparative Geometric Risk Modeling  
## Execution Report

---

# 1. Dataset Description

- Number of subjects: 10000
- Condition type: Binary (Topology Dependent pockets)
- Class balance: 50.51% Positives
- Synthetic or real labels: Synthetic (Stage 9A strict isolated test)

---

# 2. Model Implementations

## 2.1 Radial Model

Specification:
Risk ~ Mahalanobis Distance

Implementation details:
- Model type: Logistic Regression
- Regularization: None explicitly (C=1e9)
- Threshold selection: Default 0.5 (continuous probabilities used)

---

## 2.2 Vector Model

Specification:
Risk ~ (ΔSpeed, ΔLateral, ΔTone)

Implementation details:
- Model type: Logistic Regression
- Interaction terms: None
- Regularization: None explicitly (C=1e9)

---

## 2.3 Bayesian Model

Specification:
P(Condition | Position)

Implementation details:
- KDE bandwidth: Scott's rule (scipy default)
- Grid resolution (if voxelized): N/A (continuous KDE)
- Smoothing parameters: None

---

# 3. Baseline Performance Comparison

| Model    | ROC-AUC | Log-loss | Brier | Calibration Slope |
|----------|---------|----------|--------|------------------|
| Radial   | 0.5056 | 0.6931 | 0.2500 | 0.0008 |
| Vector   | 0.5155 | 0.6928 | 0.2498 | 1.0017 |
| Bayesian | 0.7294 | 0.5992 | 0.2087 | 1.3814 |

---

# 4. Bootstrap Stability (n = 100)

| Model    | AUC Mean | AUC SD | Log-loss Mean | Log-loss SD |
|----------|----------|--------|---------------|-------------|
| Radial   | 0.4995 | 0.0100 | 0.6934 | 0.0003 |
| Vector   | 0.5078 | 0.0075 | 0.6934 | 0.0005 |
| Bayesian | 0.6819 | 0.0067 | 0.6674 | 0.0151 |

---

# 5. Noise Stability Test

## 5% Noise Injection

| Model    | ΔAUC | ΔLog-loss |
|----------|------|-----------|
| Radial   | 0.0010 | -0.0000 |
| Vector   | -0.0002 | -0.0000 |
| Bayesian | 0.0008 | -0.0004 |

## 10% Noise Injection

| Model    | ΔAUC | ΔLog-loss |
|----------|------|-----------|
| Radial   | 0.0021 | -0.0000 |
| Vector   | -0.0004 | -0.0000 |
| Bayesian | 0.0003 | 0.0006 |

---

# 6. Comparative Analysis

- Baseline AUC winner: Bayesian
- Stability winner: Radial
- Noise robustness winner: Radial
- Calibration winner: Vector

### Formal Model Scores
| Model | Score(M) |
|-------|----------|
| Radial | -0.0100 |
| Vector | 0.4995 |
| Bayesian | 0.4845 |

---

# 7. Architectural Verdict

- TOPOLOGY_DEPENDENT

---

# 8. Compliance Confirmation

- [x] No PCA recomputation
- [x] No clustering
- [x] No geometry mutation
- [x] Identical coordinate inputs across models

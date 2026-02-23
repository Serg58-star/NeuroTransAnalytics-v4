# Task 39 — Comparative Geometric Risk Modeling  
## Execution Report

---

# 1. Dataset Description

- Number of subjects: 1000
- Condition type: Binary (Radial Dominant)
- Class balance: 38.00% Positives
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
| Radial   | 0.7681 | 0.5493 | 0.1845 | 0.9998 |
| Vector   | 0.5222 | 0.6625 | 0.2347 | 0.9996 |
| Bayesian | 0.7988 | 0.5530 | 0.1860 | 1.8446 |

---

# 4. Bootstrap Stability (n = 100)

| Model    | AUC Mean | AUC SD | Log-loss Mean | Log-loss SD |
|----------|----------|--------|---------------|-------------|
| Radial   | 0.7701 | 0.0198 | 0.5509 | 0.0210 |
| Vector   | 0.4946 | 0.0261 | 0.6699 | 0.0104 |
| Bayesian | 0.7446 | 0.0206 | 0.8208 | 0.1550 |

---

# 5. Noise Stability Test

## 5% Noise Injection

| Model    | ΔAUC | ΔLog-loss |
|----------|------|-----------|
| Radial   | 0.0038 | -0.0019 |
| Vector   | -0.0029 | 0.0002 |
| Bayesian | 0.0049 | -0.1014 |

## 10% Noise Injection

| Model    | ΔAUC | ΔLog-loss |
|----------|------|-----------|
| Radial   | 0.0060 | -0.0022 |
| Vector   | -0.0039 | 0.0003 |
| Bayesian | 0.0093 | -0.0002 |

---

# 6. Comparative Analysis

- Baseline AUC winner: Bayesian
- Stability winner: Vector
- Noise robustness winner: Bayesian
- Calibration winner: Radial

### Formal Model Scores
| Model | Score(M) |
|-------|----------|
| Radial | 0.7502 |
| Vector | 0.4683 |
| Bayesian | 0.3017 |

---

# 7. Architectural Verdict

- RADIAL_DOMINANT

---

# 8. Compliance Confirmation

- [x] No PCA recomputation
- [x] No clustering
- [x] No geometry mutation
- [x] Identical coordinate inputs across models

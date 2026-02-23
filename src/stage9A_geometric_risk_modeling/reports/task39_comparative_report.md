# Task 39 — Comparative Geometric Risk Modeling  
## Execution Report

---

# 1. Dataset Description

- Number of subjects: 1000
- Condition type: Binary (Vector Sensitive)
- Class balance: 39.00% Positives
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
| Radial   | 0.5812 | 0.6606 | 0.2340 | 1.0024 |
| Vector   | 0.9279 | 0.3264 | 0.1035 | 1.0001 |
| Bayesian | 0.9444 | 0.3076 | 0.0953 | 1.5699 |

---

# 4. Bootstrap Stability (n = 100)

| Model    | AUC Mean | AUC SD | Log-loss Mean | Log-loss SD |
|----------|----------|--------|---------------|-------------|
| Radial   | 0.5771 | 0.0253 | 0.6635 | 0.0101 |
| Vector   | 0.9285 | 0.0105 | 0.3281 | 0.0238 |
| Bayesian | 0.9135 | 0.0116 | 0.4349 | 0.0903 |

---

# 5. Noise Stability Test

## 5% Noise Injection

| Model    | ΔAUC | ΔLog-loss |
|----------|------|-----------|
| Radial   | -0.0047 | 0.0010 |
| Vector   | 0.0009 | -0.0011 |
| Bayesian | 0.0009 | 0.0999 |

## 10% Noise Injection

| Model    | ΔAUC | ΔLog-loss |
|----------|------|-----------|
| Radial   | -0.0089 | 0.0022 |
| Vector   | -0.0003 | 0.0006 |
| Bayesian | 0.0014 | 0.0073 |

---

# 6. Comparative Analysis

- Baseline AUC winner: Bayesian
- Stability winner: Radial
- Noise robustness winner: Bayesian
- Calibration winner: Vector

### Formal Model Scores
| Model | Score(M) |
|-------|----------|
| Radial | 0.5506 |
| Vector | 0.9179 |
| Bayesian | 0.6169 |

---

# 7. Architectural Verdict

- VECTOR_SENSITIVE

---

# 8. Compliance Confirmation

- [x] No PCA recomputation
- [x] No clustering
- [x] No geometry mutation
- [x] Identical coordinate inputs across models

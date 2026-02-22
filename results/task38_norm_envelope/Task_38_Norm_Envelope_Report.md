# Task 38: Mathematical Norm Envelope & Deviation Metrics

## Context
This report mathematically defines the boundaries of the "Norm" within the continuous 3D latent PCA space established in Stages 7-8, completely independently of clinical variables. Minimum Covariance Determinant (MCD) estimators define a mathematically robust center against which structural deviations (abnormalities) are strictly measured.

## 1. Centroid & Radial Geometry (Block A)
* **Robust Median Center (MCD)**:
  * Speed (PC1): `-0.289`
  * Lateral (PC2): `0.045`
  * Tone (PC3): `-0.007`
* **Median Subject Mahalanobis Distance (DM)**: `1.672`

## 2. Normative Envelopes (Block B)
Based on Chi-Square distribution ($df=3$):
* **50% Core (DM² $\le 2.366$)**: Encompasses `43.5%` of empirical subjects.
* **75% Envelope (DM² $\le 4.108$)**: Encompasses `63.7%` of empirical subjects.
* **90% Envelope (DM² $\le 6.251$)**: Encompasses `75.3%` of empirical subjects.
* **95% Envelope (DM² $\le 7.815$)**: Encompasses `80.3%` of empirical subjects.
* **Severe Outliers (DM² $> 7.815$)**: Constitutes `19.7%` of the population.

## 3. Density-Based Norm (Block C)
Kernel Density Estimation (KDE) confirms the density hierarchy inside the continuous limits:
* **High-Density Core**: `741` subjects.
* **Medium-Density Band**: `592` subjects.
* **Low-Density Fringe (<10th pct)**: `149` subjects.

## 4. Radial vs Axial Deviations (Block D)
Analysis of the extreme deviants (the `19.7%` outside the 95% envelope):
* Outliers driven primarily by Speed Axis (PC1): `86` subjects
* Outliers driven primarily by Lateral Axis (PC2): `117` subjects
* Outliers driven primarily by Tone Axis (PC3): `89` subjects

This demonstrates a `RADIAL_CONTINUUM_WITHOUT_BREAK`—outliers are distributed across axes rather than forming an isolated cluster along one dimension.

## 5. Stability Under Noise (Block E)
* **1% Gaussian Noise**: `100.3%` retention of 95% envelope boundary.
* **5% Gaussian Noise**: `100.3%` retention.
* **10% Gaussian Noise**: `100.2%` retention.

Mathematical limits are resilient to extreme measurement noise.

---
## FINAL ARCHITECTURAL CONCLUSIONS
**STABLE_NORM_CORE**
**DENSITY_LAYERED_NORM**
**RADIAL_CONTINUUM_WITHOUT_BREAK**

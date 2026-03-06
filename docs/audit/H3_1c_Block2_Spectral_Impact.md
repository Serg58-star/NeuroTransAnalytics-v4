# H3.1c Block 1 & 2 — Motor Model Definition & Spectral Impact

**Date**: 2026-03-04  
**Status**: COMPLETED  
**Basis**: Stage H3.1c — Correlated Motor Layer Simulation Audit

---

## Scope

Implementation of a Monte Carlo simulation where a theoretical Motor processing time is synthesized as a huge fraction of the Global Factor `G`, plus noise. This Motor component is then mathematically subtracted from the raw F1 channels to evaluate the pure Neural geometry.

## 1. Simulation Definition

We assumed the raw reaction time comprises shared `Motor` limits and independent `Neural` channel limits.
`Motor_i = α * G_i + noise(5ms)`

We tested extreme dependency states where the motor action accounts for 60% up to 90% (`α`) of the shared global variance.

## 2. Spectral Geometry of Neural Space

| Motor Fraction (`α`) | Neural L/C/R Correlation | Neural Effective Rank | Neural PC1% Variance | Neural λ₁ (Raw Amplitude) |
| :---: | :---: | :---: | :---: | :---: |
| **Original F1 (No Motor)** | **0.930** | **1.26** | **95.0%** | **6038** |
| **α = 0.60** (60% Motor)| 0.820 | 1.56 | 88.1% | 2336 |
| **α = 0.70** (70% Motor)| 0.782 | 1.67 | 85.6% | 1882 |
| **α = 0.80** (80% Motor)| **0.737** | **1.79** | **82.7%** | **1515** |
| **α = 0.90** (90% Motor)| 0.692 | 1.90 | 79.7% | 1251 |

## 3. Structural Diagnosis

Even under an extreme simulation where 80-90% of the massive shared variance is artificially siphoned off and classified as "Motor Execution Time", the remaining purely `Neural` spatial geometry refuses to collapse into the isotropic Rank=2.90 spherical geometry seen in the v5 synthetic generator.

At 80% motor-absorption, the Neural baseline still exhibits massive L/C/R correlation (r ≈ 0.74) and remains highly 1D-dominant (Eff.Rank=1.79, PC1=82.7%).

## Formal Verdict

> **BASELINE_NEURAL_GLOBAL**

The 1D-dominant, highly-correlated geometry of the empirical F1 baseline is not an artifact of motor execution time. Even mathematically erasing theoretical motor dependencies leaves a fundamentally correlated neural sensing architecture that v5 currently fails to model.

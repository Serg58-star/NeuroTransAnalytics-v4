# H2 Final — Structural Consistency Report

**Date**: 2026-03-03  
**Status**: COMPLETED  
**Basis**: Stage H2 Blocks 1–4

---

## Block Summary

| Block | Title | Formal Verdict |
| :--- | :--- | :---: |
| **Block 1** | Synthetic Isomorphism Audit | **NON_ISOMORPHIC** |
| **Block 2** | Stage 7 Geometry Replication by Sex | **GEOMETRY_STABLE** (with amplitude asymmetry) |
| **Block 3** | Extended Age Spectral Geometry | **AGE_GRADIENT_GEOMETRY** |
| **Block 4** | Variance Decomposition | η²(sex)=0.57%, η²(age)=6.99%, residual=92.4% |

---

## Key Structural Findings

### 1. Empirical vs Synthetic: NON_ISOMORPHIC

The v5 synthetic Z-space (12-dim, Eff.Rank=10.84) is fundamentally geometrically incompatible with the empirical feature space (3 channels, Eff.Rank=1.83). The empirical space is:

- Strongly 1D-dominant (PC1=82%)  
- Highly anisotropic (λ₁/λ₃=11.6)  
- Exhibits moderate clustering tendency (Peak Silhouette=0.62)

The synthetic v5 space is:

- Uniformly distributed (PC1=14%)  
- High-dimensional and nearly isotropic  
- Continuous and non-clustered (Silhouette=0.08)

### 2. Sex Geometry: Stable Topology, Non-Equal Amplitude

The 3D continuum is preserved for both male and female cohorts separately. However:

- Male λ₁ = 3.334 vs Female λ₁ = 1.839 → **ratio = 1.81×**  
- Male Peak Silhouette = 0.683 vs Female = 0.544

Sex does not rupture the topology, but **males have significantly larger variance on the dominant axis**. This is a scale effect invisible to cluster-based metrics (Stage 8 finding of SEX_INVARIANT_DYNAMICS was correct; but the baseline absolute RT variance structure is sex-differentiated).

### 3. Age Spectral Gradient: Q2 as Outlier

Q2 (ages 27–39) shows a distinctly different spectral regime:

- Eff.Rank = 2.28 (vs Q1=1.59, Q3=1.64)  
- Anisotropy = 6.04 (vs Q1=27.7, Q3=22.0)  
- λ₁ = 0.607 (vs Q1=3.92, Q3=2.34)

The stage 7 AGE_INVARIANT_CONTINUUM verdict remains correct for cluster topology but does **not** extend to spectral properties.

### 4. Variance Attribution

| Source | η² |
| :--- | :---: |
| Sex | 0.006 (0.57%) |
| Age (quartile) | 0.070 (6.99%) |
| Residual | 0.924 (92.44%) |

The residual component dominates, confirming that inter-individual heterogeneity is the primary source of variance. Demographic factors account for < 8% combined.

---

## Diagnostic Answer: Where Did the Structural Discrepancy Originate?

> **Primary origin: In the synthetic model.**

The v5 synthetic data was generated as a 12-dimensional uniformly-distributed Z-space (via the Dual-Space Architecture, Task 49.1A), designed to be high-rank and demographically neutral.

The empirical Stage 7 space is 3-channeled, low-dimensional (Eff.Rank≈1.83), and anisotropic with non-trivial spectral age-gradients and sex-amplitude asymmetries.

These spaces are structurally non-isomorphic. The v5 synthetic framework did not replicate the dominant anisotropy or the age-quartile Q2 spectral anomaly present in the empirical data.

**Secondary contributor: In empirical Stage 7 interpretation.**

Stage 7 correctly identified cluster-topology invariance. It did not report spectral age-gradients or sex λ₁ amplitude asymmetry — this audit (Block 3) reveals these existed but were not surfaced at the time.

> No architectural recommendations are made in this document.

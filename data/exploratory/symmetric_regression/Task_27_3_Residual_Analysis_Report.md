# Task 27.3D — Residual Structure Analysis Report

---

## 1. Корреляции residual с латентными переменными (Pearson)

| Residual | Latent Variable | n | Pearson r | p-value | Flag |
|---|---|---|---|---|---|
| delta_v4_left_residual | psi_tau | 1478 | 0.009991 | 0.701139 |  |
| delta_v4_left_residual | asym_dv1_abs | 1482 | -0.006798 | 0.793709 |  |
| delta_v4_left_residual | asym_dv1_rel | 1482 | 0.160992 | 4.571504e-10 |  |
| delta_v4_right_residual | psi_tau | 1478 | 0.012329 | 0.635796 |  |
| delta_v4_right_residual | asym_dv1_abs | 1482 | 0.139044 | 7.686286e-08 |  |
| delta_v4_right_residual | asym_dv1_rel | 1482 | -0.193698 | 5.402674e-14 |  |
| delta_v5_left_residual | psi_tau | 1478 | -0.004679 | 0.857361 |  |
| delta_v5_left_residual | asym_dv1_abs | 1482 | 0.104052 | 5.990526e-05 |  |
| delta_v5_left_residual | asym_dv1_rel | 1482 | 0.094018 | 0.000290 |  |
| delta_v5_right_residual | psi_tau | 1478 | -0.030347 | 0.243628 |  |
| delta_v5_right_residual | asym_dv1_abs | 1482 | 0.218406 | 1.836833e-17 |  |
| delta_v5_right_residual | asym_dv1_rel | 1482 | -0.209175 | 4.088136e-16 |  |

## 2. Корреляции residual с латентными переменными (Spearman)

| Residual | Latent Variable | n | Spearman ρ | p-value | Flag |
|---|---|---|---|---|---|
| delta_v4_left_residual | psi_tau | 1478 | 0.065308 | 0.012029 |  |
| delta_v4_left_residual | asym_dv1_abs | 1482 | -0.035972 | 0.166336 |  |
| delta_v4_left_residual | asym_dv1_rel | 1482 | 0.191041 | 1.201174e-13 |  |
| delta_v4_right_residual | psi_tau | 1478 | 0.082808 | 0.001441 |  |
| delta_v4_right_residual | asym_dv1_abs | 1482 | 0.125948 | 1.150968e-06 |  |
| delta_v4_right_residual | asym_dv1_rel | 1482 | -0.237615 | 1.813038e-20 |  |
| delta_v5_left_residual | psi_tau | 1478 | 0.064545 | 0.013067 |  |
| delta_v5_left_residual | asym_dv1_abs | 1482 | -0.017313 | 0.505414 |  |
| delta_v5_left_residual | asym_dv1_rel | 1482 | 0.153644 | 2.762122e-09 |  |
| delta_v5_right_residual | psi_tau | 1478 | 0.048783 | 0.060795 |  |
| delta_v5_right_residual | asym_dv1_abs | 1482 | 0.113457 | 1.196679e-05 |  |
| delta_v5_right_residual | asym_dv1_rel | 1482 | -0.152612 | 3.532576e-09 |  |

## 3. Cross-component residual correlations (ΔV4 vs ΔV5)

| Pair | n | Pearson r | p-value | Spearman ρ | p-value | Flag |
|---|---|---|---|---|---|---|
| ΔV4_left vs ΔV5_left | 1482 | 0.326805 | 3.174161e-38 | 0.326203 | 4.401749e-38 | |r|≥0.3 |
| ΔV4_right vs ΔV5_right | 1482 | 0.277639 | 1.230184e-27 | 0.306396 | 1.398275e-33 |  |

## 4. Межполушарные residual correlations (left vs right)

| Pair | n | Pearson r | p-value | Spearman ρ | p-value | Flag |
|---|---|---|---|---|---|---|
| ΔV4_left vs ΔV4_right | 1482 | 0.735350 | 2.362213e-252 | 0.613241 | 8.555943e-154 | |r|≥0.5 |
| ΔV5_left vs ΔV5_right | 1482 | 0.693635 | 4.160594e-213 | 0.622568 | 8.566456e-160 | |r|≥0.5 |

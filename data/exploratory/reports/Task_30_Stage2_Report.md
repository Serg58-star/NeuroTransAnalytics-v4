# Task 30. Stage 2 — Координатные преобразования латерализации

> This procedure is exploratory and descriptive. It produces structural representations only and does not imply interpretation, inference, or evaluation.

## 1. Сравнительные метрики

| Transformation | Dim (λ>1) | PC1 % | PR | Boot SD | SH ΔPC1 | B/W Ratio |
|---|---|---|---|---|---|---|
| Baseline | 3 | 32.79 | 4.730 | 1.49 | 2.41 | 2.96 |
| Block A (Mean/Diff) | 3 | 28.64 | 5.632 | 1.05 | 1.78 | 1.13 |
| Block B (Asymmetry) | 1 | 49.20 | 2.972 | 1.70 | 2.94 | 1.06 |

## 2. PC1 и PC2 Loadings (Baseline vs Block A)

### Baseline (Left/Right basis)
| Feature | PC1 | PC2 |
|---|---|---|
| `delta_v4_left_residual` | 0.456 | 0.414 |
| `delta_v4_right_residual` | 0.492 | 0.132 |
| `delta_v5_left_residual` | 0.466 | 0.112 |
| `delta_v5_right_residual` | 0.500 | -0.121 |
| `asym_dv1_abs` | 0.237 | -0.583 |
| `asym_dv1_rel` | -0.162 | 0.666 |
| `psi_tau` | -0.006 | 0.021 |

### Block A (Mean/Diff basis)
| Feature | PC1 | PC2 |
|---|---|---|
| `mean_v4` | -0.166 | 0.615 |
| `diff_v4` | 0.492 | 0.099 |
| `mean_v5` | -0.152 | 0.671 |
| `diff_v5` | 0.367 | 0.346 |
| `asym_dv1_abs` | -0.457 | 0.137 |
| `asym_dv1_rel` | 0.603 | 0.151 |
| `psi_tau` | 0.008 | -0.013 |

### Block B (Asymmetry basis)
| Feature | PC1 | PC2 |
|---|---|---|
| `diff_v4` | 0.502 | -0.010 |
| `diff_v5` | 0.402 | 0.768 |
| `asym_dv1_abs` | -0.447 | 0.640 |
| `asym_dv1_rel` | 0.622 | -0.028 |

## 3. Дисперсия Diff-компонент (Блок А)

- `diff_v4` составляет **14.29%** от общей дисперсии нового базиса.
- `diff_v5` составляет **14.29%** от общей дисперсии нового базиса.

## 4. Сценарный анализ латерализации

Сценарии:

1. **Латерализация формирует вторую ось / независима**. (При смене координат метрики стабильны, а изолированное подпространство асимметрии образует устойчивую геометрию с Dim >= 1).
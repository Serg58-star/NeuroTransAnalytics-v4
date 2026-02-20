# Task 31. Stage 3 — Канальная реконструкция (Parvo / Magno / Koniocellular)

> This procedure is exploratory and descriptive. It produces structural representations only and does not imply interpretation, inference, or evaluation.

## 1. Сравнительные метрики

| Transformation | Dim (λ>1) | PC1 % | PR | Boot SD | SH ΔPC1 | B/W Ratio |
|---|---|---|---|---|---|---|
| Baseline | 3 | 32.79 | 4.730 | 1.49 | 2.41 | 2.96 |
| Block A (Channels) | 3 | 28.64 | 5.632 | 1.05 | 1.78 | 1.13 |
| Block B (Aggregated 3D) | 1 | 44.54 | 2.809 | 1.99 | 3.24 | 2.71 |

## 2. PC1 и PC2 Loadings (Block A: Channels)

| Feature | PC1 | PC2 |
|---|---|---|
| `parvo_mean` | -0.166 | 0.615 |
| `magno_mean` | -0.152 | 0.671 |
| `parvo_diff` | 0.492 | 0.099 |
| `magno_diff` | 0.367 | 0.346 |
| `asym_dv1_abs` | -0.457 | 0.137 |
| `asym_dv1_rel` | 0.603 | 0.151 |
| `psi_tau` | 0.008 | -0.013 |

## 3. Корреляционная матрица каналов (Block C)

| Channel | Parvo Index | Magno Index | Lateral Index |
|---|---|---|---|
| **parvo_index** | 1.000 | 0.299 | -0.087 |
| **magno_index** | 0.299 | 1.000 | -0.071 |
| **lateral_index** | -0.087 | -0.071 | 1.000 |

## 4. Сценарный анализ

Сценарии:

3. **Канальная агрегация разрушает структуру**. Размерность падает ниже 2, что говорит о некорректности предложенной декомпозиции.
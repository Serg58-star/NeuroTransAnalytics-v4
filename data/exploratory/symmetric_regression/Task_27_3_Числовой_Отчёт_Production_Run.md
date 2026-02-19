# Task 27.3 — Числовой Отчёт Production Run

---

## 1. Размер выборки

| Показатель | Значение |
|---|---|
| Количество субъектов в анализе | 1482 |
| Количество моделей | 4 |
| n (delta_v4_left) | 1482 |
| n (delta_v4_right) | 1482 |
| n (delta_v5_left) | 1482 |
| n (delta_v5_right) | 1482 |

---

## 2. Линейные модели

### ΔV4 ~ ΔV1

| Поле | n | R² | Adjusted R² | β | p-value | residual_ratio |
|---|---|---|---|---|---|---|
| LEFT | 1482 | 0.002982 | 0.002308 | 0.052901 | 0.035562 | 0.997018 |
| RIGHT | 1482 | 0.011276 | 0.010608 | 0.119092 | 4.202036e-05 | 0.988724 |

### ΔV5 ~ ΔV1

| Поле | n | R² | Adjusted R² | β | p-value | residual_ratio |
|---|---|---|---|---|---|---|
| LEFT | 1482 | 0.013912 | 0.013246 | 0.147314 | 5.295022e-06 | 0.986088 |
| RIGHT | 1482 | 4.375421e-05 | -0.000632 | 0.008235 | 0.799162 | 0.999956 |

### ΔR² left vs right

| Pathway | R²_left | R²_right | ΔR²_left_vs_right |
|---|---|---|---|
| ΔV4 | 0.002982 | 0.011276 | -0.008294 |
| ΔV5 | 0.013912 | 4.375421e-05 | 0.013868 |

---

## 3. Множественные модели

### ΔV4 ~ ΔV1 + MAD

| Поле | R²_simple | R²_multiple | ΔR² | Adjusted R² | std_β_median | std_β_MAD |
|---|---|---|---|---|---|---|
| LEFT | 0.002982 | 0.002983 | 1.007600e-06 | 0.001634 | 2.487802 | 0.060951 |
| RIGHT | 0.011276 | 0.020926 | 0.009650 | 0.019603 | 1.761762 | 6.185186 |

### ΔV5 ~ ΔV1 + MAD

| Поле | R²_simple | R²_multiple | ΔR² | Adjusted R² | std_β_median | std_β_MAD |
|---|---|---|---|---|---|---|
| LEFT | 0.013912 | 0.015728 | 0.001816 | 0.014397 | 4.878487 | 3.335569 |
| RIGHT | 4.375421e-05 | 0.005943 | 0.005899 | 0.004599 | -2.787237 | 5.367943 |

### ΔR² Summary

| Категория | Модели |
|---|---|
| ΔR² < 0.02 | delta_v4_left (ΔR²=1.007600e-06); delta_v4_right (ΔR²=0.009650); delta_v5_left (ΔR²=0.001816); delta_v5_right (ΔR²=0.005899) |
| ΔR² ≥ 0.05 | — |

---

## 4. Residual correlations

### Корреляции residual с латентными переменными (Pearson)

| Residual | Latent Variable | n | Pearson r | p-value |
|---|---|---|---|---|
| delta_v4_left_residual | psi_tau | 1478 | 0.009991 | 0.701139 |
| delta_v4_left_residual | asym_dv1_abs | 1482 | -0.006798 | 0.793709 |
| delta_v4_left_residual | asym_dv1_rel | 1482 | 0.160992 | 4.571504e-10 |
| delta_v4_right_residual | psi_tau | 1478 | 0.012329 | 0.635796 |
| delta_v4_right_residual | asym_dv1_abs | 1482 | 0.139044 | 7.686286e-08 |
| delta_v4_right_residual | asym_dv1_rel | 1482 | -0.193698 | 5.402674e-14 |
| delta_v5_left_residual | psi_tau | 1478 | -0.004679 | 0.857361 |
| delta_v5_left_residual | asym_dv1_abs | 1482 | 0.104052 | 5.990526e-05 |
| delta_v5_left_residual | asym_dv1_rel | 1482 | 0.094018 | 0.000290 |
| delta_v5_right_residual | psi_tau | 1478 | -0.030347 | 0.243628 |
| delta_v5_right_residual | asym_dv1_abs | 1482 | 0.218406 | 1.836833e-17 |
| delta_v5_right_residual | asym_dv1_rel | 1482 | -0.209175 | 4.088136e-16 |

|r| ≥ 0.3: —

|r| ≥ 0.5: —

---

## 5. Heteroscedasticity

| Модель | n | BP-statistic | p-value | heteroscedastic | |resid| corr | |resid| p-value |
|---|---|---|---|---|---|---|
| delta_v4_left | 1482 | 178.419110 | 0.000000 | True | 0.412294 | 6.657010e-62 |
| delta_v4_right | 1482 | 87.737438 | 0.000000 | True | 0.411425 | 1.262202e-61 |
| delta_v5_left | 1482 | 213.774884 | 0.000000 | True | 0.355225 | 2.597920e-45 |
| delta_v5_right | 1482 | 75.700124 | 0.000000 | True | 0.305288 | 2.440974e-33 |

---

## 6. τ stability

Данные по стабильности τ (Mean τ, SD τ, CV τ, Corr(τ, PSI_count), Corr(τ, PSI_range), Corr(τ, Median_ΔV1)) не сохранены в CSV-файлах.

---

## 7. Distribution diagnostics

Данные по диагностике распределений (Skewness, Kurtosis, % выбросов >3 SD) не сохранены в CSV-файлах.

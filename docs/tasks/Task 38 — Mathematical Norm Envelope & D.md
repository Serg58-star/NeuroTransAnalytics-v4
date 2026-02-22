# NeuroTransAnalytics-v4  
# Stage 8.5 — Formal Normative Boundary Definition  
# Task 38 — Mathematical Norm Envelope & Deviation Metrics

---

## 1. Контекст

Stage 7 доказал непрерывность 3D пространства.  
Stage 8 доказал его динамическую устойчивость.

Перед переходом к Stage 9 (Clinical Validation) необходимо:

> Формально определить математические границы нормы
> внутри 3D латентного пространства.

Норма должна быть определена строго геометрически,
без клинических ярлыков.

---

## 2. Цель Task 38

Определить:

1. Центральную зону популяционного распределения.
2. Радиальную структуру отклонений.
3. Плотностные уровни.
4. Метрики дистанции от «нормативного ядра».

---

## 3. Блок A — Центроид и Радиальная Геометрия

### 3.1 Популяционный центроид

Вычислить:

- Mean vector (μ)
- Robust median center
- Covariance matrix

### 3.2 Mahalanobis Distance

Для каждого субъекта:

- D_M (расстояние до центра с учётом ковариации)

Построить распределение D_M.

---

## 4. Блок B — Нормативные оболочки

Определить:

- 50% core ellipsoid
- 75% envelope
- 90% envelope
- 95% envelope

Метод:

- Multivariate Gaussian approximation
- Robust covariance (MCD)

---

## 5. Блок C — Density-Based Norm

Использовать:

- kNN density
- Kernel Density Estimation (3D)

Определить:

- High-density core region
- Medium-density band
- Low-density fringe

---

## 6. Блок D — Radial vs Axial Deviations

Разложить отклонение на:

- радиальное (distance from centroid)
- осевое (component-wise z-score)

Определить:

- оси, наиболее влияющие на экстремальность
- распределение extreme positions

---

## 7. Блок E — Stability of Norm Under Noise

Проверить:

- устойчивость границ при 5% noise injection
- стабильность центроида
- стабильность эллипсоидов

---

## 8. Формат отчёта

GoAn должен предоставить:

1. Центроид и ковариационную матрицу.
2. Таблицу нормативных эллипсоидов (50/75/90/95%).
3. Распределение Mahalanobis distances.
4. Density map.
5. Robustness analysis.
6. Формальный вывод в формате:

   - STABLE_NORM_CORE
   - DENSITY_LAYERED_NORM
   - RADIAL_CONTINUUM_WITHOUT_BREAK

Без клинической интерпретации.

---

## 9. Архитектурное значение

Task 38 определяет:

- Где заканчивается «центр» популяции.
- Как измерять степень отклонения.
- Можно ли вводить количественную метрику «атипичности».
- Как перейти к клинической стратификации без типологизации.

Stage 8.5 обязателен перед Stage 9.
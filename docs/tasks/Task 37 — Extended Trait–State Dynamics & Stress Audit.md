# NeuroTransAnalytics-v4  
# Stage 8 — Trait vs State Decomposition  
# Task 37 — Extended Trait–State Dynamics & Stress Audit

---

## 1. Статус

Task 37 открывает Stage 8 Exploratory Architecture Framework v4.

Ветка:
feature/A8_trait_state_dynamics

Stage 8 следует за Stage 7 (Population Geometry CLOSED).

Цель — формально декомпозировать латентное 3D пространство на:

- стабильную межсубъектную компоненту (Trait)
- внутрисубъектную динамическую компоненту (State)
- проверить устойчивость динамики к шуму
- проверить половую инвариантность динамической структуры

Интерпретационный слой не активируется.

---

## 2. Исходные данные

Используется 3D латентное пространство:

- Speed Axis
- Lateral Axis
- Residual Tone

Обязательные условия:

- использовать trial-level данные
- не агрегировать каналы
- не изменять Stage 7 пространство
- использовать visit_id при наличии
- использовать trial order внутри сессии

---

# 3. Блок A — Variance Decomposition

## 3.1 Дисперсионная модель

Для каждой оси:

Total Variance = Between-subject + Within-subject

Рассчитать:

- ICC
- Within / Between ratio
- Subject-specific variance profile

---

## 3.2 Test-Retest (если доступны визиты)

- межвизитная корреляция
- Euclidean displacement
- Stability Index

---

# 4. Блок B — Trajectory Geometry

## 4.1 Внутрисессионные траектории

Для каждого субъекта:

- восстановить 3D trajectory
- рассчитать:
  - path length
  - mean step size
  - radial displacement
  - axis-specific variance

---

## 4.2 Радиальное vs Осевое движение

Определить:

- движение вдоль главной оси
- ортогональное движение
- rotational vs translational pattern

---

# 5. Блок C — Temporal Structure

## 5.1 Autocorrelation

Для каждой оси:

- ACF
- PACF

---

## 5.2 Hurst Exponent

Для каждой оси:

- H < 0.5 → anti-persistent
- H ≈ 0.5 → random
- H > 0.5 → persistent

---

# 6. Блок D — Attractor & Stability Analysis

1. Distance to subject centroid
2. Drift relative to global centroid
3. Convergence patterns
4. Local dynamic density changes

---

# 7. Блок E — Noise Injection Stress-Test

## 7.1 Controlled Noise Injection

Добавить к координатам:

- Gaussian noise (1%, 3%, 5%, 10% SD)
- Axis-specific noise
- Random temporal permutation

---

## 7.2 Проверить влияние шума на:

- ICC
- Hurst exponent
- Path length distribution
- Attractor detection
- Variance ratios

Цель:

Определить устойчивость Trait–State декомпозиции.

---

# 8. Блок F — Sex-Stratified Dynamic Analysis

Использовать переменную sex.

Разделить на:

- Male
- Female

(если третья категория присутствует — анализ отдельно)

---

## 8.1 Variance Decomposition by Sex

- ICC by sex
- Within/Between ratio

---

## 8.2 Dynamic Metrics by Sex

Сравнить:

- path length distribution
- Hurst exponent
- radial displacement
- axis-specific dynamic variance

---

## 8.3 Interaction Test

Модель:

Dynamic Metric ~ Sex + Trait Position

Проверить наличие взаимодействия.

---

# 9. Формат отчёта

GoAn обязан предоставить:

1. Variance Decomposition table
2. ICC per axis
3. Path length distribution
4. Hurst summary
5. Noise sensitivity table
6. Sex comparison table
7. Dynamic topology summary

Формальный вывод строго в формате:

- TRAIT_DOMINANT_SPACE
- STATE_SIGNIFICANT_MODULATION
- DYNAMICALLY_STRUCTURED_MANIFOLD
- NOISE_SENSITIVE_STRUCTURE
- SEX_INVARIANT_DYNAMICS
- SEX_DIFFERENTIATED_DYNAMICS

Без физиологической интерпретации.

---

# 10. Архитектурное значение

Task 37 определяет:

1. Насколько пространство стабильно.
2. Есть ли выраженная временная организация.
3. Устойчив ли вывод Stage 8 к шуму.
4. Инвариантна ли динамика по полу.
5. Требуется ли в v5 учитывать динамический слой как отдельную ось.

Stage 8 начинается с Task 37 (extended).
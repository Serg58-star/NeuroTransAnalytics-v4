# Task 50 — Population Geometry v5 (Post-Z Revalidation)

## Status
MANDATORY ARCHITECTURAL REVALIDATION

## Branch
v5-dual-space-architecture

## Prerequisite
Task 49.1 — Dual-Space Vector Architecture  
Task 49.1A — Robust Standardization Amendment (Z-Robust Layer)

---

# 1. Objective

После внедрения Robust Z-Standardization (Task 49.1A)  
пространство v5 перешло в безразмерную форму.

Task 50 предназначен для полной повторной геометрической валидации популяционного пространства в Z-координатах.

Цель:

- подтвердить сохранение латентной структуры,
- проверить размерность пространства,
- пересчитать ковариационную геометрию,
- оценить устойчивость Global Modulator (G),
- проверить инвариант ~15% общего модуля,
- исключить коллапс размерности,
- подтвердить непрерывность популяционного континуума.

---

# 2. Data Layer

Вход:

Z-space координаты субъектов:

\[
Z \in \mathbb{R}^{N \times 12}
\]

где N — число субъектов,
12 — канально-полевые координаты (Z-standardized).

Важно:

- Используются только robust-standardized координаты.
- Raw (ms) пространство не участвует в ковариационной геометрии.

---

# 3. Analytical Blocks

## 3.1 Covariance Matrix

Вычислить:

\[
\Sigma_Z = Cov(Z)
\]

Проверить:

- положительную определённость,
- устойчивость при bootstrap,
- стабильность при split-half.

---

## 3.2 PCA Spectrum

Вычислить:

- Eigenvalues
- PC1 %
- Participation Ratio (PR)
- λ > 1 criterion

Проверить:

1. Сохраняется ли размерность ≥ 3?
2. Не происходит ли коллапс в 1D?
3. Не доминирует ли один канал искусственно?

---

## 3.3 Global Modulator Revalidation

Извлечь:

\[
G = PC1(\Sigma_Z)
\]

Проверить:

- долю объяснённой дисперсии PC1,
- сопоставимость с v4 (~15% общемодулирующего вклада),
- устойчивость PC1 к bootstrap.

Важно:

PC1 теперь отражает чистую ковариацию, а не scale.

---

## 3.4 Dimensional Stability Tests

Провести:

- Bootstrap (≥ 1000 итераций)
- Split-half validation
- Noise injection (Gaussian noise 5–10%)

Проверить:

- стабильность PC1 %
- стабильность PR
- устойчивость ранга

---

## 3.5 Radial Continuum Check

Вычислить Mahalanobis distance в Z-space:

\[
D_M = \sqrt{(Z - \mu)^T \Sigma_Z^{-1} (Z - \mu)}
\]

Проверить:

- отсутствие кластеризации,
- плотностную стратификацию (KDE),
- сохранение радиального континуума.

---

# 4. Required Outputs

GoAn обязан предоставить:

1. Таблицу PCA-метрик.
2. PR, Dim, PC1 %.
3. Bootstrap SD.
4. Split-half ΔPC1.
5. Noise stability report.
6. Проверку сохранения непрерывности.
7. Сравнительный блок: v4 vs v5 (геометрия).

---

# 5. Validation Criteria

Task 50 считается пройденным, если:

- Dim ≥ 3
- PC1 не превышает 50% (исключение 1D collapse)
- PR остаётся сопоставимым с v4
- Общий модуль сохраняется (~15% ± допустимое отклонение)
- Пространство остаётся непрерывным
- Нет искусственной кластеризации

---

# 6. Governance Rule

Перед внесением изменений в расчёт Severity, Risk или Monitoring Framework:

- результаты Task 50 должны быть утверждены,
- геометрия v5 считается валидированной,
- только после этого разрешён переход к Task 51.

---

# 7. Deliverable

GoAn должен создать:

docs/v5/Task_50_Population_Geometry_v5_Report.md

С подробным аналитическим отчётом и таблицами результатов.

---

# 8. Architectural Status After Completion

Если Task 50 проходит валидацию:

v5 Population Geometry → LOCKED

Это открывает переход к:

- Task 51 — Severity Calibration v5
- Task 52 — Phase 2 Dynamics Modeling
- Stage 9B — Functional Monitoring Framework (v5)

С подробным аналитическим отчётом и таблицами результатов.

---

# 8. Architectural Status After Completion

Если Task 50 проходит валидацию:

v5 Population Geometry → LOCKED

Это открывает переход к:

- Task 51 — Severity Calibration v5
- Task 52 — Phase 2 Dynamics Modeling
- Stage 9B — Functional Monitoring Framework (v5)
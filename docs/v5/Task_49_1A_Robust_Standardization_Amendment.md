# Task 49.1A — Robust Standardization Amendment

## Status
ARCHITECTURAL AMENDMENT  
(Pending Approval)

## Parent Specification
Task 49.1 — Dual-Space Vector Architecture for v5

## Branch
v5-dual-space-architecture

---

# 1. Purpose of Amendment

Данная поправка формально вводит обязательный слой робастной стандартизации
между:

Primary Physiological Raw Space  
и  
Analytical Orthogonal Space.

Поправка устраняет выявленное методологическое искажение,
при котором каналы с большей дисперсией деформируют
геометрию ортогонального пространства.

---

# 2. Problem Statement

В версии Task 49.1 Analytical Space оперировал медианными координатами
в миллисекундах.

Это приводит к следующим рискам:

1. Каналы с большей дисперсией доминируют в PCA и ортогонализации.
2. Global Modulator (PC1) искажается scale-эффектом.
3. Mahalanobis distance становится чувствительным к неравномерности масштабов.
4. Геометрия перестаёт быть сопоставимой между каналами.

---

# 3. Architectural Principle Introduced

## Инвариант A1:

Raw Space остаётся в физиологических единицах (мс).

## Инвариант A2:

Analytical Space работает в безразмерных робастно-стандартизированных координатах.

---

# 4. Formal Definition of the Robust Standardization Layer

Пусть:

X_F — медианная оценка канала X в поле F ∈ {L, C, R}  
MAD_X — медианное абсолютное отклонение канала X

Robust Z-score определяется как:

\[
Z_{X,F} = \frac{X_F - \tilde{X}}{MAD_X}
\]

где:

\[
\tilde{X} = median(X_L, X_C, X_R)
\]

Таким образом:

- центрирование происходит относительно канальной медианы,
- масштаб определяется MAD,
- используется робастная, а не гауссовская стандартизация.

---

# 5. Revised Space Transition

## Stage 1 — Robust Estimation

Trial-level данные → median + MAD → Raw Vector \( R \in \mathbb{R}^{12} \)

## Stage 2 — Robust Standardization (NEW)

\[
R^{(Z)} \in \mathbb{R}^{12}
\]

где каждая координата заменяется на:

\[
Z_{X,F}
\]

## Stage 3 — Analytical Space Construction

Вычисление:

\[
Center_X = \frac{Z_{X,L} + Z_{X,C} + Z_{X,R}}{3}
\]

\[
Lat_{X,L} = Z_{X,L} - Z_{X,C}
\]

\[
Lat_{X,R} = Z_{X,R} - Z_{X,C}
\]

Analytical Space становится безразмерным.

---

# 6. Implications for Global Modulator (G)

PC1 вычисляется из ковариационной матрицы:

\[
\Sigma_Z = Cov(R^{(Z)})
\]

Следовательно:

\[
G = \text{PC1}(\Sigma_Z)
\]

Инвариант:

Global Modulator строится только на standardized robust coordinates.

---

# 7. Implications for Severity Index

Mahalanobis distance вычисляется в standardized пространстве:

\[
Severity = \sqrt{(x_Z - \mu_Z)^T \Sigma_Z^{-1} (x_Z - \mu_Z)}
\]

Это устраняет scale-доминирование каналов.

---

# 8. Phase 2 Clarification

Фаза 2 обрабатывается независимо:

\[
Raw_{F2} \rightarrow Robust_{F2} \rightarrow Z_{F2}
\]

Разность определяется как:

\[
\Delta Z = Z_{F2} - Z_{F1}
\]

Оператор \( \lambda \cdot d \) становится аналитической аппроксимацией
наблюдаемого \(\Delta Z\),
а не генерацией данных.

---

# 9. Invariants Preserved

1. Median remains mandatory.
2. MAD remains mandatory.
3. No mean RT introduced.
4. Central field preserved.
5. Local Donders unchanged.
6. Dual-space structure preserved.
7. Small-sample robustness maintained.
8. Heavy-tail stability preserved.

---

# 10. Versioning Impact

This amendment upgrades Task 49.1 to:

Task 49.1 (v1.1)

All implementations must comply with this amendment before approval.

---

# 11. Approval Condition

После утверждения данного Amendment:

- GoAn получает разрешение на рефакторинг dual_space_core.py.
- Обязательные изменения:
  - внедрение Robust Z-layer,
  - перерасчёт G на standardized координатах,
  - перерасчёт Severity,
  - обновление тестов.

Без утверждения Amendment A реализация Task 49.1 считается незавершённой.
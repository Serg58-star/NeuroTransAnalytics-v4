# Stage_H5 — Correlated Baseline Generator Redesign

## Исполнитель: GoAn

## Роль ChatGPT: независимая методическая верификация

---

# 1. Основание

Предыдущие этапы установили:

**Stage_H3.1**

* Baseline F1 в эмпирике имеет **1D-доминантную геометрию**
* L / C / R каналы имеют **r > 0.92**
* Effective Rank ≈ 1.2

**Stage_H3.1c**

* Удаление до **90% моторной дисперсии** не разрушает корреляционную структуру baseline
* Следовательно baseline-связность является **нейрональной**

**Stage_H3.2**

* Δ-архитектура v5 корректна

**Stage_H4**

* Load-генератор успешно декуплирован от baseline

Следовательно:

> Единственный оставшийся архитектурный дефект v5 — Phase-1 Baseline Generator.

Текущий v5 генерирует baseline как **почти сферическую 3D структуру**, что противоречит эмпирической 1D-доминантности.

---

# 2. Цель Stage_H5

Разработать **Correlated Baseline Generator**, который:

1. Воспроизводит глобальный baseline-фактор скорости реакции
2. Генерирует пространственные каналы как коррелированные проекции
3. Сохраняет эмпирическую 1D-доминантность
4. Воспроизводит амплитудную демографию
5. Не нарушает Phase-2 Load архитектуру

---

# 3. Формальная модель baseline

## 3.1 Глобальный латентный фактор

Ввести скрытый baseline-фактор:

[
G_i \sim Distribution_{baseline}
]

Рекомендуемая модель:

[
G_i \sim LogNormal(\mu,\sigma)
]

или

[
G_i \sim Gamma(k,\theta)
]

Этот фактор представляет **общую скорость нейронной обработки**.

---

## 3.2 Пространственные каналы

Три пространственных канала генерируются как проекции G:

[
V1_L = G_i + \epsilon_{L,i}
]

[
V1_C = G_i + \epsilon_{C,i}
]

[
V1_R = G_i + \epsilon_{R,i}
]

где

[
\epsilon_{k,i} \sim N(0,\sigma_{local})
]

Требования:

* Corr(L,C) ≥ 0.90
* Corr(L,R) ≥ 0.90
* Corr(C,R) ≥ 0.90

---

# 4. Геометрические требования

После генерации baseline:

Проверить:

| Метрика        | Требование |
| -------------- | ---------- |
| Effective Rank | 1.1 – 1.5  |
| PC1 variance   | ≥ 90%      |
| Corr(L,C,R)    | ≥ 0.90     |

Deliverable:

`docs/redesign/H5_Block1_Baseline_Spectral_Geometry.md`

---

# 5. Демографическая структура

Baseline должен отражать амплитудную демографию.

## 5.1 Sex amplitude scaling

Ввести множитель:

[
G_i = G_i \cdot (1 + \alpha_{sex})
]

Требование:

Male/Female λ₁ ratio ≈ 1.8 – 2.1

Deliverable:

`docs/redesign/H5_Block2_Sex_Baseline_Scaling.md`

---

## 5.2 Age structure

Ввести нелинейную функцию:

[
G_i = f_{age}(Age_i) \cdot G_i
]

Требования:

* Q2 variance minimum
* Non-monotonic spectral structure

Deliverable:

`docs/redesign/H5_Block3_Age_Baseline_Structure.md`

---

# 6. Проверка совместимости с Phase-2

После генерации baseline:

1. Применить **Stage_H4 Load Generator**
2. Проверить:

* Δ-геометрия
* отсутствие baseline→load корреляции

Deliverable:

`docs/redesign/H5_Block4_Baseline_Load_Independence.md`

---

# 7. Проверка совместимости с v5

Проверить:

* Z-score computation
* κ = 0.08 stability anchor
* Severity calculation

Deliverable:

`docs/redesign/H5_Block5_v5_System_Compatibility.md`

---

# 8. Критерии завершения

Stage_H5 считается завершённым если:

1. Baseline-геометрия соответствует эмпирике
2. Демографическая структура воспроизводится
3. Phase-2 остаётся независимым
4. v5 downstream-метрики сохраняются

---

# 9. Возможные финальные verdict

* BASELINE_GENERATOR_CORRECTED
* BASELINE_PARTIAL_ALIGNMENT
* BASELINE_GENERATOR_FAILED

---

# Назначение Stage_H5

Завершить архитектурную коррекцию v5.

После Stage_H5 система должна содержать:

1. **Correlated Neural Baseline Layer**
2. **Independent Functional Load Layer**
3. **Valid Z-space Severity Metrics**
4. **Stable κ-threshold framework**

---

# Конец задачи

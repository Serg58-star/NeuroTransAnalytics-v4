# Task_Stage_H6 — Full System Consistency Audit

**Executor:** GoAn  
**Role of ChatGPT:** Independent methodological verification  
**Project:** NeuroTransAnalytics-v5 / Testing_RT  
**Status:** ARCHITECTURAL CONSISTENCY STAGE  

---

# 1. Основание

Предыдущая сессия (Stage_H2 → Stage_H5) завершила реконструкцию архитектуры v5.

Установлено:

- Baseline (F1) — **1D-доминантный глобальный фактор**
- Functional transitions (Δ) — **многомерное почти ортогональное пространство**
- Demography влияет **только на variance baseline**
- Load penalties являются **индивидуальным state-показателем**
- Synthetic генераторы baseline и load **перепроектированы**

Архитектура системы теперь формально состоит из четырёх слоёв:

Layer 1 — Correlated Neural Baseline
Layer 2 — Independent Functional Load
Layer 3 — PSI Sequential Dynamics
Layer 4 — Z-space Severity Model

κ = 0.08 stability anchor


Однако все предыдущие этапы проверяли **слои по отдельности**.

Следовательно требуется **финальная проверка согласованности всей архитектуры как единой системы**.

---

# 2. Цель Stage_H6

Проверить, что все слои архитектуры v5:

- математически совместимы,
- не создают скрытых зависимостей,
- не нарушают геометрию пространства,
- не разрушают Severity-метрики.

Ключевой вопрос Stage_H6:

> Сохраняется ли геометрическая и статистическая устойчивость системы при полном соединении всех архитектурных слоёв?

---

# 3. Общие ограничения

В отличие от предыдущих этапов:

Разрешено:

- использовать **полную synthetic систему v5**
- использовать **Severity**
- использовать **κ**
- использовать **PSI**

Запрещено:

- менять архитектуру
- менять генераторы
- подгонять параметры
- вводить новые переменные
- менять Z-пространство

Stage_H6 — **чистый аудит согласованности**, а не этап разработки.

---

# 4. Аналитические блоки

Каждый блок оформляется **отдельным .md документом**.

---

# Block 1 — Baseline → Δ Independence Verification

## Цель

Подтвердить, что после Stage_H4/H5:

Cov(Baseline, Δ) ≈ 0


Baseline-геометрия не определяет функциональные нагрузки.

## Проверить

1. Corr(F1, ΔV4)
2. Corr(F1, ΔV5)
3. Corr(F1, ΔLat)
4. Partial correlations controlling for Age/Sex
5. Mutual information (Baseline vs Load)

## Требования

| Metric | Expected |
|------|------|
| |Corr| < 0.05 |
| Mutual Information | ≈ 0 |

## Deliverable

docs/audit/H6_Block1_Baseline_Load_Independence.md


---

# Block 2 — Load → Z-Space Projection Stability

## Цель

Проверить, что переход

Raw RT → Z-space


не искажает геометрию функционального пространства.

## Проверить

1. Δ-space covariance matrix (raw)
2. Δ-space covariance matrix (Z-space)
3. Effective Rank
4. PC1 variance
5. λ-spectrum comparison

## Требования

| Metric | Condition |
|------|------|
| Eff.Rank difference | < 10% |
| PC1 shift | < 5% |
| λ-spectrum | shape preserved |

## Deliverable

docs/audit/H6_Block2_Zspace_Geometry_Stability.md


---

# Block 3 — PSI Interaction Audit

## Цель

Проверить, что PSI-динамика не искажает базовую геометрию пространства.

PSI должен быть **динамическим модификатором**, а не структурным фактором.

## Проверить

1. Corr(PSI metrics, ΔV4)
2. Corr(PSI metrics, ΔV5)
3. Corr(PSI metrics, Severity)
4. Δ-space geometry with PSI regressed out
5. Change in Effective Rank

## Формальные критерии

| Metric | Expected |
|------|------|
| PSI → Δ correlation | low |
| PSI → Severity | moderate |
| Eff.Rank change | < 5% |

## Deliverable

docs/audit/H6_Block3_PSI_Interaction_Audit.md


---

# Block 4 — Severity Geometry Consistency

## Цель

Проверить корректность перехода:

Z-vector → Severity(Z)


Severity должен отражать **геометрическую дистанцию**, а не отдельные координаты.

## Проверить

1. Distribution Severity
2. Correlation Severity vs individual Z axes
3. Contribution of each axis
4. Stability under bootstrap
5. Sensitivity to heavy-tail samples

## Требования

| Metric | Condition |
|------|------|
| Dominant axis contribution | < 35% |
| Bootstrap SD | stable |
| Heavy-tail robustness | preserved |

## Deliverable

docs/audit/H6_Block4_Severity_Geometry.md


---

# Block 5 — κ Stability Anchor Verification

## Цель

Проверить устойчивость **κ-якоря (0.08)** в полной архитектуре.

κ должен сохранять стабильность longitudinal drift.

## Проверить

1. Longitudinal simulation
2. Mean reverting behavior
3. Spectral gap
4. Transition stability

## Требования

| Metric | Target |
|------|------|
| P_ii | < 0.95 |
| Spectral gap | ≥ 0.15 |
| System entropy | ≥ 0.60 |

## Deliverable

docs/audit/H6_Block5_Kappa_Stability.md


---

# Block 6 — End-to-End System Stress Test

## Цель

Проверить систему как **единую архитектуру**.

Полный pipeline:

Baseline generation
↓
Functional load
↓
PSI dynamics
↓
Z transformation
↓
Severity computation
↓
Longitudinal drift (κ)


## Проверить

1. Numerical stability
2. Absence of NaN
3. Geometry preservation
4. Heavy-tail behavior
5. Risk tail capture

## Deliverable

docs/audit/H6_Block6_End_to_End_System_Audit.md


---

# 5. Финальный агрегированный документ

После завершения всех блоков сформировать:

docs/audit/H6_Final_System_Consistency_Report.md


Документ должен содержать:

1. Краткое summary каждого блока
2. Таблицу ключевых метрик
3. Финальный вердикт

---

# 6. Возможные финальные verdict

SYSTEM_ARCHITECTURE_CONSISTENT

или

SYSTEM_PARTIAL_INCONSISTENCY

или

SYSTEM_ARCHITECTURE_UNSTABLE


---

# 7. Критерий завершения Stage_H6

Stage_H6 считается завершённым только если:

- выполнены **все 6 блоков**
- сформированы **6 отдельных документов**
- сформирован **H6_Final_System_Consistency_Report**
- не предложены архитектурные изменения

---

# Назначение Stage_H6

Подтвердить, что архитектура v5:

- математически согласована
- геометрически устойчива
- готова к переходу

Stage 10 — Real Dataset Pilot

---

# Конец документа

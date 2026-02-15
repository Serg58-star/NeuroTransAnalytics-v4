# Task 19 — C3.4 Scenario Computation (A0 First)

**Project:** NeuroTransAnalytics-v4  
**Current Branch:** main  
**New Branch to create:** feature/task-19-c3-4-scenario-a0  
**Layer:** C3.4 — Scenario Computation  
**Prerequisites:**  
- C3.1 — ETL (etl_v4.1.2)  
- C3.2 — Component Timing (component_v4.0.0)  
- C3.3 — QC & Aggregation (qc_aggregation_v4.0.0)  
**Executor:** Google Antigravity (GoAn)  
**Mode:** Planning Required  

---

## 1. Контекст

Слои C3.1–C3.3 завершены и интегрированы в main.

Переходим к C3.4 — Scenario Engine.

Согласно архитектуре v4:

- Сценарный анализ начинается строго с уровня A0.
- Никакие сценарии A1–D не допускаются до завершения A0.
- Сценарный слой не вводит новых вычислительных метрик.
- Используются только агрегаты из C3.3.

---

## 2. Цель задачи

Реализовать слой C3.4 для сценариев уровня A0:

### A0.0 — ΔV1 Baseline Stability  
### A0.1 — ΔV1 Variability Profile  

Без перехода к A1.

---

## 3. Входной контракт

Input:

AggregatedFrame (из C3.3)


Содержит:

- subject_id
- session_id
- age
- sex
- test_type
- count_valid
- median_rt_ms
- mad_rt_ms
- iqr_rt_ms
- median_ΔV1
- mad_ΔV1
- iqr_ΔV1
- median_ΔV4
- median_ΔV5_MT

---

## 4. Сценарий A0.0 — ΔV1 Baseline Stability

### Логика:

1. Рассматривается только Tst1.
2. Используется:
   - median_ΔV1
   - mad_ΔV1
   - iqr_ΔV1
3. Формируется структурированная запись:

A0_0_result


Поля:

- subject_id
- session_id
- baseline_median
- baseline_mad
- baseline_iqr
- count_valid

Без интерпретации.

---

## 5. Сценарий A0.1 — ΔV1 Variability Profile

### Логика:

1. Рассматривается Tst1.
2. Используется:
   - mad_ΔV1
   - iqr_ΔV1
3. Формируется:

A0_1_result


Поля:

- subject_id
- session_id
- variability_mad
- variability_iqr

Без порогов.
Без классификаций.
Без выводов.

---

## 6. Архитектурные ограничения

- Нет интерпретации.
- Нет пороговых решений.
- Нет клинических заключений.
- Нет перехода к A1.
- Нет визуализации.
- Нет изменения агрегатов.
- Нет повторного QC.
- Нет статистических тестов.

C3.4 — это структурированное представление результатов,
а не аналитическая логика.

---

## 7. Структура реализации

src/c3_core/scenario_engine/
init.py
scenario_v4.py


Класс:

ScenarioEngineV4


Методы:

- run_a0_0(df)
- run_a0_1(df)
- run(df)

Метод run возвращает:

"A0_0": DataFrame,
"A0_1": DataFrame


---

## 8. Definition of Done

1. Используются только агрегаты C3.3.
2. Количество строк соответствует числу сессий Tst1.
3. Нет фильтраций.
4. Нет изменения значений.
5. Нет добавления новых метрик.
6. Реализация детерминирована.
7. Walkthrough предоставлен.
8. Implementation Plan утверждён до реализации.

---

## 9. Запрещено

- Добавлять новые вычисления.
- Добавлять пороги.
- Делать сравнения между тестами.
- Делать интерпретации.
- Делать выводы.
- Делать классификацию.
- Переходить к A1.

---

После утверждения Task 19 — переход к Planning Mode.

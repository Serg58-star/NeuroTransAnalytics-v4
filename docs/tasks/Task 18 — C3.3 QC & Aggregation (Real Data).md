# Task 18 — C3.3 QC & Aggregation (Real Data)

**Project:** NeuroTransAnalytics-v4  
**Current Branch:** main  
**New Branch to create:** feature/task-18-c3-3-qc-aggregation  
**Layer:** C3.3 — QC & Aggregation  
**Prerequisites:**  
- C3.1 — ETL (etl_v4.1.2)  
- C3.2 — Component Timing (component_v4.0.0)  
**Executor:** Google Antigravity (GoAn)  
**Mode:** Planning Required  

---

## 1. Контекст

Слои C3.1 и C3.2 завершены и интегрированы в main.

Текущий шаг архитектуры v4 — слой C3.3:

- алгоритмический контроль качества,
- детерминированная маркировка валидности,
- расчёт устойчивых агрегатов,
- подготовка данных для C3.4 (Scenario Engine).

C3.3 не интерпретирует данные.

---

## 2. Цель задачи

Реализовать слой C3.3, который:

1. Принимает ComponentFrame из C3.2.
2. Применяет QC-фильтрацию на основе `technical_qc_flag`.
3. Формирует агрегированные показатели:
   - медиана
   - MAD
   - IQR
4. Не изменяет исходные строки.
5. Не удаляет данные физически.
6. Не выполняет сценарных расчётов.
7. Не выполняет визуализацию.

---

## 3. Входной контракт

Input:

ComponentFrame (DataFrame)


Содержит:

- subject_id
- session_id
- age
- sex
- test_type
- stimulus_index
- rt_ms
- psi_pre_ms
- ΔV1
- ΔV4
- ΔV5_MT
- technical_qc_flag

---

## 4. Логика QC

C3.3 не пересчитывает технический QC.

Он:

- использует `technical_qc_flag`,
- исключает `technical_qc_flag == False` из агрегатов,
- не удаляет строки из базового DataFrame.

---

## 5. Агрегации

### 5.1 Уровень агрегирования

Минимальный уровень:

subject_id
session_id
test_type


Допустимые дополнительные уровни:

- psi_pre_ms
- stimulus_color
- stimulus_location

---

### 5.2 Метрики

Для каждой группы рассчитываются:

- median_rt
- mad_rt
- iqr_rt
- median_ΔV1
- median_ΔV4
- median_ΔV5_MT

MAD рассчитывается как:

median(|x - median(x)|)

IQR:

Q3 - Q1


Использовать только детерминированные функции.

---

## 6. Выходной контракт

Выход:

AggregatedFrame (DataFrame)


Содержит:

- grouping keys
- count_valid
- медианы
- MAD
- IQR

Никаких интерпретаций.

---

## 7. Структура реализации

src/c3_core/qc_aggregation/
init.py
qc_aggregation_v4.py


Класс:

QCAggregationV4


Методы:

- apply_qc_filter(df)
- compute_robust_stats(df)
- run(df)

---

## 8. Архитектурные ограничения

- Нет доступа к SQLite.
- Нет импорта C3.4.
- Нет импорта GUI.
- Нет визуализации.
- Нет сценарной логики.
- Нет изменения C3.1 или C3.2.

---

## 9. Definition of Done

1. Количество строк в исходном DataFrame не изменяется.
2. QC применяется только к агрегатам.
3. Все агрегаты воспроизводимы.
4. Нет скрытых фильтраций.
5. Нет использования mean как основного показателя.
6. Реализация детерминирована.
7. Walkthrough предоставлен.
8. Implementation Plan утверждён до реализации.

---

## 10. Запрещено

- Делать популяционные выводы.
- Делать кластеризацию.
- Делать сценарные сравнения.
- Делать визуализацию.
- Удалять строки.
- Изменять значения ΔV.

---

После утверждения Task 18 — переход к Planning Mode.

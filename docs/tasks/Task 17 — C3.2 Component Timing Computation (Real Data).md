# Task 17 — C3.2 Component Timing Computation (Real Data)

**Project:** NeuroTransAnalytics-v4  
**Branch to create:** feature/task-17-c3-2-component-timing  
**Layer:** C3.2 — Component Timing Computation  
**Prerequisite:** C3.1 ETL v4.1.2 (approved)  
**Executor:** Google Antigravity (GoAn)  
**Mode:** Planning Required  

---

## 1. Контекст

Слой C3.1 завершён и стабилен (etl_v4.1.2).  
Данные нормализованы в EventFrame.

Следующий обязательный слой архитектуры v4 — **C3.2**:

- детерминированный расчёт компонент временной архитектуры;
- отсутствие интерпретации;
- отсутствие агрегирования;
- отсутствие сценарной логики.

Основание: C3 Map и C3.2 Component Timing Computation v4.

---

## 2. Цель задачи

Реализовать вычислительный модуль C3.2, который:

1. Принимает EventFrame из C3.1.
2. Рассчитывает для каждой валидной реакции:
   - ΔV1
   - ΔV4 (только для Tst2)
   - ΔV5/MT (только для Tst3)
3. Не модифицирует входные данные.
4. Не выполняет QC-фильтрацию.
5. Не выполняет агрегирование.
6. Не выполняет сценарные вычисления.

---

## 3. Входной контракт

Input:

EventFrame (pandas DataFrame)


Обязательные поля:

- subject_id
- session_id
- age
- sex
- test_type
- stimulus_index
- rt_ms
- psi_pre_ms
- stimulus_color
- stimulus_location
- technical_qc_flag

---

## 4. Выходной контракт

Выходной DataFrame (ComponentFrame):

| Field | Description |
|-------|------------|
| subject_id | unchanged |
| session_id | unchanged |
| test_type | unchanged |
| stimulus_index | unchanged |
| rt_ms | unchanged |
| psi_pre_ms | unchanged |
| ΔV1 | float |
| ΔV4 | float / NaN |
| ΔV5_MT | float / NaN |
| technical_qc_flag | unchanged |

ΔV4:
- вычисляется только для Tst2  
- для Tst1 и Tst3 → NaN

ΔV5_MT:
- вычисляется только для Tst3  
- для Tst1 и Tst2 → NaN

---

## 5. Методологические ограничения

1. Расчёт строго арифметический.
2. Никакой физиологической интерпретации.
3. Никаких статистических выводов.
4. Никаких агрегатов (медиан, MAD).
5. Не изменять RT.
6. Не удалять строки.
7. Не фильтровать по technical_qc_flag.

---

## 6. Алгоритмические требования

### 6.1 ΔV1

- Базовая компонента.
- Вычисляется для всех тестов.
- Формула строго соответствует методологии v4.
- Использует rt_ms и параметры дизайна (PSI, позиция).

### 6.2 ΔV4

- ΔV4 = RT(Tst2) − базовая модель ΔV1
- Только для Tst2.
- Не использовать усреднение.
- Не использовать группировку.

### 6.3 ΔV5/MT

- Аналогично ΔV4.
- Только для Tst3.

---

## 7. Структура реализации

Рекомендуемая структура:

src/c3_core/component_timing/
init.py
component_v4.py


Класс:

ComponentTimingV4


Методы:

- compute_delta_v1(df)
- compute_delta_v4(df)
- compute_delta_v5_mt(df)
- run(df)

---

## 8. Архитектурные ограничения

- Нет импорта C3.3.
- Нет импорта C3.4.
- Нет импорта GUI.
- Нет прямого доступа к SQLite.
- Работа исключительно с DataFrame.

---

## 9. Definition of Done

1. Количество строк не изменяется.
2. Все ΔV поля рассчитаны корректно.
3. Нет NaN в ΔV1 (кроме технически невозможных случаев).
4. ΔV4 присутствует только для Tst2.
5. ΔV5_MT присутствует только для Tst3.
6. Реализация детерминированна.
7. Создан Walkthrough.
8. Implementation Plan утверждён до реализации.

---

## 10. Порядок выполнения

1. Передать данный документ GoAn.
2. GoAn формирует Implementation Plan.
3. Архитектор проверяет план.
4. После утверждения — реализация.
5. Архитектурный аудит.
6. Merge в main.

---

## 11. Запрещено

- Включать агрегаты.
- Включать популяционный анализ.
- Включать сценарные расчёты.
- Делать интерпретацию.
- Изменять C3.1.

---

После утверждения Task 17 переходим к Planning Mode.

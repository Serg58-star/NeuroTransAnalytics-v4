# Task 20 — C3.5 Scenario Visualization (A0)

**Project:** NeuroTransAnalytics-v4  
**Current Branch:** main  
**New Branch to create:** feature/task-20-c3-5-scenario-visualization-a0  
**Layer:** C3.5 — Visualization  
**Prerequisites:**  
- C3.1 — ETL (etl_v4.1.2)  
- C3.2 — Component Timing (component_v4.0.0)  
- C3.3 — QC & Aggregation (qc_aggregation_v4.0.0)  
- C3.4 — Scenario Engine (scenario_v4.0.0, A0 implemented)  
**Executor:** Google Antigravity (GoAn)  
**Mode:** Planning Required  

---

## 1. Контекст

Вычислительный пайплайн C3 полностью реализован для уровня A0:

ETL → Component → QC Aggregation → Scenario (A0)


Однако результаты сценариев не отображаются в GUI.

Слой C3.5 предназначен для:

- отображения готовых ScenarioResult,
- без выполнения вычислений,
- без интерпретации,
- без изменения данных.

---

## 2. Цель задачи

Реализовать C3.5 для сценариев A0:

- A0.0 — Baseline Stability
- A0.1 — Variability Profile

GUI должен:

1. Загружать готовые ScenarioResult.
2. Отображать таблицы.
3. Позволять базовую навигацию (фильтр по subject/session).
4. Не выполнять пересчёт.

---

## 3. Архитектурные ограничения (критически важно)

### 3.1 GUI НЕ должен:

- вызывать ETL
- вызывать ComponentTiming
- вызывать QC
- вызывать ScenarioEngine
- выполнять агрегации
- пересчитывать метрики
- изменять данные

GUI работает только с уже вычисленными результатами.

---

## 4. Формат входных данных

C3.4 должен экспортировать ScenarioResult как:

data/derived/scenarios/A0_0.parquet
data/derived/scenarios/A0_1.parquet


или JSON-эквивалент.

C3.5 загружает только эти файлы.

---

## 5. Функциональность GUI

### 5.1 Экран “A0 Baseline”

Отображает:

- subject_id
- session_id
- baseline_median
- baseline_mad
- baseline_iqr
- count_valid

Дополнительно:

- сортировка
- фильтрация по subject_id
- поиск по session_id

---

### 5.2 Экран “A0 Variability”

Отображает:

- subject_id
- session_id
- variability_mad
- variability_iqr

---

### 5.3 Метаданные (обязательно)

В нижней панели отображать:

- version C3.4
- timestamp генерации
- указание:
  
  > “Exploratory representation. No interpretation.”

---

## 6. Структура реализации

src/gui/scenario_viewer/
init.py
scenario_viewer.py
a0_views.py


Компоненты:

- ScenarioLoader (читает parquet/json)
- ScenarioTableModel
- A0BaselineView
- A0VariabilityView

---

## 7. Definition of Done

1. GUI отображает данные A0.0.
2. GUI отображает данные A0.1.
3. Нет вызова вычислительных слоёв.
4. Нет скрытых вычислений.
5. Отображается версия и timestamp.
6. Реализация отделена от C3.
7. Walkthrough предоставлен.
8. Implementation Plan утверждён до реализации.

---

## 8. Запрещено

- Добавлять графические "оценки нормы".
- Добавлять цветовую интерпретацию.
- Добавлять клинические выводы.
- Добавлять статистические тесты.
- Делать динамический пересчёт.

---

## 9. Следующий этап

После реализации C3.5:

- результаты становятся наблюдаемыми,
- можно переходить к A1,
- либо к C4 (Interpretation Layer).

---

After approval → switch to Planning Mode.

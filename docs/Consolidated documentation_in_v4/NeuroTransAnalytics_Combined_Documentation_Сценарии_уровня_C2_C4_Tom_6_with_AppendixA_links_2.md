<!-- ================================================== -->
<!-- source: 11_1_C2_1_Data_Model_v4.md -->
<!-- ================================================== -->
<a id="doc-2-11_1_c2_1_data_model_v4"></a>

# C2.1 — Логическая модель данных (Data Model v4)

---

## Appendix A — Data & Legacy Context (ссылка)

См. **Appendix A — Data & Legacy Context**: `Appendix_A_Data_and_Legacy_Context.md`

Ключевое содержание Appendix A:
- источники данных (`testbase.mdb`, `users.xlsx`, `boxbase`);
- codebook таблиц `users` и `boxbase`;
- критические метаданные стимулов (цвет, позиция, PSI, “тройки”);
- системные параметры тестирования;
- контекст текущей реализации (GUI/SQLite) и правила безопасной разработки.

---

## 1. Назначение документа

Документ описывает **логическую модель данных версии v4** проекта *NeuroTransAnalytics*.

Цель модели — формально определить сущности, их атрибуты и связи таким образом, чтобы:

* все сценарии анализа уровней **A0–B3** были воспроизводимы;
* все методические требования уровня **C1** были реализуемы без потерь;
* данные могли расширяться без изменения уже сохранённой структуры.

Документ **не описывает физическую реализацию** (форматы, СУБД) — это предмет C2.2.

---

## 2. Общие принципы логической модели

### 2.1. Принцип событийной первичности

Базовой единицей данных является **событие**, а не агрегат.

* каждое предъявление стимула — отдельное событие;
* каждая реакция — отдельное событие;
* агрегаты всегда вычисляются поверх событий.

---

### 2.2. Принцип раздельности дизайна и реакции

В модели:

* параметры **дизайна теста** хранятся отдельно;
* параметры **реакции** хранятся отдельно;
* любые связи между ними реализуются через идентификаторы событий.

---

### 2.3. Принцип версионности

Каждая логика расчёта и сценарий анализа имеют явную версию.

---

## 3. Основные сущности и их атрибуты

### 3.1. Subject

**Назначение:** анонимизированное описание испытуемого.

Атрибуты:

* subject_id (PK)
* sex
* age
* age_group (опционально)

---

### 3.2. TestSession

**Назначение:** единичный сеанс тестирования.

Атрибуты:

* session_id (PK)
* subject_id (FK)
* test_type
* phase (F1 / F2 / F3)
* session_datetime
* test_config_version

---

### 3.3. StimulusEvent

**Назначение:** единичное предъявление стимула.

Атрибуты:

* stimulus_event_id (PK)
* session_id (FK)
* stimulus_role (test / masking / intermediate)
* stimulus_color
* stimulus_location (left / center / right)
* stimulus_position_index
* psi_test
* psi_mask
* psi_transition
* background_id
* masking_pattern_id

---

### 3.4. ResponseEvent

**Назначение:** реакция на конкретный тестовый стимул.

Атрибуты:

* response_event_id (PK)
* stimulus_event_id (FK)
* rt
* validity_flag
* error_type

---

## 4. Производные сущности

### 4.1. ComponentTiming

**Назначение:** хранение компонентных временных показателей.

Атрибуты:

* component_timing_id (PK)
* stimulus_event_id (FK)
* delta_v1
* delta_v4
* delta_v5_mt
* computation_version
* filtering_params

---

### 4.2. AggregateMetrics

**Назначение:** агрегированные показатели.

Атрибуты:

* aggregate_id (PK)
* session_id (FK)
* aggregation_scope
* metric_name
* metric_value
* computation_version

---

## 5. Сущности дизайна теста

### 5.1. TestConfig

**Назначение:** описание конфигурации теста.

Атрибуты:

* test_config_id (PK)
* test_type
* color_set
* spatial_scheme
* psi_scheme
* masking_scheme
* background_scheme

---

### 5.2. BackgroundConfig

**Назначение:** параметры фона.

Атрибуты:

* background_id (PK)
* background_color
* background_dynamic_type
* background_contrast
* background_phase

---

### 5.3. MaskingPattern

**Назначение:** описание маскирующей последовательности.

Атрибуты:

* masking_pattern_id (PK)
* pattern_type
* pattern_description

---

## 6. Сценарный слой

### 6.1. ScenarioDefinition

Атрибуты:

* scenario_id (PK)
* scenario_code (A0.1, B1, C1.3, etc.)
* scenario_version
* scenario_description

---

### 6.2. ScenarioResult

Атрибуты:

* scenario_result_id (PK)
* scenario_id (FK)
* target_entity
* result_reference
* computation_version

---

## 7. Связи между сущностями (высокоуровнево)

* Subject 1—N TestSession
* TestSession 1—N StimulusEvent
* StimulusEvent 1—0..1 ResponseEvent
* StimulusEvent 1—0..1 ComponentTiming
* TestSession 1—N AggregateMetrics

---

## 8. Поддержка расширяемости

Модель допускает:

* добавление новых компонент времени;
* добавление новых типов стимулов;
* расширение параметров фона;
* добавление новых сценариев без изменения существующих таблиц.

---

## 9. Итоговая роль модели

Логическая модель v4 обеспечивает:

* полную трассируемость от стимула до сценарного вывода;
* методологическую чистоту (дизайн ≠ реакция);
* основу для физической реализации хранения (C2.2).

---

<!-- ================================================== -->
<!-- source: 11_2_C2_2_Physical_Storage_Design.md -->
<!-- ================================================== -->
<a id="doc-3-11_2_c2_2_physical_storage_design"></a>

# C2.2 — Физическая реализация хранения данных (Physical Storage Design v4)

## 1. Назначение документа

Документ описывает **физическую реализацию хранения данных** проекта *NeuroTransAnalytics* версии v4
на основе логической модели **C2.1**.

Цель:

* обеспечить реализуемость архитектуры на персональном компьютере (Windows 10);
* сохранить всю полноту данных без редукции;
* обеспечить удобство вычислений, визуализации и расширения проекта.

Документ **не содержит программного кода**, а фиксирует архитектурные решения хранения.

---

## 2. Общая стратегия хранения

Рекомендуется гибридная стратегия:

* **SQLite** — для событийных и реляционных данных;
* **Parquet** — для крупных массивов производных и агрегатов;
* **файловая иерархия** — для сценарных результатов и визуализаций.

Такой подход:

* минимизирует инфраструктурные требования;
* масштабируется от ноутбука до рабочей станции;
* поддерживает итеративный исследовательский процесс.

---

## 3. Реляционное хранилище (SQLite)

### 3.1. Назначение

SQLite используется для хранения:

* первичных событий;
* параметров дизайна тестов;
* метаданных и версий.

---

### 3.2. Основные таблицы

#### subjects

* subject_id (PK)
* sex
* age
* age_group

#### test_sessions

* session_id (PK)
* subject_id (FK)
* test_type
* phase
* session_datetime
* test_config_version

#### stimulus_events

* stimulus_event_id (PK)
* session_id (FK)
* stimulus_role
* stimulus_color
* stimulus_location
* stimulus_position_index
* psi_test
* psi_mask
* psi_transition
* background_id
* masking_pattern_id

#### response_events

* response_event_id (PK)
* stimulus_event_id (FK)
* rt
* validity_flag
* error_type

---

### 3.3. Таблицы дизайна

#### test_configs

* test_config_id (PK)
* test_type
* color_set
* spatial_scheme
* psi_scheme
* masking_scheme
* background_scheme

#### background_configs

* background_id (PK)
* background_color
* background_dynamic_type
* background_contrast
* background_phase

#### masking_patterns

* masking_pattern_id (PK)
* pattern_type
* pattern_description

---

## 4. Хранение производных данных

### 4.1. ComponentTiming (Parquet)

Хранится в виде Parquet-файлов:

* delta_v1
* delta_v4
* delta_v5_mt
* computation_version
* filtering_params
* stimulus_event_id

Разделение:

* по версии расчёта;
* по типу теста;
* по дате расчёта.

---

### 4.2. AggregateMetrics (Parquet)

Хранит:

* агрегаты с указанием области агрегации;
* версии алгоритмов;
* ссылки на исходные события.

---

## 5. Сценарный слой хранения

### 5.1. Структура каталогов

```
data/
  raw/
  sqlite/
    neurotransanalytics_v4.db
  derived/
    component_timing/
    aggregates/
  scenarios/
    A0/
    A1/
    A2/
    B1/
    B2/
    C/
```

---

### 5.2. Сценарные результаты

Для каждого сценария:

* отдельный каталог;
* сохранение промежуточных данных;
* экспорт визуализаций;
* файл описания версии сценария.

---

## 6. Версионность и воспроизводимость

Фиксируется:

* версия базы данных;
* версия логической модели;
* версия сценариев;
* версия расчётных алгоритмов.

Никакие данные не перезаписываются без смены версии.

---

## 7. Производительность и масштабирование

Архитектура рассчитана на:

* десятки миллионов событий;
* пакетную обработку;
* интерактивный анализ агрегатов.

Используются:

* индексы в SQLite;
* колоночное хранение Parquet;
* кэширование сценарных выборок.

---

## 8. Резервное копирование и переносимость

Рекомендуется:

* регулярное резервное копирование SQLite;
* хранение Parquet-файлов как неизменяемых артефактов;
* переносимость проекта целиком через файловую структуру.

---

## 9. Итоговая роль документа

Документ C2.2 обеспечивает:

* физическую реализуемость архитектуры v4;
* согласованность с методологией C1;
* основу для реализации вычислительных пайплайнов (C3).

---

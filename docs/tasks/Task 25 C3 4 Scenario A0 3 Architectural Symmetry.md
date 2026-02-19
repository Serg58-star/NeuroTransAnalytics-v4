# Task 25 — C3.4 Scenario A0.3: Architectural Symmetry (ΔV1)

## 1. Статус задачи

Уровень: C3.4 — Scenario Engine
Сценарий: A0.3 — Architectural Symmetry (ΔV1)
Версия сценария: v4.0.0
Тип задачи: Расширение Scenario Engine без изменения C3.1–C3.3

---

## 2. Цель задачи

Реализовать сценарий A0.3, направленный на структурный анализ пространственной симметрии базовой компоненты ΔV1.

Сценарий исследует различия ΔV1 между:

* левым полем (left),
* центральным полем (center),
* правым полем (right).

Сценарий выполняет только структурное сопоставление без:

* физиологической интерпретации,
* нейролокализации,
* пороговой классификации,
* кластеризации,
* нормализации.

---

## 3. Архитектурные ограничения

### 3.1 Разрешено

Изменения допустимы только в пределах:

* src/core/scenario_definitions/
* src/core/scenario_engine/
* механизма экспорта Parquet-артефактов

### 3.2 Запрещено

* Изменять C3.1 (ETL)
* Изменять C3.2 (Component Timing)
* Изменять C3.3 (QC & Aggregation)
* Пересчитывать QC
* Модифицировать raw-данные
* Выполнять вычисления в GUI

---

## 4. Вычислительная спецификация C3.4

### 4.1 Входные данные

Используются данные слоя C3.3 (AggregatedFrame).

Фильтр:

```
test_type = "Tst1"
technical_qc_flag = False
```

Необходимо использовать поле пространственной локализации стимула:

```
stimulus_location ∈ {left, center, right}
```

### 4.2 Уровень агрегирования

1. Первичная агрегация — на уровне:

```
subject_id
stimulus_location
```

2. Вторичная агрегация — формирование симметричных структур:

Для каждого субъекта формируются:

* median_left

* median_center

* median_right

* mad_left

* mad_center

* mad_right

* iqr_left

* iqr_center

* iqr_right

### 4.3 Производные структурные показатели

Разрешено вычислять только прямые разности:

* diff_left_right = median_left − median_right
* diff_left_center = median_left − median_center
* diff_right_center = median_right − median_center

Запрещено:

* нормализация разностей
* процентные различия
* z-score
* направление доминантности
* пороговая маркировка асимметрии

---

## 5. Структура выходного артефакта

Файл:

```
data/derived/scenarios/A0_3.parquet
```

### 5.1 Формат

* Parquet
* engine="fastparquet"
* index=False
* CSV fallback запрещён

### 5.2 Поля артефакта

| Поле                   | Тип    |
| ---------------------- | ------ |
| subject_id             | int    |
| median_left            | float  |
| median_center          | float  |
| median_right           | float  |
| mad_left               | float  |
| mad_center             | float  |
| mad_right              | float  |
| iqr_left               | float  |
| iqr_center             | float  |
| iqr_right              | float  |
| diff_left_right        | float  |
| diff_left_center       | float  |
| diff_right_center      | float  |
| scenario_code          | string |
| scenario_version       | string |
| etl_version            | string |
| component_algo_version | string |
| qc_version             | string |

### 5.3 Свойства артефакта

* Immutable
* Deterministic
* Reproducible
* Versioned
* Явная сортировка по subject_id перед сохранением

---

## 6. GUI (C3.5) — ограничения

### 6.1 Разрешено

Добавить вкладку A0.3 с:

* таблицей субъектов
* scatter plot:

  * X = diff_left_right
  * Y = median_center
* boxplot распределений median_left, median_center, median_right

### 6.2 Запрещено

* вычислять дополнительные метрики в GUI
* нормализовать данные
* классифицировать асимметрию
* выделять «аномалии»
* формировать выводы

GUI только отображает A0_3.parquet.

---

## 7. Проверка архитектурной целостности

Сценарий A0.3:

* не изменяет ΔV1
* не вмешивается в компонентный расчёт
* не нарушает C3.1–C3.3
* не выполняет интерпретацию
* не создаёт cross-layer зависимостей

---

## 8. Критерии завершения Task 25

Task 25 считается завершённой после:

1. Корректной генерации A0_3.parquet
2. Подтверждения engine="fastparquet"
3. Подтверждения сортировки по subject_id
4. Подтверждения использования централизованного реестра версий
5. Архитектурного аудита перед merge

---

Статус после реализации: ожидает аудита.

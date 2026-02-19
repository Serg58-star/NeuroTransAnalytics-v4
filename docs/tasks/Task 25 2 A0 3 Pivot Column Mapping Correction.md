# Task 25.2 — A0.3 Pivot & Column Mapping Correction

## 1. Статус

Уровень: C3.4 — Scenario Engine
Сценарий: A0.3 — Architectural Symmetry (ΔV1)
Тип задачи: Исправление логики pivot и структуры выходного артефакта
Версия после исправления: scenario_v4.0.2

---

## 2. Основание для задачи

В текущей реализации A0.3 выявлены критические дефекты:

1. Некорректное flattening MultiIndex после pivot.
2. Автоматическое создание нулевых колонок при отсутствии совпадения имён.
3. В результате все diff-показатели могут становиться равными 0.
4. Таблицы перегружены metadata-полями (версии), что нарушает требование представления структурных данных.

Настоящая задача устраняет указанные дефекты.

---

## 3. Обязательные изменения

### 3.1 Удаление version-полей из сценарных таблиц

Из всех сценарных Parquet-артефактов (A0.x) убрать поля:

* scenario_version
* etl_version
* component_algo_version
* qc_version

Допускается сохранение versioning исключительно во внутреннем pipeline-логировании.

Сценарные таблицы должны содержать только:

* структурные вычисленные показатели
* идентификаторы (subject_id, session_id при необходимости)
* scenario_code

---

### 3.2 Строгий mapping MultiIndex → ожидаемые имена

После выполнения pivot:

```
pivot(index='subject_id', columns='stimulus_location', values=[...])
```

Обязательная логика:

1. Явное перечисление ожидаемых пар (metric, location):

   * ('median_ΔV1', 'left')   → median_left
   * ('median_ΔV1', 'center') → median_center
   * ('median_ΔV1', 'right')  → median_right
   * ('mad_ΔV1', 'left')      → mad_left
   * ('mad_ΔV1', 'center')    → mad_center
   * ('mad_ΔV1', 'right')     → mad_right
   * ('iqr_ΔV1', 'left')      → iqr_left
   * ('iqr_ΔV1', 'center')    → iqr_center
   * ('iqr_ΔV1', 'right')     → iqr_right

2. Запрещено использовать автоматическое `.lower()`, `.replace()` или любые строковые трансформации без строгого соответствия.

3. Если ожидаемая пара отсутствует — колонка создаётся как NaN, а не 0.0.

---

### 3.3 Запрет на автоматическое создание нулевых колонок

Удалить полностью следующий паттерн:

```
if col not in pivot.columns:
    pivot[col] = 0.0
```

Нули маскируют ошибки pivot и делают diff статистически ложными.

Разрешено:

* сохранять NaN при отсутствии данных;
* либо выбрасывать исключение при отсутствии обязательных колонок.

---

### 3.4 Unit-check: контроль нулевой симметрии

Добавить обязательную проверку после расчёта diff:

```
if all(diff_left_right == 0) and \
   all(diff_left_center == 0) and \
   all(diff_right_center == 0):
       raise ValueError("A0.3 symmetry collapse: all diffs are zero. Check pivot mapping.")
```

Цель:

* предотвратить молчаливое распространение дефектных данных;
* обеспечить fail-fast поведение.

---

## 4. Требования к A0_3.parquet

Файл должен содержать только:

| Поле              | Тип    |
| ----------------- | ------ |
| subject_id        | int    |
| median_left       | float  |
| median_center     | float  |
| median_right      | float  |
| mad_left          | float  |
| mad_center        | float  |
| mad_right         | float  |
| iqr_left          | float  |
| iqr_center        | float  |
| iqr_right         | float  |
| diff_left_right   | float  |
| diff_left_center  | float  |
| diff_right_center | float  |
| scenario_code     | string |

* Явная сортировка по subject_id.
* engine="fastparquet".
* index=False.

---

## 5. GUI ограничения

1. GUI отображает только структурные поля.
2. Версионные данные не выводятся в таблицах.
3. Если diff содержат NaN — отображать как NaN, не заменять нулями.
4. Если unit-check вызывает ошибку — GUI должен показать сообщение об ошибке, а не пустой график.

---

## 6. Критерии завершения

Task 25.2 считается завершённой после:

1. Корректной регенерации A0_3.parquet.
2. Подтверждения отсутствия version-полей в таблицах.
3. Подтверждения ненулевых diff при наличии асимметрии.
4. Успешного прохождения unit-check.

---

Статус после выполнения: A0.3 функционально корректен и пространственно валиден.

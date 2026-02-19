# Task 25.3 — Spatial Refactor of A0.0 and A0.1 + Removal of Redundant Columns

## 1. Статус

Уровень: C3.4 — Scenario Engine
Затрагиваемые сценарии: A0.0 (Baseline Stability), A0.1 (Variability Profile)
Тип задачи: Архитектурная гармонизация после C3 v4.0.1 Extension
Версия после исправления: scenario_v4.0.3

---

## 2. Основание для задачи

После перехода C3 к версии v4.0.1 (Spatially-Extended Contract):

* AggregatedFrame содержит stimulus_location как обязательное измерение;
* A0.3 корректно использует spatial dimension;
* A0.0 и A0.1 продолжают схлопывать spatial dimension;
* scenario_code дублируется в каждой строке и не несёт информации.

Это создаёт архитектурную несогласованность внутри A0-блока.

Настоящая задача устраняет указанную несогласованность.

---

## 3. Удаление избыточных колонок

### 3.1 Удалить из всех A0.x parquet-артефактов:

* scenario_code

Версионная информация остаётся только во внутреннем логировании пайплайна.

Ни одна таблица A0.x не должна содержать служебные version-поля.

---

## 4. Пространственный рефакторинг A0.0

### 4.1 Текущая проблема

A0.0 агрегирует данные на уровне session_id, игнорируя stimulus_location.

### 4.2 Новая спецификация

A0.0 должен отражать baseline ΔV1 по каждому полю зрения.

Выходная структура (на уровне session):

| Поле               | Тип   |
| ------------------ | ----- |
| subject_id         | int   |
| session_id         | int   |
| count_valid_left   | int   |
| count_valid_center | int   |
| count_valid_right  | int   |
| median_left        | float |
| median_center      | float |
| median_right       | float |
| mad_left           | float |
| mad_center         | float |
| mad_right          | float |
| iqr_left           | float |
| iqr_center         | float |
| iqr_right          | float |

### 4.3 Запрещено

* схлопывать spatial dimension;
* усреднять left/center/right;
* выводить "общую" baseline строку без spatial breakdown.

---

## 5. Пространственный рефакторинг A0.1

### 5.1 Новая спецификация

A0.1 должен отражать variability ΔV1 по каждому полю зрения.

Выходная структура (на уровне session):

| Поле                   | Тип   |
| ---------------------- | ----- |
| subject_id             | int   |
| session_id             | int   |
| variability_mad_left   | float |
| variability_mad_center | float |
| variability_mad_right  | float |
| variability_iqr_left   | float |
| variability_iqr_center | float |
| variability_iqr_right  | float |

### 5.2 Запрещено

* объединять поля зрения;
* создавать "общую" variability без spatial breakdown.

---

## 6. Fail-fast контроль

После фильтрации Tst1 в A0.0 и A0.1 добавить обязательную проверку:

```
if 'stimulus_location' not in df.columns:
    raise ValueError("Spatial dimension missing in AggregatedFrame (v4.0.1 required)")
```

Дополнительно:

Если для любой session_id отсутствует хотя бы одна из трёх позиций (left, center, right):

* НЕ заполнять нулями;
* либо оставлять NaN;
* либо выбрасывать исключение (предпочтительно).

---

## 7. Требования к Parquet-артефактам

* engine="fastparquet"
* index=False
* явная сортировка по subject_id, session_id
* отсутствие служебных колонок

---

## 8. GUI требования

1. Таблицы должны отображать spatial breakdown.
2. Графики должны строиться отдельно для left / center / right.
3. Запрещено скрытое усреднение в GUI.
4. При отсутствии spatial dimension — показывать ошибку, а не пустую таблицу.

---

## 9. Критерии завершения

Task 25.3 считается завершённой после:

1. Регенерации A0_0.parquet и A0_1.parquet.
2. Подтверждения отсутствия scenario_code во всех A0.x.
3. Подтверждения spatial breakdown в A0.0 и A0.1.
4. Успешного прохождения fail-fast проверок.

---

Статус после выполнения: A0-блок полностью spatial-aware и архитектурно согласован с C3 v4.0.1.

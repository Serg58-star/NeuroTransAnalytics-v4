# C3 Status Update — v4.0.1

## 1. Предыдущий статус

C3 Subsystem Status (v4.0.0):

✔ Stable
✔ Deterministic
✔ Observable
✔ Parquet-restored
✔ Layout-canonical

---

## 2. Новый статус

После контролируемого расширения C3.3 (включение spatial dimension в AggregatedFrame):

C3 Subsystem Status (v4.0.1):

✔ Deterministic
✔ Observable
✔ Parquet-restored
✔ Layout-canonical
✔ Spatially-extended

Изменение статуса:

Stable → Extended (v4.0.1)

---

## 3. Обоснование

Расширение агрегирования по `stimulus_location` необходимо для корректной реализации пространственных сценариев уровня A0.

Расширение:

* не изменяет алгоритмы расчёта компонент;
* не меняет QC-политику;
* не вводит новые вычислительные слои;
* не нарушает детерминированность;
* не нарушает контракт хранения (Parquet only, fastparquet).

---

## 4. Инварианты остаются действующими

1. ΔV1 = RT_Tst1 (до tapping-интеграции);
2. GUI не выполняет вычислений;
3. Scenario Engine не выполняет интерпретацию;
4. Нет cross-layer импортов;
5. Нет скрытых дефолтов;
6. Воспроизводимость обязательна.

---

## 5. Дальнейшая работа

После регенерации derived-слоя и подтверждения корректности A0.0–A0.2:

Продолжить реализацию A0.3 на расширенном контракте.

---

Статус обновлён: C3 v4.0.1 (Extended).

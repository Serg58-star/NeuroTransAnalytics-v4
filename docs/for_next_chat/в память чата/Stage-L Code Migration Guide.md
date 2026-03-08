# Stage-L Code Migration Guide

## Перевод аналитического кода Stage-L с RT на компонентные переменные (ΔV4 / ΔV5-MT)

Project: **NeuroTransAnalytics v4**
Layer: **Stage-L — Legacy Structural Analysis**
Purpose: **перенаправление существующего кода анализа с RT на компонентную архитектуру реакции**

---

# 1. Назначение документа

Документ описывает **практический процесс миграции существующего аналитического кода** Stage-L.

В текущем виде код Stage-L:

* анализирует **RT**
* использует таблицы вида:

```
reactions_view
```

где основной переменной анализа является:

```
rt
```

После миграции анализ должен выполняться **только на компонентных переменных**:

```
delta_v4
delta_v5_mt
```

RT остаётся **только промежуточной величиной**, используемой для вычисления компонент.

---

# 2. Общая стратегия миграции

Миграция выполняется **без переписывания аналитических алгоритмов**.

Изменяется только:

* источник данных
* переменная анализа

---

## До миграции

```
SQL → reactions_view
        column: rt

Python → analysis(rt)
```

---

## После миграции

```
SQL → component_view
        columns:
            delta_v4
            delta_v5_mt

Python → analysis(delta_v4)
Python → analysis(delta_v5_mt)
```

---

# 3. Этап 1 — создание SQL-представления компонент

Необходимо создать SQL-view:

```
component_view
```

---

## Пример SQL

```sql
CREATE VIEW component_view AS
SELECT
    r.subject_id,
    r.session_id,
    r.test_type,
    r.psi,
    r.field,
    r.stimulus_index,

    r.rt,

    c.delta_v1,
    c.delta_v4,
    c.delta_v5_mt

FROM reactions_view r
LEFT JOIN component_timing c
ON r.stimulus_event_id = c.stimulus_event_id;
```

---

# 4. Этап 2 — замена источника данных в Python

Старый код:

```python
df = pd.read_sql(
    "SELECT * FROM reactions_view",
    conn
)
```

Новый код:

```python
df = pd.read_sql(
    "SELECT * FROM component_view",
    conn
)
```

---

# 5. Этап 3 — замена переменной анализа

## Старый код

```python
rt = df["rt"]
```

---

## Новый код

### для цветовой архитектуры

```python
x = df["delta_v4"]
```

---

### для двигательной архитектуры

```python
x = df["delta_v5_mt"]
```

---

# 6. Этап 4 — обновление визуализаций

## Старый код

```python
sns.histplot(df["rt"])
plt.title("RT distribution")
```

---

## Новый код

### ΔV4

```python
sns.histplot(df["delta_v4"])
plt.title("ΔV4 distribution")
```

---

### ΔV5/MT

```python
sns.histplot(df["delta_v5_mt"])
plt.title("ΔV5/MT distribution")
```

---

# 7. Этап 5 — обновление группировок

## Старый код

```python
df.groupby("psi")["rt"].mean()
```

---

## Новый код

### цветовая архитектура

```python
df.groupby("psi")["delta_v4"].mean()
```

---

### двигательная архитектура

```python
df.groupby("psi")["delta_v5_mt"].mean()
```

---

# 8. Этап 6 — обновление автокорреляций

## Старый код

```python
series = df["rt"]
acf = sm.tsa.acf(series)
```

---

## Новый код

```python
series = df["delta_v4"]
acf = sm.tsa.acf(series)
```

или

```python
series = df["delta_v5_mt"]
acf = sm.tsa.acf(series)
```

---

# 9. Этап 7 — обновление регрессионных моделей

## Старый код

```python
model = sm.OLS(df["rt"], X).fit()
```

---

## Новый код

### цветовая архитектура

```python
model = sm.OLS(df["delta_v4"], X).fit()
```

---

### двигательная архитектура

```python
model = sm.OLS(df["delta_v5_mt"], X).fit()
```

---

# 10. Этап 8 — обновление экспортируемых таблиц

## Старый CSV

```
psi
rt_mean
rt_sd
```

---

## Новый CSV

```
psi
delta_v4_mean
delta_v4_sd
delta_v5_mt_mean
delta_v5_mt_sd
```

---

# 11. Этап 9 — обновление отчётов

В отчётах Stage-L необходимо заменить:

```
RT
```

на

```
ΔV4
ΔV5/MT
```

Пример:

Было:

```
RT distribution by PSI
```

Стало:

```
ΔV4 distribution by PSI
ΔV5/MT distribution by PSI
```

---

# 12. Контроль корректности миграции

После миграции необходимо проверить:

### 1. отсутствие RT-анализа

В коде Stage-L **не должно быть**:

```
analysis(rt)
```

---

### 2. корректность компонент

Проверка:

```
RT ≈ ΔV1 + ΔV4
RT ≈ ΔV1 + ΔV5/MT
```

---

### 3. отсутствие отрицательных компонент

```
delta_v4 ≥ 0
delta_v5_mt ≥ 0
```

---

# 13. Результат миграции

После выполнения миграции Stage-L:

* использует **компонентную архитектуру**
* анализирует:

```
ΔV4
ΔV5/MT
```

* полностью соответствует методологии проекта NeuroTransAnalytics.

---

# 14. Принцип работы Stage-L после миграции

Stage-L становится **component-level analysis stage**.

Объект анализа:

```
ΔV4
ΔV5/MT
```

RT используется только:

```
RT → component extraction
```

и больше не участвует в аналитических процедурах.

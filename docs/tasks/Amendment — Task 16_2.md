# Audit — C3.1 ETL v4.1.1
**File:** etl_v4.py  
**Walkthrough:** Walkthrough.md  
**Branch:** feature/task-16-real-data-integration  
**Status:** Approved with Mandatory Fix  

---

## 1. Общая архитектурная оценка

Файл: :contentReference[oaicite:0]{index=0}  
Walkthrough: :contentReference[oaicite:1]{index=1}  

### Положительные аспекты

✔ Read-only подключение к SQLite (mode=ro)  
✔ MIN_RT_MS вынесен в архитектурную константу  
✔ trial_id корректно переименован в session_id  
✔ age и sex включены в EventFrame  
✔ 108 событий на сессию подтверждено  
✔ Нет cross-layer импортов  
✔ Нет вычислений C3.2 / C3.3 / C3.4  
✔ Нет интерпретаций  

Слой C3.1 концептуально реализован корректно.

---

## 2. Критическое замечание — NaN в rt_ms

В `_validate_integrity` выполняется:

```python
df.loc[df['rt_ms'] < MIN_RT_MS, 'technical_qc_flag'] = False

Однако отсутствует проверка:

df['rt_ms'].isna()

Если RT = NaN, запись останется technical_qc_flag = True.

Это методологическая ошибка.

Обязательное исправление:

Добавить:

df.loc[df['rt_ms'].isna(), 'technical_qc_flag'] = False

до пороговой проверки.

3. Методологическое замечание — вычисление возраста

Возраст вычисляется через:

event_frame.apply(..., axis=1)

Это:

корректно логически

но неэффективно вычислительно

не критично на текущем объёме данных

Архитектурного нарушения нет.

Допустимо оставить.

4. Потенциальная методологическая неоднозначность

Функция _calculate_age возвращает 0 при ошибке:

except:
    return 0

Это может маскировать:

отсутствие birth_date

некорректный формат

Лучше:

return None

и далее маркировать QC.

Но это не блокирующее замечание.

5. QC по субъекту

Добавлено:

df.loc[~df['subject_id'].isin(valid_subject_ids), 'technical_qc_flag'] = False

Это корректно.

6. Количественная проверка

Walkthrough сообщает:

204,336 событий

1,892 сессии

108 событий на сессию

✔ Арифметически корректно
✔ Нормализация выполнена правильно

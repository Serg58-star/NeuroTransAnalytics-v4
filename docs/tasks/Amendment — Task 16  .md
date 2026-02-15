# Amendment — Task 16  
## Inclusion of Subject Attributes (age / sex) in EventFrame

**Project:** NeuroTransAnalytics-v4  
**Layer:** C3.1 — ETL  
**Branch:** feature/task-16-real-data-integration  
**Status:** Mandatory Fix  
**Reason:** Prevent loss of subject-level analytical axes  

---

## 1. Архитектурное основание

Согласно логической модели v4 (C2.1):

- Subject является самостоятельной сущностью;
- возраст и пол являются модифицирующими осями;
- демографические оси используются в сценариях уровня D и C.

Удаление этих атрибутов на этапе ETL приводит к искусственному обеднению модели.

ETL обязан формировать полноценную событийную структуру,
а не минимально достаточную.

---

## 2. Требуемое изменение

### 2.1 Extract

`users` уже извлекается в:

```python
users_df = self._extract_users(conn)

Это корректно.

2.2 Transform — обязательный шаг

В _build_event_frame необходимо:

Выполнить merge EventFrame с users_df по subject_id.

Добавить в EventFrame поля:

| Field | Type |
| ----- | ---- |
| age   | int  |
| sex   | str  |

Если возраст хранится как birth_date,
то допускается:

либо вычисление возраста на лету,

либо включение birth_date как есть.

Предпочтительно включить оба поля:

birth_date

age (если уже существует в БД)

ETL не выполняет демографическую интерпретацию,
он лишь переносит данные.

3. Обновлённая структура EventFrame

EventFrame обязан содержать:
| Field             | Type       |
| ----------------- | ---------- |
| subject_id        | int        |
| session_id        | int        |
| age               | int        |
| sex               | str        |
| test_type         | str        |
| stimulus_index    | int        |
| rt_ms             | float      |
| psi_pre_ms        | int        |
| stimulus_color    | str / None |
| stimulus_location | str / None |
| technical_qc_flag | bool       |

4. Архитектурные ограничения

Merge выполняется строго по subject_id.

Если субъект отсутствует в users,
technical_qc_flag = False.

Никаких демографических фильтраций.

Никаких возрастных группировок.

Никакой интерпретации.

5. Запрещено

Удалять extract_users.

Игнорировать демографические поля.

Делать демографический QC.

Делать агрегацию по полу или возрасту.

6. Definition of Done

Исправление считается выполненным, если:

EventFrame содержит age и sex.

Количество строк не изменилось.

Merge не нарушает 108 событий на сессию.

Нет cross-layer импортов.

Реализация остаётся детерминированной.

7. Версия

После внесения изменения:

ETL version → etl_v4.1.1

Commit обязателен перед переходом к Task 17.


---

После внесения этого изменения я проведу повторный аудит файла.

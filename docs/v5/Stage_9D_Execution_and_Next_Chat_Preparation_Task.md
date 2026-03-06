# NeuroTransAnalytics v5
# Stage 9D — Execution & Next Chat Preparation Task

## Режим
GoAn — Программирование + Структурный аудит + Подготовка документации

Интерпретации запрещены.
Изменение Core запрещено.
Статистический анализ Stage 9D.2 запрещён на этом этапе.

---

# I. Входной документ

Обязательный к исполнению:

Stage_9D_Population_Differentiation_Audit (v3).md

Следовать строго структуре 9D.0 → 9D.1 → 9D.2.
На текущем этапе разрешено выполнить только 9D.0.

---

# II. Stage 9D.0 — SQLite Schema Audit

## 1. Подключиться к базе:

neuro_data.db

## 2. Выполнить:

SELECT name FROM sqlite_master WHERE type='table';

Для каждой таблицы:

PRAGMA table_info(table_name);

## 3. Определить (без предположений):

- таблицу субъектов
- таблицу тестов
- таблицу демографии
- идентификатор субъекта
- поле пола
- кодировку пола
- поля, позволяющие вычислить возраст
- формат даты
- наличие множественных тестов

## 4. Построить join-логику.

---

# III. Deliverables Stage 9D.0

Создать:

/docs/Stage_9D_SQLite_Schema_Audit_Report.md

Включить:

- список таблиц
- структуру таблиц
- диаграмму связей
- список ключевых полей
- вывод о возможности вычисления возраста
- описание кодировки пола

Статистические выводы запрещены.

---

# IV. Подготовка к следующему чату Testing_RT

## 1. Создать каталог:

/docs/for_next_chat

## 2. Скопировать в него:

A. Stage_9D_Population_Differentiation_Audit (v3).md
B. Stage_9D_SQLite_Schema_Audit_Report.md
C. Stage_10_Real_Data_Pilot_Readiness_Protocol.md
D. Protocol_Roles_and_Working_Model_NeuroTransAnalytics_v4.md
E. v5_Synthetic_Architecture_Completion_Summary.md
F. Task_50A_Z_Space_Geometric_Validation_Criteria_Update.md
G. Task_51A_Z_Space_Severity_Centering_Correction.md
H. Task_52A_Anchored_Projection_Framework_for_Phase_2_Dynamics.md
I. Stage_9B_Functional_Monitoring_Framework_v5.md
J. Stage_9B_Functional_Monitoring_Report.md
K. Stage_9_PreAudit_Task_Report.md

Дополнительно включить другие документы,
если они необходимы для понимания Z-space и Severity,
но не более 23 файлов суммарно.

Файлы со Skills не добавлять.

---

# V. Создать индекс-файл

/docs/for_next_chat/FILES_FOR_STAGE_9D_NEXT_CHAT.md

С указанием:

- Названия файла
- Исходного расположения
- Причины включения
- Обязателен ли

---

# VI. Указать, что нужно продублировать в чат

В отдельном разделе указать:

Какие формулы и фиксированные параметры
нужно вставить прямо в первый промпт следующего чата.

Минимально:

- Severity формула
- Anchored Projection формула
- ΔZ формула
- κ = 0.08
- Anchored thresholds (если применимо)
- PASS/FAIL критерии Stage 9D

---

# VII. Запрещено

- Выполнять Stage 9D.2
- Делать выводы
- Строить регрессии
- Делать корреляции
- Интерпретировать структуру данных

---

# VIII. Результат

После завершения:

Проект должен быть готов
к переходу в следующий чат Testing_RT,
где будет выполнен Stage 9D.1 и Stage 9D.2.
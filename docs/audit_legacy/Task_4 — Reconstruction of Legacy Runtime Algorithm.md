# Task_4 — Reconstruction of Legacy Runtime Algorithm

*(Delphi → Formal Algorithm)*

Executor: **GoAn**
Mode: **Algorithm Reconstruction / Technical Analysis**
Project: **NeuroTransAnalytics-v4 / Testing_RT**

---

# 1. Цель задачи

На основе пакета legacy-документов, размещенного в:

```
C:\NeuroTransAnalytics-v4\docs\for_next_chat
```

необходимо реконструировать **точный runtime-алгоритм выполнения legacy тестов зрительных реакций**.

Результатом должна стать **формальная алгоритмическая модель теста**, независимая от Delphi.

---

# 2. Почему выполняется реконструкция

Реконструкция выполняется **не ради исторического анализа**.

Она необходима для:

```
1. корректной интерпретации данных базы boxbase
2. построения data-adapter (C2.1 → C3.1)
3. формирования StimulusEvent / ResponseEvent
4. разработки reference simulator legacy теста
5. обеспечения воспроизводимости анализа
```

Алгоритм станет **канонической моделью поведения legacy системы**.

---

# 3. Источники для реконструкции

Использовать **только документы из пакета**:

```
docs\for_next_chat
```

Основные источники:

* Legacy_Module_Index.md
* Legacy_Source_File_Index.md
* Delphi_Project_Structure.md
* Stimulus_Code_Extracts.md
* Response_Handling_Code.md
* Result_Processing_Code.md
* config_full_index.md
* config_sections.md
* config_stimulus_parameters.md
* config_timing_parameters.md
* Appendix_A_Data_and_Legacy_Context.md

Дополнительно:

* Protocol_Architecture_Alignment_v4.md

---

# 4. Требуемая глубина реконструкции

Необходимо восстановить:

## 4.1 State Machine теста

Полную последовательность состояний системы:

```
INIT
↓
LOAD_CONFIG
↓
WARMUP
↓
WAIT_PSI
↓
SHOW_STIMULUS
↓
WAIT_RESPONSE
↓
REGISTER_RESPONSE
↓
NEXT_TRIAL
↓
END_TEST
```

---

## 4.2 Алгоритм генерации стимулов

Определить:

* порядок стимулов
* выбор цвета
* выбор позиции
* использование таблиц стимулов
* использование config.ini

---

## 4.3 Timing алгоритм

Реконструировать:

```
PSI
stimulus duration
timer behaviour
rotation cycles
```

Используя:

* config_timing_parameters
* Delphi timer functions.

---

## 4.4 Обработку ответов

Определить:

* момент регистрации ответа
* обработку преждевременных нажатий
* обработку опозданий
* правила завершения стимульной серии.

---

## 4.5 Алгоритм записи результатов

Реконструировать:

```
WriteResults()
```

Определить:

* какие данные записываются
* структура файлов
* соответствие полям boxbase.

---

## 4.6 Алгоритм повторов при выбросах

Определить:

* когда активируется повтор
* как определяется CV
* как вставляется повторная попытка.

---

# 5. Формат результата

Создать документ:

```
LEGACY_RUNTIME_ALGORITHM.md
```

Структура документа:

```
# Legacy Runtime Algorithm

1. System Overview

2. Runtime State Machine

3. Stimulus Generation

4. Timing System

5. Response Handling

6. Result Recording

7. Outlier Handling

8. Formal Algorithm (pseudocode)
```

---

# 6. Требование формализации

В конце документа должен быть представлен **полный псевдокод теста**.

Пример формата:

```
FOR trial = 1..36

  wait PSI[trial]

  show stimulus

  start timer

  wait response OR timeout

  register reaction time

END
```

Псевдокод должен отражать **реальное поведение legacy системы**.

---

# 7. Ограничения

Запрещено:

```
интерпретировать физиологию
предлагать улучшения системы
изменять алгоритм
```

Разрешено:

```
восстанавливать
формализовать
сопоставлять код и документы
```

---

# 8. Проверка корректности

После реконструкции необходимо ответить:

1️⃣ Какие элементы алгоритма подтверждены документами
2️⃣ Какие элементы реконструированы косвенно
3️⃣ Какие элементы остаются неизвестными

Ответ добавить в конец документа.

---

# 9. Критерий завершения задачи

Задача считается выполненной, если:

```
legacy тест можно воспроизвести
исключительно по формальному алгоритму
без обращения к Delphi-коду
```

---

# 10. Назначение результата

Документ станет основой для:

```
data-adapter v0
Scenario Engine
reference simulator legacy теста
```

и будет использоваться во всех последующих этапах проекта.

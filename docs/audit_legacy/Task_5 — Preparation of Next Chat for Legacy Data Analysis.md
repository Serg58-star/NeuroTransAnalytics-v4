# Task_5 — Preparation of Next Chat for Legacy Data Analysis

Executor: GoAn
Project: NeuroTransAnalytics-v4 / Testing_RT

---

# 1. Цель задачи

Подготовить контекстный пакет документов для продолжения анализа legacy-системы в следующем чате проекта.

Следующий этап работы — **анализ реальных legacy-данных**.

---

# 2. Источник legacy-данных

В проекте NeuroTransAnalytics-v4 используется база:

```
neuro_data.db
```

Важно:

```
neuro_data.db является преобразованной копией legacy-базы Boxbase.
```

Следовательно:

```
legacy data source = neuro_data.db
```

Все анализы legacy-данных должны выполняться именно на этой базе.

---

# 3. Область поиска документов

Основной каталог:

```
C:\NeuroTransAnalytics-v4\docs\audit_legacy
```

Дополнительно:

```
C:\NeuroTransAnalytics-v4\docs\legacy
C:\NeuroTransAnalytics-v4\docs\audit
```

---

# 4. Задача GoAn

GoAn должен:

1. Найти документы, необходимые для анализа legacy-системы.
2. Отобрать минимальный, но достаточный набор.
3. Скопировать их в каталог:

```
C:\NeuroTransAnalytics-v4\docs\for_next_chat
```

Ограничение:

```
не более 24 файлов
```

---

# 5. Приоритет документов

## stimulus protocol

```
config_sequence_data.md
config_stimulus_parameters.md
config_timing_parameters.md
config_sections.md
config_full_index.md
```

---

## reconstructed runtime algorithm

```
LEGACY_RUNTIME_ALGORITHM.md
```

---

## code extracts

```
Stimulus_Code_Extracts.md
Response_Handling_Code.md
Result_Processing_Code.md
```

---

## architecture

```
Legacy_Source_File_Index.md
Legacy_Module_Index.md
Delphi_Project_Structure.md
```

---

## research context

```
Appendix_A_Data_and_Legacy_Context.md
Protocol_Architecture_Alignment_v4.md
1_Research_Paradigm_NeuroTransAnalytics.md
```

---

# 6. Индекс контекста

Создать файл:

```
LEGACY_ANALYSIS_CONTEXT_INDEX.md
```

со структурой:

```
Stimulus protocol
Runtime algorithm
Code extracts
Legacy architecture
Research context
Data source (neuro_data.db)
```

---

# 7. Проверка пакета

Перед копированием GoAn должен:

* удалить дубликаты
* оставить наиболее полные версии файлов.

---

# 8. Подготовка нового чата

GoAn должен создать файл:

```
NEXT_CHAT_START_BLOCK.md
```

который будет содержать:

* список файлов для загрузки
* краткое описание текущего состояния проекта.

---

# 9. Ограничения

GoAn **не должен**:

* анализировать данные
* строить гипотезы
* модифицировать документы.

GoAn должен только:

```
искать
отбирать
копировать
индексировать
```

---

# 10. Назначение задачи

Подготовить компактный пакет контекста для следующего этапа:

```
Legacy Data Pattern Verification
```

с использованием базы:

```
neuro_data.db (converted Boxbase)
```

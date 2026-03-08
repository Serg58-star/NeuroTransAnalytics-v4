# 2_Stage G — Уточнение архитектуры каналов
## NeuroTransAnalytics v5 — Generator Research Layer

Исполнитель: GoAn  
Этап: Stage G (Generator Exploration)  
Причина: устранение архитектурного противоречия между legacy-протоколом и каналами генератора v5.

---

# 1. Проблема

В legacy-версии теста **не существовало явного деления на физиологические каналы**.

Тест оперировал только параметрами стимула:

- цвет
- позиция
- PSI
- номер стимула

Компоненты реакции извлекались **после теста**.

Следовательно:

каналы не являются наблюдаемыми параметрами теста


В генераторе v5 каналы заданы напрямую:

V1
Parvo
Magno
Koniocellular


Это создаёт архитектурное противоречие.

---

# 2. Принцип исправления

В Stage G каналы должны **не задаваться напрямую**, а **формироваться из параметров стимула**.

Базовый принцип:

Stimulus parameters → Functional channels → Reaction

где:

stimulus parameters =
color
spatial position
PSI


---

# 3. Новый уровень модели

Архитектура генератора должна быть изменена на:

Stimulus Generator
↓
Stimulus parameters
(color / position / PSI)
↓
Functional channel mapping
↓
Subject model
↓
Reaction


---

# 4. Определение каналов

В Stage G каналы должны определяться **комбинациями параметров стимулов**.

Пример экспериментального отображения:

| Stimulus | Channel interpretation |
|--------|-----------------------|
| Blue + center | Parvo-like |
| Blue + peripheral | Magno-like |
| Red + center | V1-like |
| Yellow + peripheral | Koniocellular-like |

Это **гипотеза**, которую нужно проверять.

---

# 5. Task G-13  
## Реализация слоя отображения каналов

Создать модуль:

generator/channel_mapping.py

Функция модуля:

map_channel(stimulus_color, stimulus_position) → functional_channel


Mapping должен быть конфигурируемым.

---

# 6. Task G-14  
## Конфигурация отображения каналов

Добавить в файл:

generator_config.yaml

раздел:

channel_mapping:
blue_center: Parvo
blue_peripheral: Magno
red_center: V1
yellow_peripheral: Koniocellular


Эта конфигурация должна быть изменяемой для экспериментальных сценариев.

---

# 7. Task G-15  
## Экспериментальные режимы каналов

Генератор должен поддерживать несколько режимов:

### Mode 1 — Legacy faithful

no channels

реакции зависят только от:

stimulus parameters


---

### Mode 2 — Derived channels

каналы вычисляются через mapping.

---

### Mode 3 — Explicit channels

каналы задаются напрямую (как в текущем генераторе v5).

---

# 8. Task G-16  
## Сравнение режимов генерации

Необходимо провести сравнительный анализ:

Mode 1
vs
Mode 2
vs
Mode 3

Сравниваются:

ΔV4 distributions
ΔV5 distributions
PSI sensitivity
spatial effects

---

# 9. Критерий успешности

Stage G должен определить:

1. можно ли объяснить компонентную архитектуру **только параметрами стимулов**;
2. требуется ли введение явных каналов;
3. какие комбинации стимулов формируют функциональные каналы.

---

# 10. Результат

Документ:

Stage_G_Channel_Model_Evaluation.md

должен содержать:

- описание tested mappings
- статистику Δ-компонент
- вывод о необходимости каналов.


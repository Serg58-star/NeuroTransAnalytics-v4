# 3_Stage G — Коррекция модели стимулов (цветовой слой)
## NeuroTransAnalytics v5 — Generator Research Layer

Исполнитель: GoAn  
Этап: Stage G (Generator Exploration)

---

# 1. Назначение

В генераторе Stage G необходимо учитывать реальные параметры legacy-тестов.

В legacy-системе использовались **три цвета стимулов**:

red
green
blue


Цвет **yellow** в legacy-протоколе отсутствовал.

Поэтому любые модели генератора, использующие yellow как базовый стимул, считаются **несоответствующими legacy-дизайну**.

---

# 2. Правило цветовой конфигурации

Базовый набор цветов Stage G:

RED
GREEN
BLUE

Этот набор должен считаться:

legacy_color_set

и использоваться в режиме:

Legacy faithful mode


---

# 3. Task G-17  
## Исправление цветового набора генератора

Проверить весь код генератора Stage G и убедиться, что:

1. yellow не используется как базовый стимул
2. цветовая схема соответствует legacy-набору:

['RED', 'GREEN', 'BLUE']


При необходимости:

- удалить yellow
- заменить его на green

---

# 4. Task G-18  
## Реализация цветовых конфигураций

Добавить поддержку нескольких цветовых схем в конфигурации генератора.

В файле:

generator_config.yaml

создать раздел:

color_sets:
legacy_rgb:
- RED
- GREEN
- BLUE

experimental_rgb:
- RED
- GREEN
- BLUE

experimental_extended:
- RED
- GREEN
- BLUE
- YELLOW


---

# 5. Task G-19  
## Связь цветов со стимульными каналами

В модуле:

generator/channel_mapping.py

реализовать конфигурируемое отображение:

(color, position) → functional_channel

Пример (legacy-режим):

RED → V1-like
GREEN → Parvo-like
BLUE → Magno-like

Экспериментальные режимы могут вводить:

YELLOW → Koniocellular-like


---

# 6. Task G-20  
## Экспериментальные сценарии цветовых стимулов

Генератор должен поддерживать сценарии:

### Scenario C0 — Legacy RGB

RED
GREEN
BLUE

### Scenario C1 — Extended spectrum

RED
GREEN
BLUE
YELLOW


### Scenario C2 — Spatial color mapping

цветовая интерпретация зависит от позиции:

BLUE + CENTER
BLUE + PERIPHERY


---

# 7. Критерий корректности

Генератор считается корректным, если:

1. legacy-режим воспроизводит исходную цветовую архитектуру теста
2. экспериментальные режимы не нарушают базовый протокол
3. все цветовые параметры фиксируются в базе данных генератора

---

# 8. Результат

Создать документ:

Stage_G_Color_Model.md


Документ должен содержать:

- используемые цветовые наборы
- mapping цветов на функциональные каналы
- различия legacy и экспериментальных режимов





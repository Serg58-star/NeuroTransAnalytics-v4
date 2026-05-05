# Stage G — Первые задачи
## NeuroTransAnalytics v4 → v5
### Generator Research Layer

Назначение: обеспечить немедленное начало работы в новом чате без этапа предварительного планирования.

Stage G начинается **как исследовательская ветка**, цель которой — изучить влияние параметров стимулов на активацию зрительных каналов и компонентную структуру реакции.

Основная модель исследования:

Stimulus
→ Channel activation
→ ΔV components
→ Reaction time


Все анализы выполняются **только в контексте структуры стимулов**.

---

# Task G1 — Формирование таблицы условий стимулов

Цель: создать единую таблицу условий стимулов для всей legacy-базы.

Создать таблицу:

stimulus_condition_matrix

Структура:

subject_id
session_id
test
color
field
stimulus_index
PSI
rt
delta_v1
delta_v4
delta_v5_mt

Условия:

Test = simple | color | shift
Color = red | green | blue
Field = left | center | right


Каждая запись должна соответствовать **одной реакции**.

---

# Task G2 — Проверка полноты экспериментального дизайна

Цель: подтвердить корректность структуры эксперимента.

Проверить распределение:

Test × Color × Field

Ожидаемая структура:

3 × 3 × 3 = 27 условий

Также проверить:

12 стимулов на каждое поле
4 стимулa каждого цвета

Создать отчёт:

Stage_G2_Stimulus_Design_Audit.md


---

# Task G3 — Привязка позиций стимулов к координатам

Цель: создать геометрическую модель поля зрения.

Создать таблицу:

stimulus_geometry

Пример координат:

center (0,0)
left (-1,0)
right (1,0)

top_center (0,1)

lower_left (-1,-1)
lower_right (1,-1)

Добавить поля:

x
y
eccentricity
hemifield

eccentricity:

sqrt(x² + y²)


---

# Task G4 — Расчёт медиан и MAD для условий стимулов

Использовать **только робастную статистику**.

Для каждой комбинации условий вычислить:

median_rt
MAD_rt
median_delta_v4
MAD_delta_v4
median_delta_v5_mt
MAD_delta_v5_mt

Результат сохранить:

stimulus_condition_statistics


---

# Task G5 — Базовые канальные индексы

Вычислить первые индексы каналов.

Magnocellular:

M_speed =
median(shift_left + shift_right)


M_periphery =
median(shift_left + shift_right)
− median(shift_center)

Parvocellular:

P_index =
median(green_center)
− median(red_center)


Koniocellular:

K_index =
median(blue_center)
− median(red_center)

Создать документ:

Stage_G5_Channel_Index_Report.md


---

# Task G6 — Матрица условий эксперимента

Построить матрицу:

Test × Color × Field


3 × 3 × 3 = 27 условий


Для каждого условия вычислить:

median_rt
MAD_rt
median_delta_v4
median_delta_v5_mt

Создать таблицу:

stimulus_condition_matrix_27


---

# Task G7 — Карты активации каналов

Вычислить:

A_M(test,color,field)
A_P(test,color,field)
A_K(test,color,field)

Использовать нормированную реакцию:

activation =
baseline − RT

или

zscore(RT)


---

# Task G8 — Пространственные карты каналов

Используя координаты стимулов построить функции:

M(x,y)
P(x,y)
K(x,y)

Это даст:

retinal channel maps

Создать отчёт:

Stage_G8_Retinal_Channel_Maps.md


---

# Task G9 — Чувствительность каналов

Для каждого канала вычислить:

Sensitivity =
|signal| / noise

где:

noise = MAD

Метрики:

S_M
S_P
S_K

Создать документ:

Stage_G9_Channel_Sensitivity.md


---

# Task G10 — Подготовка архитектуры генератора стимулов

Начать проектирование генератора Stage G.

Генератор должен иметь слои:

Stimulus Generator
(Test × Color × Field × PSI)
↓
Channel Activation Model
(M / P / K)
↓
Component Model
(ΔV1 / ΔV4 / ΔV5)
↓
Subject Model
(noise / fatigue)
↓
Reaction Time

Создать документ:

Stage_G10_Generator_Architecture.md


---

# Ожидаемый результат первых задач Stage G

После выполнения задач G1–G10 должны быть получены:

таблица условий стимулов
проверка экспериментального дизайна
геометрическая модель поля зрения
базовые канальные индексы
карты активации каналов
пространственные карты каналов
метрики чувствительности каналов
архитектура генератора стимулов


Это создаёт основу для дальнейшей оптимизации теста и возможной модификации v5.




















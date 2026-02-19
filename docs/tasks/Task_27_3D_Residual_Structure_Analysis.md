# Task_27_3D_Residual_Structure_Analysis

## Цель

Провести дополнительный анализ остаточной структуры
после регрессионного контроля базовой скорости и вариабельности.

Задача — определить,
имеют ли residual компоненты ΔV4 и ΔV5
структурированную связь с другими параметрами.

Никаких интерпретаций.
Только числовые показатели.

---

# I. Исходные данные

Использовать результаты production-run (Task 27.3).

Для каждой модели доступны:

- ΔV4_field_residual
- ΔV5_field_residual
- PSI_tau
- Asym_ΔV1_abs
- Asym_ΔV1_rel

Если residual не сохранены —
пересчитать их, используя уже рассчитанные β.

---

# II. Обязательные расчёты

Для каждого поля (left, right):

## 1. Корреляции residual ΔV4

Рассчитать:

- Corr(ΔV4_residual, PSI_tau)
- Corr(ΔV4_residual, Asym_abs)
- Corr(ΔV4_residual, Asym_rel)

## 2. Корреляции residual ΔV5

Рассчитать:

- Corr(ΔV5_residual, PSI_tau)
- Corr(ΔV5_residual, Asym_abs)
- Corr(ΔV5_residual, Asym_rel)

Использовать:

- Pearson r
- Spearman ρ

Вывести:

- коэффициенты
- p-value

---

# III. Дополнительная проверка остаточной структуры

1. Рассчитать корреляцию между:

    ΔV4_residual_left и ΔV5_residual_left  
    ΔV4_residual_right и ΔV5_residual_right  

2. Проверить межполушарную согласованность:

    Corr(ΔV4_residual_left, ΔV4_residual_right)  
    Corr(ΔV5_residual_left, ΔV5_residual_right)

---

# IV. Критерии фиксации

В отчёте выделить случаи:

- |r| ≥ 0.3
- |r| ≥ 0.5

Без интерпретации.

---

# V. Формат результата

Создать:

1. residual_structure_results.csv
2. Дополнение к отчёту:

    Task_27_3_Residual_Analysis_Report.md

Структура отчёта:

- Таблица корреляций
- Таблица p-value
- Таблица межполушарных связей
- Таблица cross-component residual correlations

Никаких выводов.
Никаких объяснений.

---

# VI. Ограничения

Запрещено:

- Делать PCA
- Делать кластеризацию
- Делать UMAP
- Строить графики
- Делать вывод A/B/C

---

# Цель этапа

Определить,
имеет ли остаточное пространство
структурированную взаимосвязь
или оно близко к шуму.

Конец документа.

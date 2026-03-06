# Stage_H2.2b — Subject-Level Spectral Recalculation (First-Visit Only)

## Исполнитель: GoAn

## Роль ChatGPT: независимая методическая верификация

---

# 1. Основание

В Stage_H2.2 спектральные и демографические выводы были получены на уровне **записей (records)**, а не на уровне **уникальных субъектов**.

Обнаружено:

* Наличие повторных тестов.
* 138 повторных записей принадлежат двум мужчинам.
* Возможное искажение ковариационной структуры.
* Возможное искусственное усиление Male λ₁.

Следовательно:

> Необходимо пересчитать геометрию строго на уровне субъектов.

---

# 2. Цель Stage_H2.2b

Проверить устойчивость выводов Stage_H2.2 при переходе:

**от record-level анализа → к subject-level анализу (First-Visit Only).**

Ключевой вопрос:

> Сохраняются ли спектральные и демографические эффекты после устранения повторных наблюдений?

---

# 3. Формирование выборки

## 3.1 Правило включения

Для каждого `subject_id`:

* оставить **только первое посещение** (минимальная дата теста);
* полностью исключить все последующие повторные записи.

## 3.2 Контроль

Зафиксировать:

* Общее число уникальных субъектов.
* Число исключённых повторных записей.
* Распределение пола и возраста в новой выборке.

Deliverable:

`docs/audit/H2_2b_Block0_Sample_Construction.md`

---

# 4. Аналитические блоки (повтор Stage_H2.2)

Каждый блок → отдельный .md документ.

---

## Блок 1 — Baseline-Adjusted Spectral Geometry (Subject-Level)

Повторить расчёт:

* Effective Rank
* Participation Ratio
* PC1%
* λ-спектр
* Анизотропию

Сравнить:

* H2.2 (record-level)
* H2.2b (subject-level)

Deliverable:

`docs/audit/H2_2b_Block1_Spectral_Geometry_Subject_Level.md`

Формальный вывод:

* SPECTRAL_STRUCTURE_STABLE
* SPECTRAL_STRUCTURE_MODIFIED

---

## Блок 2 — Load-Only Geometry (Subject-Level)

Пересчитать:

* Eff.Rank
* PC1%
* λ₁–λ₃
* Hopkins
* Silhouette

Deliverable:

`docs/audit/H2_2b_Block2_Load_Only_Subject_Level.md`

---

## Блок 3 — Sex Spectral Stability (Subject-Level)

Проверить:

* Male vs Female λ₁
* Eff.Rank
* PC1%
* λ₁ ratio

Сравнить с H2.2 (record-level 1.51×).

Deliverable:

`docs/audit/H2_2b_Block3_Sex_Spectral_Subject_Level.md`

Формальный вывод:

* SEX_EFFECT_STABLE
* SEX_EFFECT_REDUCED
* SEX_EFFECT_COLLAPSED

---

## Блок 4 — Age Spectral Stability (Subject-Level)

Проверить:

* Eff.Rank по квартилям
* λ₁
* PC1%
* Сохраняется ли Q2-аномалия

Deliverable:

`docs/audit/H2_2b_Block4_Age_Spectral_Subject_Level.md`

Формальный вывод:

* AGE_GRADIENT_CONFIRMED
* AGE_GRADIENT_REDUCED
* AGE_GRADIENT_DISAPPEARED

---

# 5. Финальный сравнительный документ

Сформировать:

`docs/audit/H2_2b_Final_Comparison_Report.md`

Включить:

1. Таблицу Record-Level vs Subject-Level.
2. Изменение Eff.Rank.
3. Изменение λ₁ ratio (Male/Female).
4. Изменение Q2 спектрального эффекта.
5. Итоговый ответ:

> Были ли демографические эффекты артефактом повторных тестов?

Без архитектурных рекомендаций.

---

# 6. Строгие ограничения

Запрещено:

* Использовать synthetic.
* Использовать κ или Severity.
* Менять признаковый базис.
* Моделировать форму демографической зависимости.
* Делать проектные выводы.

Это чистая проверка устойчивости спектральных результатов.

---

# 7. Критерий завершения

Stage_H2.2b считается завершённым только если:

* Все блоки выполнены.
* Представлено строгое сравнение record-level и subject-level результатов.
* Даны формальные verdict-метки.
* Нет интерпретационных комментариев.

---

# Конец задачи

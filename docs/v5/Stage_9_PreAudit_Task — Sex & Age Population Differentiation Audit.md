# NeuroTransAnalytics-v4
# Stage 9 — Population Differentiation Audit
# Sex and Age Structural Verification

## Статус
DOCUMENTATION EXTRACTION TASK (NO INTERPRETATION)

## Режим
Работа с документацией.
GoAn действует строго как архивариус.

Интерпретации, выводы и гипотезы запрещены.

---

# 1. Цель задачи

Проверить, содержатся ли в документации проекта NeuroTransAnalytics-v4
математические доказательства или опровержения различий:

1. Между мужчинами и женщинами
2. Между возрастными группами
3. Взаимодействия пола и возраста

Интересует только документально зафиксированная проверка,
а не предположения.

---

# 2. Область поиска

Проверить ВСЕ доступные документы проекта, включая:

- Stage 1–8.5
- Stage 9A
- Stage 9B
- Stage 9C
- Population Geometry Reports
- Task 36–52
- Completion Summaries
- Validation Reports
- Statistical Appendices
- Bootstrap Reports
- Covariance Analysis
- PCA Analysis
- Supplementary Notes

---

# 3. Что именно искать

GoAn должен найти:

## 3.1 Проверка половых различий

- t-test / Mann-Whitney
- permutation tests
- bootstrap CI comparison
- effect size (Cohen’s d)
- multivariate comparison (MANOVA)
- covariance matrix comparison
- PCA separation by sex
- Silhouette by sex grouping
- Mahalanobis distribution split by sex

Любые формальные проверки различий.

---

## 3.2 Проверка возрастных различий

- регрессия по возрасту
- корреляции с возрастом
- spline-анализ
- ANCOVA
- стратификация по возрастным группам
- изменение PR, PC1, Severity по возрасту
- drift analysis с возрастным фактором

---

## 3.3 Совместный анализ (Sex × Age)

- Interaction models
- Two-way ANOVA
- Multivariate interaction
- Age-adjusted sex comparison

---

# 4. Формат ответа

Для каждого найденного фрагмента:

1. Название документа
2. Раздел
3. Точная цитата
4. Номер страницы или строк (если доступно)
5. Тип анализа (если указан в тексте)

Никаких интерпретаций.
Никаких выводов.
Никаких резюме.

Если таких проверок нет,
GoAn должен прямо указать:

"В доступной документации математическая проверка различий пола и возраста не обнаружена."

---

# 5. Запрещено

- Делать выводы
- Обобщать
- Формулировать гипотезы
- Предлагать новые тесты
- Пересказывать без цитирования

---

# 6. Причина задачи

До перехода к дальнейшему развитию Risk Layer
необходимо убедиться,
что геометрия действительно универсальна,
а не содержит скрытой стратификации по полу или возрасту.

---

# 7. Ожидаемый результат

Строго документальный отчёт о наличии или отсутствии
математической проверки различий пола и возраста
в исторических данных проекта.

---

# Конец задачи
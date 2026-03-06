# Stage_H3 — PSI Structural Contribution Audit

## Исполнитель: GoAn

## Роль ChatGPT: независимая методическая верификация

---

# 1. Основание

В ходе Stage_H2.2 и Stage_H2.2b установлено:

* Эмпирическое пространство baseline-adjusted является умеренно многомерным (Eff.Rank ≈ 6.5).
* Демографические спектральные эффекты (Male λ₁-доминантность, Q2 возрастная диффузия) устойчивы.
* Повторные тесты не искажают структуру.

Однако остаётся нерешённый вопрос:

> Каков вклад стабильной псевдослучайной структуры PSI в формирование спектральной геометрии?

Историческая эмпирика содержит структурированный PSI-драйвер (не белый шум).
В v5 PSI является архитектурно встроенным механизмом.

Сравнение систем без явной оценки PSI-вклада является неполным.

---

# 2. Цель Stage_H3

Выделить, количественно оценить и изолировать вклад PSI-структуры в:

1. Глобальную размерность (Eff.Rank)
2. Load-only геометрию
3. Sex-амплитудную асимметрию
4. Age Q2-диффузию

Ключевой вопрос:

> Формируют ли выявленные спектральные эффекты амплитудные свойства системы или динамически-PSI-опосредованные?

---

# 3. Формирование PSI-представления

## 3.1 Уровень анализа

Работать на уровне trial-sequence (36 проб), не на агрегированных медианах.

## 3.2 Извлекаемые параметры PSI

Для каждого теста и канала вычислить:

* Hurst exponent
* Autocorrelation decay
* Variance growth rate
* Spectral density slope
* Entropy / permutation entropy
* PSI amplitude index (если ранее определён)

Формировать:

PSI Feature Matrix (subject-level).

Deliverable:

`docs/audit/H3_Block0_PSI_Feature_Definition.md`

---

# 4. Аналитические блоки

Каждый блок → отдельный .md документ.

---

## Блок 1 — PSI Contribution to Global Spectral Geometry

### Задача:

1. Построить baseline-adjusted 12D без PSI-параметров.

2. Добавить PSI-параметры как отдельные оси.

3. Сравнить:

   * Eff.Rank
   * PC1%
   * λ-спектр

4. Оценить изменение размерности.

Deliverable:

`docs/audit/H3_Block1_PSI_Global_Contribution.md`

Формальный вывод:

* PSI_NEGLIGIBLE
* PSI_MODERATE_CONTRIBUTION
* PSI_DOMINANT_FACTOR

---

## Блок 2 — PSI vs Load-Only Geometry

Проверить:

* Корреляцию PSI-параметров с ΔV4, ΔV5, Δ-lat.
* Влияние PSI на Eff.Rank load-space.
* Изменяется ли load-анизотропия при регрессии PSI.

Deliverable:

`docs/audit/H3_Block2_PSI_Load_Interaction.md`

---

## Блок 3 — PSI Demographic Stability

Проверить:

* Есть ли различия PSI-параметров между Male / Female.
* Есть ли возрастной градиент PSI.
* Коррелирует ли Q2-диффузия с PSI-изменениями.

Deliverable:

`docs/audit/H3_Block3_PSI_Demographic_Stability.md`

Формальный вывод:

* PSI_DEMOGRAPHICALLY_INVARIANT
* PSI_PARTIALLY_DEMOGRAPHIC
* PSI_DEMOGRAPHICALLY_STRUCTURED

---

## Блок 4 — PSI-Residual Spectral Geometry

Регрессировать PSI-параметры из baseline-adjusted 12D.

Построить спектр остаточного пространства.

Проверить:

* Изменяется ли Eff.Rank.
* Сохраняется ли Male λ₁-доминантность.
* Сохраняется ли Q2-эффект.

Deliverable:

`docs/audit/H3_Block4_PSI_Residual_Geometry.md`

---

# 5. Строгие ограничения

Запрещено:

* Использовать synthetic.
* Использовать κ, Severity.
* Вносить архитектурные изменения v5.
* Делать проектные выводы.

Это чистая декомпозиция динамического вклада.

---

# 6. Критерий завершения

Stage_H3 считается завершённым только если:

* Выделены PSI-параметры.
* Их вклад в размерность количественно оценён.
* Проверена демографическая стабильность PSI.
* Выполнена PSI-регрессия и пересчёт спектра.
* Даны формальные verdict-метки без интерпретаций.

---

# 7. Ожидаемый результат

Stage_H3 должен дать строгий ответ:

> Является ли PSI скрытым фактором, формирующим спектральную геометрию baseline-adjusted пространства?

Только после этого допустим переход к:

* Stage_H3.1 — F1 Cross-Model Comparison
* Протокольному выравниванию v5
* Либо корректировке synthetic

---

# Конец задачи

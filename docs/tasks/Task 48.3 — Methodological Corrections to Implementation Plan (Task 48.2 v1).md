# Task 48.3 — Methodological Corrections to Implementation Plan (Task 48.2 v1)
## Усиление контроля ложноположительных результатов и вычислительной устойчивости

**Версия:** v1  
**Дата:** 2026-02-25  
**Основание:** Task 48.2 — Implementation Plan v1  
**Статус:** Draft — Approval Required  

---

# 1. Цель поправки

Устранить методологические риски в Implementation Plan Task 48.2:

1. Исключить невозможность оценки False Positive Rate.
2. Предусмотреть вычислительные ограничения MixedLM.
3. Уточнить корректность AIC/BIC сравнения моделей.
4. Зафиксировать обязательность финального вердикта об исчерпанности микроуровня.

Поправка обязательна до запуска Phase 1.

---

# 2. Поправки по фазам

---

## 2.1 Phase 1 — Synthetic Generator

### Обязательное дополнение: Negative Controls

Добавить два контрольных сценария:

### (A) Zero-Interaction Scenario
- Коэффициент `log(PSI) × Position` = 0
- Остальные эффекты сохранены

Цель:
- Проверить, что модель не извлекает ложное взаимодействие.

---

### (B) Zero-Nonlinearity Scenario
- Коэффициенты `Position²` и `[log(PSI)]²` = 0
- Остальные эффекты сохранены

Цель:
- Проверить, что quadratic модели не дают ложноположительные результаты.

---

### Требование

Для обоих сценариев необходимо:

- Оценить False Positive Rate.
- Зафиксировать долю ложных значимых результатов (при α = 0.05).
- Подтвердить, что FPR ≈ 5% (в пределах статистической погрешности).

Без этого Phase 2 считается методологически неполной.

---

## 2.2 Phase 2 — Validation

### Обязательное уточнение: MixedLM Fallback Strategy

MixedLM при ~1500 субъект-сессиях может:

- не сходиться,
- выдавать предупреждения о сингулярности,
- быть вычислительно нестабильной.

Добавить обязательный fallback-порядок:

1. Полная модель:
   RT ~ log(PSI) + Position + (log(PSI) + Position | Subject)

2. Если не сходится:
   RT ~ log(PSI) + Position + (Position | Subject)

3. Если всё ещё не сходится:
   Random intercept model.

Отчёт обязан фиксировать:

- какая модель использована;
- причины перехода к fallback;
- влияние упрощения на дисперсию random slopes.

---

## 2.3 Phase 3 — Real Data

### Уточнение по AIC/BIC

AIC/BIC сравнение допустимо только:

- для вложенных моделей;
- или для моделей с идентичной зависимой переменной и одинаковым набором наблюдений.

Обязательное требование:

- явно указать, какие модели сравниваются;
- зафиксировать корректность сравнения;
- исключить некорректные AIC/BIC интерпретации.

---

## 2.4 Phase 4 — Reporting

### Обязательное требование

Раздел:

> Deliver the final verdict on whether the micro-level database is completely exhausted prior to v5 design.

Должен:

- основываться на результатах interaction, nonlinearity и clustering;
- быть аргументирован численно;
- избегать декларативных формулировок;
- чётко разделять:
  - доказанные эффекты,
  - невыявленные эффекты,
  - методологические ограничения.

Это является логическим завершением микроуровня.

---

# 3. Verification Plan Update

Добавить обязательные проверки:

- Synthetic Negative Control Check (Interaction).
- Synthetic Negative Control Check (Nonlinearity).
- MixedLM Convergence Check.
- AIC/BIC Correctness Check.
- Final Exhaustion Assessment Justification.

---

# 4. Governance

Per our Governance Rule, I am requesting your explicit written approval ("Approved for implementation. Reference: Task 48.3 v1") before amending the Implementation Plan for Task 48.2.

---

End of Task 48.3
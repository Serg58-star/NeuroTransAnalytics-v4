# Stage 9C — Task 56
# Повторная валидация Transition Probability Field (после стабилизации)

## Статус
RISK LAYER REVALIDATION

## Зафиксированный генератор

κ = 0.08 (LOCKED)

---

# 1. Цель

Повторно построить Transition Probability Field
на стабилизированной продольной динамике.

Подтвердить устранение структурной ригидности.

---

# 2. Вычислительные параметры

- N = 500
- T = 10
- Без bootstrap
- Полный спектральный анализ
- Полная Transition Matrix

---

# 3. Проверяемые критерии

## 3.1 Переходная матрица

- Нет P_ii > 0.95
- Строки суммируются к 1

---

## 3.2 Спектральная устойчивость

- |λ_max| = 1
- Нет |λ| > 1
- Spectral Gap ≥ 0.15

---

## 3.3 Стационарное распределение

- Ни один квадрант > 50%

---

## 3.4 Энтропия

- Mean Entropy ≥ 0.6
- Нет экстремально низких H_i (< 0.1)

---

## 3.5 Непрерывность

- Silhouette_longitudinal < 0.20

---

# 4. Deliverable

docs/v5/Stage_9C_Task_56_TPF_Revalidation_Report.md

Включить:

- Новую Transition Matrix
- Eigenvalues
- Stationary distribution
- Entropy
- Silhouette
- Сравнение с версией до стабилизации
- Финальный вердикт

---

# 5. Outcome

Если критерии выполнены:

→ Transition Probability Field → LOCKED  
→ Переход к формализации Risk Accumulation Index

Если нет:

→ дополнительная динамическая коррекция
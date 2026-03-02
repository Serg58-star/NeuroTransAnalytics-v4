# Stage 9C — Task 56A
# Повторная валидация TPF с фиксированными порогами квадрантов

## Статус
METHODICAL CORRECTION

## Зафиксированные параметры

κ = 0.08
Quadrant thresholds = Baseline (κ=0)

---

# 1. Цель

Повторить TPF валидацию,
используя фиксированные S75 и DII75,
рассчитанные на baseline генераторе (κ=0).

---

# 2. Запрещено

- пересчитывать S75
- пересчитывать DII75
- менять систему квадрантов

---

# 3. Проверяемые критерии

1. Absorbing states ≤ 0.95
2. Spectral gap ≥ 0.15
3. Max stationary mass ≤ 50%
4. Mean entropy ≥ 0.60
5. Silhouette_longitudinal < 0.20

---

# 4. Deliverable

docs/v5/Stage_9C_Task_56A_TPF_Revalidation_Anchored_Report.md

---

# 5. Интерпретация

Если критерии выполнены:

→ κ = 0.08 окончательно подтверждён  
→ Transition Probability Field → LOCKED  

Если нет:

→ пересмотр g(S) функции
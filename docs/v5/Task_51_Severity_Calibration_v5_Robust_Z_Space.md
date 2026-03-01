# Task 51 — Severity Calibration v5 (Robust Z-Space)

## Status
ARCHITECTURAL CALIBRATION PHASE (Synthetic Model)

## Branch
v5-dual-space-architecture

## Prerequisite
Task 49.1 — Dual-Space Vector Architecture  
Task 49.1A — Robust Standardization Amendment  
Task 50A — Z-Space Geometric Validation (LOCKED)

---

# 1. Objective

После блокировки Z-Space Population Geometry (Task 50A),
необходимо откалибровать Severity Index в v5.

Цель Task 51:

- формально определить центр нормы в Z-пространстве,
- откалибровать Mahalanobis distance,
- построить радиальную стратификацию,
- проверить устойчивость границ,
- протестировать heavy-tail устойчивость,
- сформировать стабильную Severity-шкалу для v5.

Важно:

Данный этап выполняется на синтетической популяции.
Это архитектурная калибровка, не клиническая нормировка.

---

# 2. Mathematical Framework

Работа ведётся в Z-пространстве:

\[
Z \in \mathbb{R}^{N \times 12}
\]

где координаты уже robust-standardized (MAD-based).

---

# 3. Robust Centroid (MCD)

## 3.1 Definition

Центр нормы определяется через:

Minimum Covariance Determinant (MCD)

\[
\mu_{MCD}
\]

и соответствующую ковариационную матрицу:

\[
\Sigma_{MCD}
\]

Требования:

- устойчивость к heavy-tail
- устойчивость к до 25–30% атипичных точек
- отсутствие смещения центра

---

# 4. Mahalanobis Distance (Robust Form)

Severity определяется как:

\[
D_M = \sqrt{(Z - \mu_{MCD})^T \Sigma_{MCD}^{-1} (Z - \mu_{MCD})}
\]

Это становится:

Severity Index v5

---

# 5. Radial Zone Stratification

На основе распределения \(D_M\) построить радиальные зоны:

### Zone A — Core (≤ 50th percentile)
### Zone B — Stable Norm (50–75%)
### Zone C — Extended Norm (75–90%)
### Zone D — Peripheral Deviation (90–95%)
### Zone E — Extreme Deviation (>95%)

Требования:

- зоны должны быть радиальными,
- не формировать дискретных кластеров,
- сохранять непрерывность континуума.

---

# 6. Bootstrap Envelope

Провести ≥ 1000 bootstrap итераций:

Проверить:

- стабильность \(\mu_{MCD}\),
- стабильность \(\Sigma_{MCD}\),
- SD границ зон,
- вариативность 95% envelope.

Критерии устойчивости:

- Смещение центра ≤ 5%
- Смещение 95% границы ≤ 5%

---

# 7. Heavy-Tail Stress Test

Смоделировать:

- 20% субъектов с увеличенным хвостом
- 30% субъектов с burst-нагрузкой

Проверить:

- смещение центра,
- изменение зон,
- устойчивость MCD к хвостам,
- стабильность Severity.

---

# 8. Continuum Preservation Check

Проверить:

- отсутствие искусственной кластеризации зон,
- monotonic radial growth,
- непрерывность KDE по \(D_M\),
- silhouette < 0.20 (при k=2..5).

---

# 9. Required Outputs

GoAn обязан предоставить:

1. Значение \(\mu_{MCD}\)
2. Ковариационную матрицу \(\Sigma_{MCD}\)
3. Таблицу percentiles для зон
4. Bootstrap SD по границам
5. Stress-test отчёт
6. График распределения Severity
7. Заключение: Stable / Unstable

Документ:

docs/v5/Task_51_Severity_Calibration_v5_Report.md


---

# 10. Failure Criteria

Task 51 считается FAILED если:

- центр нестабилен (>10% смещения),
- зоны скачкообразно изменяются,
- heavy-tail разрушает границы,
- возникает кластеризация.

---

# 11. Governance Rule

До завершения Task 51:

- Severity не используется в Monitoring Framework,
- Risk Modeling не запускается,
- Clinical Mapping запрещён.

---

# 12. Expected Outcome

Если Task 51 проходит:

v5 Severity Model → LOCKED (Synthetic)

Это открывает переход к:

Task 52 — Phase 2 Dynamics Modeling  
Stage 9B — Functional Monitoring Framework v5

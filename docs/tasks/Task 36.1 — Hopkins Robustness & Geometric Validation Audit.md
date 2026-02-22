# NeuroTransAnalytics-v4  
# Stage 7 — Continuum vs Discrete Types  
# Task 36.1 — Hopkins Robustness & Geometric Validation Audit

---

## 1. Статус

Task 36.1 является обязательным верификационным продолжением Task 36  
и выполняется в ветке:

feature/A7_population_geometry

Причина открытия:

В Task 36 получено значение Hopkins = 0.991 на реальном датасете (N=1482),  
что является экстремально высоким показателем.

Такое значение допустимо, но требует процедурной и геометрической проверки.

---

## 2. Цель

Проверить, не является ли Hopkins = 0.991 следствием:

- особенностей bounding box,
- масштабной неоднородности осей,
- вытянутой геометрии облака,
- наличия выбросов,
- краевых эффектов,
- неадекватной стандартизации,
- или артефакта sampling-процедуры.

Задача строго методологическая.  
Интерпретационный слой не активируется.

---

## 3. Обязательные проверки

### 3.1 Проверка стандартизации

GoAn обязан:

1. Указать:
   - применялась ли Z-нормировка перед расчётом Hopkins?
   - если да — к каким данным (raw axes или PCA space)?
2. Повторить Hopkins:
   - без стандартизации,
   - с Z-нормировкой,
   - с MinMax scaling,
   - с whitening (covariance normalization).

Сравнить значения.

---

### 3.2 Bounding Box Audit

1. Описать способ построения bounding box.
2. Проверить:
   - min/max диапазоны по каждой оси,
   - наличие сильной вытянутости (eigenvalue ratio).
3. Построить:
   - convex hull volume,
   - bounding box volume,
   - их отношение.

Повторить Hopkins при:

- bounding box sampling,
- convex hull constrained sampling,
- PCA-rotated bounding box.

---

### 3.3 Выбросы

1. Проверить наличие extreme points:
   - Mahalanobis distance > 99th percentile.
2. Удалить верхние 1% выбросов.
3. Пересчитать Hopkins.

---

### 3.4 Эллипсоидальность облака

1. Рассчитать covariance matrix.
2. Вычислить eigenvalue ratio (λ1/λ3).
3. Оценить anisotropy index.

Если λ1 >> λ2 >> λ3 — облако вытянуто.

Повторить Hopkins в:

- PCA-aligned coordinates,
- whitened space.

---

### 3.5 Краевая плотность

1. Проверить распределение расстояний до границ bounding box.
2. Вычислить edge density ratio:
   proportion of points within 5% от границы.

Если концентрация у краёв высока —
Hopkins может быть завышен.

---

### 3.6 Sampling robustness

Hopkins повторить:

- при k = 5, 10, 20,
- при 100 повторениях,
- с random seeds.

Оценить variance Hopkins.

---

## 4. Контрольный synthetic replay

Для сопоставления:

1. Сгенерировать:
   - равномерный 3D континуум,
   - вытянутый эллипсоид без кластеров,
   - градиентное облако плотности,
   - реальные данные с пермутацией координат.

2. Сравнить Hopkins в этих сценариях.

---

## 5. Формат отчёта

GoAn должен предоставить:

1. Таблицу Hopkins при разных нормировках.
2. Таблицу Hopkins при разных bounding box стратегиях.
3. Таблицу Hopkins после удаления выбросов.
4. Eigenvalue spectrum.
5. Convex hull / box ratio.
6. Sampling variance Hopkins.
7. Synthetic comparison table.

Финальный вывод строго в формате:

- HOPKINS_CONFIRMED
- HOPKINS_PARTIALLY_INFLATED
- HOPKINS_ARTIFACT

Без интерпретаций вне геометрии.

---

## 6. Архитектурное значение

Если Hopkins подтвердится устойчивым:

→ пространство действительно обладает сильной плотностной неоднородностью.

Если Hopkins снизится существенно:

→ Stage 7 вывод требует пересмотра.

Task 36.1 обязателен перед окончательной фиксацией Stage 7.
# NeuroTransAnalytics-v4  
# Stage 7 — Continuum vs Discrete Types  
# Task 36 — Population Geometry Audit

---

## 1. Статус

Task 36 открывает Stage 7 Exploratory Architecture Framework v4.  
Задача выполняется в ветке:

feature/A7_population_geometry

Режим: Exploratory (описательный).  
Интерпретационный слой не активируется.

---

## 2. Цель

Проверить, является ли популяционная структура 3-мерного латентного пространства:

- непрерывным континуумом,
или
- содержит устойчивые дискретные подтипы.

Анализ проводится строго на trait-ядре.

---

## 3. Используемое пространство

Используется production-пространство из Structural Verification:

1. Speed Axis  
2. Lateral Axis  
3. Residual Tone  

Ограничения:

- Trial-level данные не модифицируются.
- Новые признаки не вводятся.
- Микродинамический слой (Stage 5) не включается.
- Parametric индексы (μ, τ и др.) не используются.
- Никакой агрегации каналов.

Допускается только стандартная Z-нормировка для алгоритмов кластеризации.

---

## 4. Аналитические процедуры

### 4.1 Density diagnostics

1. kNN local density estimation (k = 10, 20, 30)
2. Распределение расстояния до ближайшего соседа
3. Hopkins statistic

Цель:
Оценить наличие кластерной тенденции против гипотезы равномерного континуума.

---

### 4.2 Clustering family audit

Провести для k = 2…8:

1. K-means
2. Gaussian Mixture Models (full covariance)
3. Hierarchical clustering (Ward)
4. HDBSCAN

Для каждого метода вычислить:

- Silhouette score
- Calinski–Harabasz index
- Davies–Bouldin index
- BIC (для GMM)
- Bootstrap stability (100 resamples)

---

### 4.3 Gap Statistic

Вычислить Gap(k) для k = 1…8.

Reference distribution:
равномерное распределение внутри bounding box 3D-пространства.

---

### 4.4 Projection robustness

Повторить кластеризацию:

- в исходном 3D,
- в PCA-пространстве (3 компоненты),
- в Rank-based представлении.

Оценить согласованность разметки через Adjusted Rand Index.

---

### 4.5 Topological diagnostics

1. kNN graph connectivity
2. Проверка числа компонент связности
3. MST (minimum spanning tree) edge distribution

Цель:
Выявить возможные разрывы плотности.

---

## 5. Критерии формального решения

### Континуум подтверждается, если:

- Hopkins ≈ 0.5
- Silhouette < 0.25 для всех k
- Gap Statistic не показывает устойчивого k > 1
- Низкая bootstrap-стабильность кластеров
- Граф kNN имеет одну связную компоненту

---

### Дискретность подтверждается, если:

- Стабильный k ≥ 2 у нескольких методов
- Silhouette ≥ 0.35
- Минимум BIC при k > 1 (GMM)
- Высокий Adjusted Rand Index между методами
- Стабильность при bootstrap

---

## 6. Ожидаемые артефакты

GoAn должен предоставить:

1. Implementation Plan (Planning mode).
2. Таблицы метрик для всех методов.
3. Gap curve.
4. Hopkins statistic.
5. Bootstrap stability matrix.
6. Матрицу согласованности методов (ARI).
7. Визуализации:
   - 3D scatter с кластерной разметкой
   - Density map
   - MST граф

Финальный вывод допускается только в формате:

- CONTINUUM
- WEAK CLUSTER TENDENCY
- STABLE DISCRETE TYPES

Без интерпретаций.

---

## 7. Архитектурное значение

Task 36 определяет:

- допустимость типологизации субъектов,
- необходимость или недопустимость введения кластерных классов в v5,
- сохранение строго координатной модели или переход к гибридной (coordinate + type).

Stage 7 начинается с Task 36.
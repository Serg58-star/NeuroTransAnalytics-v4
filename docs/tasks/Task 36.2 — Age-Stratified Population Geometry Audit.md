# NeuroTransAnalytics-v4  
# Stage 7 — Continuum vs Discrete Types  
# Task 36.2 — Age-Stratified Population Geometry Audit

---

## 1. Статус

Task 36.2 является дополнительным контрольным анализом Stage 7.

Цель — проверить, сохраняется ли непрерывная геометрия
после стратификации по возрасту.

Ветка:
feature/A7_population_geometry

---

## 2. Гипотеза проверки

Общая непрерывность (WEAK CLUSTER TENDENCY) может быть следствием:

- смешения возрастных когорт,
- наложения различных плотностных режимов,
- возрастно-зависимых геометрических деформаций.

Если внутри возрастных групп появится дискретность,
Stage 7 требует пересмотра.

---

## 3. Формирование возрастных групп

Использовать переменную age из neuro_data.db.

Сформировать:

### Базовая стратификация (квартильная)

- Q1 — младшая четверть
- Q2
- Q3
- Q4 — старшая четверть

Дополнительно:

### Декадная стратификация

- <30
- 30–39
- 40–49
- 50–59
- 60+

(если размер группы < 100 — объединять с соседней)

---

## 4. Для каждой возрастной группы выполнить

### 4.1 Density metrics

- Hopkins
- kNN density profile

### 4.2 Clustering audit

- KMeans (k=2…6)
- GMM
- Ward
- Silhouette
- Gap statistic

### 4.3 Topology

- Persistent homology (H0, H1)
- Betti curves
- MST connectivity

### 4.4 Eigen-geometry

- PCA eigenvalues
- Participation Ratio
- Anisotropy index

---

## 5. Cross-group comparison

1. Сравнить Hopkins между возрастами.
2. Проверить появление устойчивого k > 1 в какой-либо группе.
3. Проверить различия persistence lifetime.
4. Проверить изменение anisotropy.

---

## 6. Дополнительный тест

Выполнить:

- ANCOVA / regression:
  Cluster tendency metric ~ Age

Цель:
Определить, усиливается ли кластерность с возрастом.

---

## 7. Формат отчёта

Для каждой возрастной группы предоставить:

- N
- Hopkins
- Silhouette_peak
- Gap_optimal_k
- # persistent H0
- Max H1 lifetime
- Connectivity status

Финальный вывод допускается только в формате:

- AGE_INVARIANT_CONTINUUM
- AGE_DEPENDENT_DENSITY_GRADIENT
- AGE_SPECIFIC_CLUSTERING

Без физиологической интерпретации.

---

## 8. Архитектурное значение

Если непрерывность сохраняется во всех возрастных группах:

→ Stage 7 подтверждается окончательно.

Если в старших возрастах возникает устойчивый k ≥ 2:

→ возможно возрастная дискретизация
и потребуется дополнительная типологическая модель.
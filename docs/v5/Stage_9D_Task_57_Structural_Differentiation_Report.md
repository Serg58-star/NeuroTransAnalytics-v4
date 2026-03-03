# Stage 9D Task 57 — Structural Differentiation Report

## 1. N субъектов и структура тестов
- Общее число уникальных субъектов (N): 1482
- Использовано строк: 1886
- Максимум тестов: 112 | Минимум тестов: 1
- Среднее число тестов: 1.27 | Медиана: 1.0
- Доля 1 теста: 90.1%
- Доля >= 3 тестов: 3.4%

## 2. Геометрические показатели Z-space
- Participation Ratio (PR): 3.97
- Effective Rank: 3.97
- PC1 Explained Variance: 49.3%
- Matrix Condition Number (Sigma): 3.94e+18
- Max Silhouette (any K=2..5): 0.429

## 3. Sex-block Результаты
- Δ Centers (Euclidean): 3.996 -> **FAIL**
- Covariance Relative Difference (Frobenius): 48.3% -> **FAIL**
- Severity Cohen's d: 0.046 -> **PASS**
- Clustering by Sex (Silhouette): 0.029 -> **PASS**

## 4. Age-block Результаты
- Correlation (Severity ~ Age) rho: 0.048 -> **PASS**
- Clustered OLS R²: 0.00% -> **PASS**
- Clustered Nonlinear Spline (Age+Age^2) R²: 0.36% -> **PASS**
- Max Geometric Quartile Drift (PR/PC1): 160.8% -> **FAIL**
  - Max centroid drift across quartiles: 5.94 Z

## 5. Interaction Результаты (Mixed-Effects)
- Interaction term p-value (Sex x Age): 1.0000 -> **PASS**

## 6. Итоговый глобальный статус Stage 9D
- Total FAIL parameters: 3
- **GLOBAL STATUS:** **FAIL**

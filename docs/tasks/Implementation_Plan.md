Implementation Plan
1 minute ago

Review
Отчёт о стратегическом плане для Stage 1 (Task 29)
Данный документ описывает технический план реализации Этапа 1 эксплоративного анализа на основе Exploratory Architecture Framework v4.md и инструкций Task 29.

1. Повторное использование модулей
Анализ существующей архитектуры exploratory_lab показал:

Доступ к данным и расчет 11 базовых признаков (TrialLevelDataLoader, BaselineFeatureExtractor) переиспользуются без изменений.
В скриптах 
scripts/run_bootstrap_stability.py
 и 
scripts/run_pca_split_half.py
 уже реализованы функции 
pca_metrics()
, 
run_bootstrap()
 и 
run_split_half()
. Сейчас они захардкожены в скриптах.
Решение: Для соблюдения DRY и архитектурной чистоты мы извлечем эти функции в новый модуль src/exploratory_lab/geometry/stability.py.
Метрики 
Dim
, PC1%, Participation Ratio штатно извлекаются из PCA (
pca_metrics
).
2. Расширение функций
Будет добавлен новый функционал:

Расчёт Between/Within дисперсии: будет реализован как утилита, которая вычисляет отношение межсубъектной дисперсии к внутрисубъектной дисперсии по PC1.
Процедура Box-Cox оптимизации (scipy.stats.boxcox) с сохранением $\lambda$.
3. Архитектурные изменения: новый Pipeline
Согласно шаблону исследовательских процедур (exploratory-procedure-template), будет создан новый скрипт конвейера:

Файл: src/exploratory_lab/pipelines/stage1_scale_invariance.py
Pipeline загрузит признаки (production-набор, мы возьмем расширенный набор из 7 признаков, на котором была установлена стабильная 2D структура в задаче 27, либо 11 базовых — ожидаю уточнения от пользователя). Далее Pipeline применит по очереди 5 трансформаций:

Log-transform: np.log(X + epsilon)
Box-Cox: поиск $\lambda$ раздельно по векторам
Rank-based: замена значений рангами (scipy.stats.rankdata) по всей выборке
Z-score within subject: StandardScaler сгруппированный по subject_id
Z-score within test: StandardScaler, сгруппированный по исходным тестам (Tst1, Tst2, Tst3) до агрегации (потребует маппинга на сырые данные, либо использования промежуточного DataFrame).
Для каждого состояния мы прогоняем стандартизированный набор stability_metrics (PCA, Bootstrap SD, Split-half, B/W).

User Review Required
IMPORTANT

Уточнение набора признаков. В Task 29 указано "Используется текущий production-набор признаков, на котором ранее была подтверждена двумерная структура". Подразумевается ли использование 7 признаков (Core residuals + Asym + PSI tau), как в проверках 
run_bootstrap_stability.py
 (где структура стабильна), или исходных 11 базовых признаков (
baseline_features.py
)?

Уточнение Z-нормировки внутри теста. Для этой трансформации (29.5) необходимо нормировать до агрегации на уровень субъекта (поскольку Tst1, Tst2, Tst3 существуют на уровне trial-level data). План: выполнить нормировку массивов RT внутри TrialLevelDataLoader на уровне испытаний, а затем стандартным образом пропустить через BaselineFeatureExtractor. Это корректно?

4. Verification Plan
Выполнение stage1_scale_invariance.py должно завершиться корректно и сформировать Task_29_Stage1_Report.md.
Отчет будет содержать сравнительную таблицу со всеми столбцами (Dim, PC1%, PR, SD, ΔPC1, B/W).
Я проверю соответствие табличных результатов критериям закрытия Stage 1 и зафиксирую вывод в отчете.
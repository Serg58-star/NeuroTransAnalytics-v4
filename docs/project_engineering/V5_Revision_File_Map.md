# V5 Revision File Map

## Structural Update Inventory after Full Variance Partition (Tasks 48.5 - 48.7)

**Context:** Following the empirical confirmation that ∆V5/MT is statistically independent (Partial R² ~ 35%) and the discovery of the Global Modulator (~15%), the prior v4 architectural assumption that the Magno channel was "uninformative" and that PCA/subtractive geometry adequately isolated variances is formally annulled.

Below is the exhaustive inventory of `v4` project documents requiring revision for the `v5` transition.

---

### 1. `docs/project_engineering/NeuroTransAnalytics_v4_Engineering_Reconstruction_and_Full_Scenario_Audit.md`

- **Section(s):** Channel Metrics Definitions (`∆V5/MT`)
- **Target Phrase/Concept:** "Вычислялось как `Tst3 - Tst1`"
- **Revision Required:** **Structural mathematical correction**. Must redefine v5 geometry to abandon the double-subtractive baseline model that caused the artificial VIF/Variance Overlap.
- **Priority:** **High** (Core architecture definition)

### 2. `docs/tasks/Task_Report/Stage 9 — Strategic Architecture Geometric Risk Modeling & Functional Monitoring Framework.md`

- **Section(s):** Stage 9A Conclusions, PCA dimensional structures.
- **Target Phrase/Concept:** Assertions scaling the 3D trait core and relying on the PCA projection without recognizing the ~15% global baseline factor.
- **Revision Required:** **Conceptual correction**. Recontextualize the PCA metrics to acknowledge the geometric equilibrium proven in Task 48.7 (Tst1, ∆V4, ∆V5 ~ 1/3 each).
- **Priority:** **High** (Directly impacts final Stage 9 reporting logic)

### 3. `docs/tasks/Task_Report/Stage 3 Channel Reconstruction Analytical Report.md`

- **Section(s):** Conclusions on Parvo/Magno Index Aggregation (e.g., Block A/B)
- **Target Phrase/Concept:** "Простая Parvo/Magno агрегация разрушает геометрию", "Исходная геометрия не сводится к бинарному Parvo/Magno разделению".
- **Revision Required:** **Full rewrite required** (for concluding paragraphs). The observed "collapse" was an artifact of the `(TstX - V1)` collinearity, not an inherent biological lack of dimensionality. The channels naturally span independent axes as proven by the 41.4% antagonistic asymmetry.
- **Priority:** **High** (Historical accuracy of framework progression)

### 4. `docs/tasks/Task_Report/Exploratory Architecture Framework v4.md`

- **Section(s):** Section X. Parvo / Magno индексы
- **Target Phrase/Concept:** "Corr(Parvo, Magno) между субъектами и внутри субъекта."
- **Revision Required:** **Structural mathematical correction**. Update the structural matrix to reflect the Commonality Analysis (Task 48.7) decoupling unique vs shared variance.
- **Priority:** **High** (Fundamental framework structure)

### 5. `docs/Consolidated documentation_in_v4/NeuroTransAnalytics_Combined_Documentation_Сценарии_уровня_C_C1_Tom_5.md` (and `_a.md`)

- **Section(s):** Metric Validation / C1 Interpretations
- **Target Phrase/Concept:** "[канал/тест] считаются малоинформативными."
- **Revision Required:** **Minor wording correction / Conceptual correction**. Strict annulment of "малоинформативными" regarding Magno/Tst3.
- **Priority:** **Medium** (Documentation consistency)

### 6. `docs/10_2_C1_1_PSI_Design_Guidelines.md`

- **Section(s):** Information Value thresholds.
- **Target Phrase/Concept:** "считаются малоинформативными."
- **Revision Required:** **Conceptual correction**.
- **Priority:** **Medium**

### 7. `docs/tasks/Task_Report/Stage 5 - Structural Verification V4 Final Report.md`

- **Section(s):** Risk of Dimensionality Collapse
- **Target Phrase/Concept:** "Грубая Parvo/Magno агрегация → коллапс размерности"
- **Revision Required:** **Conceptual correction**. Clarify the mathematical source of the collapse (V1 baseline sharing).
- **Priority:** **Medium**

### 8. `docs/tasks/Walkthrough 31_Stage_3.md` & `docs/tasks/Task 31 — Stage 3...md`

- **Section(s):** Output observations.
- **Target Phrase/Concept:** "Parvo/Magno классификация ... не способна в одиночку удержать богатую геометрию данных (происходит коллапс в один фактор — общую скорость)."
- **Revision Required:** **Conceptual correction**. The "one factor" is empirically identified as the Global Modulator (15.4%).
- **Priority:** **Medium**

### 9. `docs/tasks/Task 28_1_Deep_Audit_Report.md`

- **Section(s):** 2_Research_Axes_and_Test_Conditions_v4 (Item 3)
- **Target Phrase/Concept:** "мы анализируем их как если бы они были независимы, но кросс-корреляция между ΔV4 и ΔV5 для одного субъекта не изучалась глубоко."
- **Revision Required:** **Minor wording correction**. Mark as resolved by Task 48.6 (Empirical evaluation confirmed profound independence).
- **Priority:** **Low**

### 10. `docs/tasks/Walkthrough 32_Stage_4.md`

- **Section(s):** Mask Interference
- **Target Phrase/Concept:** "Parvo/Magno 'cross-talk'".
- **Revision Required:** **Minor wording correction**. Ensure 'cross-talk' distinguishes between physiological interference and the geometric overlap artifact.
- **Priority:** **Low**

---
*Inventory generated pursuant to Task 49.0 v1 Governance Rules.*

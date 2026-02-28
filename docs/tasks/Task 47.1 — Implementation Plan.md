# Task 47.1 — Implementation Plan (Amendment to Task 47)

## Усиление требований инженерной реконструкции и полного аудита сценариев

**Version:** v1
**Date:** 2026-02-25

### 1. Goal Description

To amend the original Implementation Plan for Task 47 to integrate strict quantitative requirements, neurophysiological hypothesis tracking, and an expanded parameter mapping matrix. The engineering reconstruction must explicitly verify the correspondence between the real historical test protocol and the analytics performed in Stage 1–9C, identifying any structural deviations, omissions, or abstractions introduced by the modeling layers.

### 2. User Review Required
>
> [!IMPORTANT]
> Pursuant to the Governance Rule and Task 47.1 instructions, explicit written approval is required before the generation of this amended engineering document can begin.
> Please provide the following phrase to approve: **"Approved for implementation. Reference: Task 47.1 v1"**

### 3. Proposed Changes

#### [MODIFY] docs/project_engineering/NeuroTransAnalytics_v4_Engineering_Reconstruction_and_Full_Scenario_Audit.md

The target document format is being updated from the original 6 sections to **7 mandatory sections**, incorporating the strict requirements from Task 47.1:

1. **Инженерная реконструкция исторической системы СЗР**: Includes architecture, spatial organization, stimulus structure, and variability control.
    - **[NEW SUBSECTION]** *Reconstruction of the Original Neurophysiological Hypothesis*: Separating verified elements, untested elements, and declarative assumptions (e.g., ∆V1 vs ∆V4 vs ∆V5/MT).
2. **Полный аудит сценариев A/B/C**:
    - **[NEW REQUIREMENT]**: Quantitative evaluation matrix. For each scenario: Status, % Realization (estimated with justification), Presence of a report, and Priority for unrealized scenarios.
3. **Матрица соответствия «Параметр теста → Аналитика → v5»**:
    - **[EXPANDED REQUIREMENT]**: Must explicitly cover: Field of view, Color, PSI, Position in series (1-36), Masking clusters (Тройки), Shift (0/1/2/3), Pre-test trials, Anti-CV repetitions, RANO/POZDNO, SrKvadrOtkl, VidSost_txt, Time of day, and System parameters (MinRedLight, MaxRedLight, ROTATE_PERIOD).
4. **Что реально изучено в neuro_data.db**: Segregated by statistically verified, described but not verified, and unanalyzed.
5. **Дополнительные допустимые исследования (Exploratory)**:
    - **[NEW RESTRICTIONS]**: Any proposed methods must contain mathematical justification, known limitations, and potential effect on v5. Architecture modifications are strictly prohibited.
6. **Связь с проектируемой v5**: Outlining what is justified to keep, what must be revised (motor component subtraction), and what needs experimental verification.
7. **[NEW SECTION] Степень изученности базы neuro_data.db и оценка потенциала дальнейшего анализа**: Evaluation of whether historical data potential is exhausted, identification of unmined layers, and analysis of diminishing returns.

#### Execution Methodology

- **Phase 1**: Scan the entire `/docs` and `src/` to inventory the 14 A scenarios, 3 B scenarios, and 17 C scenarios, mapping them to completed scripts and reports to generate the quantitative % realization matrix.
- **Phase 2**: Analyze `README_addendum_summary.md`, `codebook_for_SZR.xlsx` references, and the original descriptions to construct the parameter mapping table and neurophysiological hypothesis baseline.
- **Phase 3**: Draft the comprehensive 7-section markdown document.

### 4. Verification Plan

- Verify `NeuroTransAnalytics_v4_Engineering_Reconstruction_and_Full_Scenario_Audit.md` contains exactly 7 primary sections in the specified order.
- Verify the Parameter Mapping Matrix contains rows for all 13 explicitly requested extended parameters.
- Verify the Quantitative Scenario Audit contains the required table structure (Сценарий | Уровень | Статус | % реализации | Наличие отчёта | Приоритет).

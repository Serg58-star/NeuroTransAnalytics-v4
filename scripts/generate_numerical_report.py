"""
Task 27.3C — Full Numerical Report from CSV

Generates a comprehensive numerical .md report from pre-computed CSV files.
No database access. No recalculations. Only reads stored results.

Source files (in data/exploratory/symmetric_regression/):
    - linear_regression_results.csv
    - multiple_regression_results.csv
    - heteroscedasticity_tests.csv

Output:
    - Task_27_3_Числовой_Отчёт_Production_Run.md
"""

import pandas as pd
import numpy as np
from pathlib import Path


DATA_DIR = Path(__file__).parent.parent / "data" / "exploratory" / "symmetric_regression"

LINEAR_CSV = DATA_DIR / "linear_regression_results.csv"
MULTIPLE_CSV = DATA_DIR / "multiple_regression_results.csv"
HETERO_CSV = DATA_DIR / "heteroscedasticity_tests.csv"

OUTPUT_FILE = DATA_DIR / "Task_27_3_Числовой_Отчёт_Production_Run.md"


def fmt(value, precision=6):
    """Format a numerical value for the report."""
    if isinstance(value, bool):
        return str(value)
    if isinstance(value, (int, np.integer)):
        return str(value)
    if isinstance(value, (float, np.floating)):
        if pd.isna(value):
            return "—"
        if abs(value) < 0.0001 and value != 0:
            return f"{value:.6e}"
        return f"{value:.{precision}f}"
    return str(value)


def load_csv_files():
    """Load all three CSV source files."""
    linear = pd.read_csv(LINEAR_CSV, index_col=0)
    multiple = pd.read_csv(MULTIPLE_CSV, index_col=0)
    hetero = pd.read_csv(HETERO_CSV, index_col=0)
    return linear, multiple, hetero


def section_1_sample_size(linear: pd.DataFrame) -> str:
    """Section 1: Sample size."""
    lines = []
    lines.append("## 1. Размер выборки")
    lines.append("")

    n_values = linear["n"].astype(int)
    n_total = n_values.iloc[0]
    n_models = len(linear)

    lines.append("| Показатель | Значение |")
    lines.append("|---|---|")
    lines.append(f"| Количество субъектов в анализе | {n_total} |")
    lines.append(f"| Количество моделей | {n_models} |")

    for model_name, row in linear.iterrows():
        lines.append(f"| n ({model_name}) | {int(row['n'])} |")

    lines.append("")
    return "\n".join(lines)


def section_2_linear_models(linear: pd.DataFrame) -> str:
    """Section 2: Linear models (ΔV ~ Median_ΔV1) for each field."""
    lines = []
    lines.append("## 2. Линейные модели")
    lines.append("")

    # Models grouped by pathway
    pathways = {
        "ΔV4 ~ ΔV1": ["delta_v4_left", "delta_v4_right"],
        "ΔV5 ~ ΔV1": ["delta_v5_left", "delta_v5_right"],
    }

    for pathway_name, model_keys in pathways.items():
        lines.append(f"### {pathway_name}")
        lines.append("")
        lines.append("| Поле | n | R² | Adjusted R² | β | p-value | residual_ratio |")
        lines.append("|---|---|---|---|---|---|---|")

        for key in model_keys:
            if key not in linear.index:
                continue
            row = linear.loc[key]
            field = key.split("_")[-1].upper()
            lines.append(
                f"| {field} "
                f"| {int(row['n'])} "
                f"| {fmt(row['r_squared'])} "
                f"| {fmt(row['adj_r_squared'])} "
                f"| {fmt(row['beta'])} "
                f"| {fmt(row['p_value'])} "
                f"| {fmt(row['residual_ratio'])} |"
            )

        lines.append("")

    # ΔR² left vs right
    lines.append("### ΔR² left vs right")
    lines.append("")
    lines.append("| Pathway | R²_left | R²_right | ΔR²_left_vs_right |")
    lines.append("|---|---|---|---|")

    for pathway_prefix in ["delta_v4", "delta_v5"]:
        left_key = f"{pathway_prefix}_left"
        right_key = f"{pathway_prefix}_right"
        if left_key in linear.index and right_key in linear.index:
            r2_left = linear.loc[left_key, "r_squared"]
            r2_right = linear.loc[right_key, "r_squared"]
            delta_r2 = r2_left - r2_right
            label = "ΔV4" if "v4" in pathway_prefix else "ΔV5"
            lines.append(
                f"| {label} "
                f"| {fmt(r2_left)} "
                f"| {fmt(r2_right)} "
                f"| {fmt(delta_r2)} |"
            )

    lines.append("")
    return "\n".join(lines)


def section_3_multiple_models(multiple: pd.DataFrame) -> str:
    """Section 3: Multiple models (ΔV ~ Median_ΔV1 + MAD)."""
    lines = []
    lines.append("## 3. Множественные модели")
    lines.append("")

    pathways = {
        "ΔV4 ~ ΔV1 + MAD": ["delta_v4_left", "delta_v4_right"],
        "ΔV5 ~ ΔV1 + MAD": ["delta_v5_left", "delta_v5_right"],
    }

    for pathway_name, model_keys in pathways.items():
        lines.append(f"### {pathway_name}")
        lines.append("")
        lines.append("| Поле | R²_simple | R²_multiple | ΔR² | Adjusted R² | std_β_median | std_β_MAD |")
        lines.append("|---|---|---|---|---|---|---|")

        for key in model_keys:
            if key not in multiple.index:
                continue
            row = multiple.loc[key]
            field = key.split("_")[-1].upper()
            lines.append(
                f"| {field} "
                f"| {fmt(row['r_squared_simple'])} "
                f"| {fmt(row['r_squared'])} "
                f"| {fmt(row['delta_r_squared'])} "
                f"| {fmt(row['adj_r_squared'])} "
                f"| {fmt(row['standardized_beta_median'])} "
                f"| {fmt(row['standardized_beta_mad'])} |"
            )

        lines.append("")

    # ΔR² summary
    lines.append("### ΔR² Summary")
    lines.append("")
    lines.append("| Категория | Модели |")
    lines.append("|---|---|")

    dr2_low = []
    dr2_high = []
    for key, row in multiple.iterrows():
        dr2 = row["delta_r_squared"]
        if dr2 < 0.02:
            dr2_low.append(f"{key} (ΔR²={fmt(dr2)})")
        if dr2 >= 0.05:
            dr2_high.append(f"{key} (ΔR²={fmt(dr2)})")

    lines.append(f"| ΔR² < 0.02 | {'; '.join(dr2_low) if dr2_low else '—'} |")
    lines.append(f"| ΔR² ≥ 0.05 | {'; '.join(dr2_high) if dr2_high else '—'} |")

    lines.append("")
    return "\n".join(lines)


def section_4_residual_correlations() -> str:
    """Section 4: Residual correlations — not available in stored CSV."""
    lines = []
    lines.append("## 4. Residual correlations")
    lines.append("")
    lines.append("Данные по корреляциям остатков (Corr(residual, PSI_tau), Corr(residual, Asym_abs), "
                 "Corr(residual, Asym_rel)) не сохранены в CSV-файлах.")
    lines.append("")
    return "\n".join(lines)


def section_5_heteroscedasticity(hetero: pd.DataFrame) -> str:
    """Section 5: Heteroscedasticity tests."""
    lines = []
    lines.append("## 5. Heteroscedasticity")
    lines.append("")
    lines.append("| Модель | n | BP-statistic | p-value | heteroscedastic | |resid| corr | |resid| p-value |")
    lines.append("|---|---|---|---|---|---|---|")

    for key, row in hetero.iterrows():
        lines.append(
            f"| {key} "
            f"| {int(row['n'])} "
            f"| {fmt(row['lm_statistic'])} "
            f"| {fmt(row['p_value'])} "
            f"| {row['heteroscedastic']} "
            f"| {fmt(row['abs_resid_correlation'])} "
            f"| {fmt(row['abs_resid_p_value'])} |"
        )

    lines.append("")
    return "\n".join(lines)


def section_6_tau_stability() -> str:
    """Section 6: τ stability — not available in stored CSV."""
    lines = []
    lines.append("## 6. τ stability")
    lines.append("")
    lines.append("Данные по стабильности τ (Mean τ, SD τ, CV τ, Corr(τ, PSI_count), "
                 "Corr(τ, PSI_range), Corr(τ, Median_ΔV1)) не сохранены в CSV-файлах.")
    lines.append("")
    return "\n".join(lines)


def section_7_distribution_diagnostics() -> str:
    """Section 7: Distribution diagnostics — not available in stored CSV."""
    lines = []
    lines.append("## 7. Distribution diagnostics")
    lines.append("")
    lines.append("Данные по диагностике распределений (Skewness, Kurtosis, % выбросов >3 SD) "
                 "не сохранены в CSV-файлах.")
    lines.append("")
    return "\n".join(lines)


def generate_report() -> str:
    """Generate the full 7-section numerical report."""
    linear, multiple, hetero = load_csv_files()

    sections = [
        "# Task 27.3 — Числовой Отчёт Production Run",
        "",
        "---",
        "",
        section_1_sample_size(linear),
        "---",
        "",
        section_2_linear_models(linear),
        "---",
        "",
        section_3_multiple_models(multiple),
        "---",
        "",
        section_4_residual_correlations(),
        "---",
        "",
        section_5_heteroscedasticity(hetero),
        "---",
        "",
        section_6_tau_stability(),
        "---",
        "",
        section_7_distribution_diagnostics(),
    ]

    return "\n".join(sections)


def main():
    print("=" * 60)
    print("Task 27.3C — Generating Numerical Report from CSV")
    print("=" * 60)
    print()

    # Verify source files exist
    for path in [LINEAR_CSV, MULTIPLE_CSV, HETERO_CSV]:
        if not path.exists():
            print(f"ERROR: Source file not found: {path}")
            return 1
        print(f"  ✓ Found: {path.name}")

    print()

    # Generate report
    report = generate_report()

    # Save
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"  → Report saved to: {OUTPUT_FILE}")
    print(f"  → Report length: {len(report)} characters")
    print()
    print("=" * 60)
    print("DONE")
    print("=" * 60)
    return 0


if __name__ == "__main__":
    exit(main())

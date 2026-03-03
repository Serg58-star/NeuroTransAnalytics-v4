import os
import shutil
from pathlib import Path

files_to_find = [
    "Stage_9D_Population_Differentiation_Audit (v3).md",
    "Stage_9D_SQLite_Schema_Audit_Report.md",
    "Stage_10_Real_Data_Pilot_Readiness_Protocol.md",
    "Protocol_Roles_and_Working_Model_NeuroTransAnalytics_v4.md",
    "v5_Synthetic_Architecture_Completion_Summary.md",
    "Task_50A_Z_Space_Geometric_Validation_Criteria_Update.md",
    "Task_51A_Z_Space_Severity_Centering_Correction.md",
    "Task_52A_Anchored_Projection_Framework_for_Phase_2_Dynamics.md",
    "Stage_9B_Functional_Monitoring_Framework_v5.md",
    "Stage_9B_Functional_Monitoring_Report.md",
    "Stage_9_PreAudit_Task_Report.md"
]

base_dir = Path("C:/NeuroTransAnalytics-v4")
docs_dir = base_dir / "docs"
dest_dir = docs_dir / "for_next_chat"
dest_dir.mkdir(parents=True, exist_ok=True)

found_files = []

for root, dirs, files in os.walk(docs_dir):
    if "for_next_chat" in root:
        continue
    for f in files:
        if f in files_to_find:
            src_path = Path(root) / f
            dest_path = dest_dir / f
            shutil.copy2(src_path, dest_path)
            found_files.append((f, str(src_path.relative_to(base_dir))))

with open(dest_dir / "FILES_FOR_STAGE_9D_NEXT_CHAT.md", "w", encoding="utf-8") as out:
    out.write("# Индекс файлов для Stage 9D Next Chat\n\n")
    out.write("## Скопированные файлы\n\n")
    for fname, rel_path in found_files:
        out.write(f"- **Название:** `{fname}`\n")
        out.write(f"  - **Исходное расположение:** `{rel_path}`\n")
        out.write(f"  - **Причина:** Обязательный документ согласно Stage 9D Execution Task\n")
        out.write(f"  - **Обязателен:** Да\n\n")
    out.write("---\n")
    out.write("## Данные для копирования в первый промпт следующего чата\n\n")
    out.write("### 1. Severity формула\n")
    out.write("`Severity(Z) = ||Z_patient||_2 / sqrt(3)`\n\n")
    out.write("### 2. Anchored Projection формула\n")
    out.write("`P_anchored(v) = v - (v \\cdot u_anchored) * u_anchored` (где `u_anchored` - вектор базовой группы/нормы)\n\n")
    out.write("### 3. ΔZ формула\n")
    out.write("`ΔZ = Z_test - Z_baseline`\n\n")
    out.write("### 4. Параметр Generator Stability\n")
    out.write("`κ = 0.08`\n\n")
    out.write("### 5. Anchored thresholds (S75, DII75)\n")
    out.write("Зафиксированы на значениях базового распределения (при κ=0).\n\n")
    out.write("### 6. PASS/FAIL критерии Stage 9D\n")
    out.write("- **Различие центров (Sex):** PASS: Δ ≤ 0.5 Z | FAIL: Δ > 1.0 Z\n")
    out.write("- **Различие ковариаций:** PASS: расхождение < 10% | FAIL: расхождение > 20%\n")
    out.write("- **Severity difference (Sex):** PASS: |Cohen’s d| < 0.3 | FAIL: |d| ≥ 0.5\n")
    out.write("- **Silhouette (Sex):** PASS: < 0.15 | FAIL: ≥ 0.25\n")
    out.write("- **Age correlation (Severity ~ Age):** PASS: |ρ| < 0.2 | FAIL: |ρ| ≥ 0.35\n")
    out.write("- **Age regression R2:** PASS: R2 < 0.05 | FAIL: R2 ≥ 0.10\n")
    out.write("- **Age Non-linear R2:** PASS: < 10% | FAIL: ≥ 15%\n")
    out.write("- **Age quartile drift:** PASS: ≤ 10% | FAIL: > 20%\n")
    out.write("- **Interaction (Sex x Age):** PASS: p ≥ 0.05 | FAIL: p < 0.01\n")
    out.write("- **Global PASS:** 0 FAILs. **Global FAIL:** ≥2 FAILs. **Borderline:** 1 FAIL.\n")

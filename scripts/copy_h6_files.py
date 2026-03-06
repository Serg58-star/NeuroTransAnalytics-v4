import os
import shutil

chat_dir = r'C:\NeuroTransAnalytics-v4\docs\for_next_chat'
os.makedirs(chat_dir, exist_ok=True)

files_to_copy = [
    r'C:\NeuroTransAnalytics-v4\docs\audit\Stage_H_Session_Full_Architectural_Summary.md',
    r'C:\NeuroTransAnalytics-v4\docs\audit\Stage_H2 — Empirical & Synthetic Consistency Audit.md',
    r'C:\NeuroTransAnalytics-v4\docs\audit\Stage_H2.2 — Baseline-Adjusted Empirical Geometry Audit.md',
    r'C:\NeuroTransAnalytics-v4\docs\audit\Stage_H2.2b — Subject-Level Spectral Recalculation (First-Visit Only).md',
    r'C:\NeuroTransAnalytics-v4\docs\audit\Stage_H3 — PSI Structural Contribution Audit.md',
    r'C:\NeuroTransAnalytics-v4\docs\audit\Stage_H3.1 — F1 Cross-Model Comparison.md',
    r'C:\NeuroTransAnalytics-v4\docs\audit\Stage_H3.1c — Correlated Motor Layer Simulation Audit.md',
    r'C:\NeuroTransAnalytics-v4\docs\audit\Stage_H3.2 — Δ-Space Cross-Model Comparison.md',
    r'C:\NeuroTransAnalytics-v4\docs\audit\Stage_H5 — Correlated Baseline Generator Redesign.md',
    r'C:\NeuroTransAnalytics-v4\docs\redesign\Stage_H4 — Decoupled Load Generator Redesign.md',
    r'C:\NeuroTransAnalytics-v4\docs\tasks\Task H5 — Implementation Plan.md',
    r'C:\NeuroTransAnalytics-v4\docs\v5\v5_Synthetic_Architecture_Completion_Summary.md',
    r'C:\NeuroTransAnalytics-v4\docs\v5\Stage_10_Real_Data_Pilot_Readiness_Protocol.md',
    r'C:\NeuroTransAnalytics-v4\docs\audit\H3_2_Block0_Data_Alignment.md',
    r'C:\NeuroTransAnalytics-v4\docs\audit\H3_2_Block1_Delta_Distribution.md',
    r'C:\NeuroTransAnalytics-v4\docs\audit\H3_2_Block2_Delta_Spectral_Geometry.md',
    r'C:\NeuroTransAnalytics-v4\docs\audit\H3_2_Block3_Delta_Demography.md',
    r'C:\NeuroTransAnalytics-v4\docs\audit\H3_2_Block4_Delta_Variance_Decomposition.md',
    r'C:\NeuroTransAnalytics-v4\docs\redesign\H4_Block1_Scale_Calibration.md',
    r'C:\NeuroTransAnalytics-v4\docs\redesign\H4_Block2_Spectral_Verification.md',
    r'C:\NeuroTransAnalytics-v4\docs\redesign\H4_Block3_Demographic_Decoupling.md',
    r'C:\NeuroTransAnalytics-v4\docs\redesign\H4_Block4_v5_Compatibility_Check.md'
]

with open(os.path.join(chat_dir, 'FILES_FOR_NEXT_CHAT.md'), 'w', encoding='utf-8') as f:
    f.write('# FILES FOR NEXT CHAT\n\n')
    f.write('| № | File | Purpose | Local Path |\n')
    f.write('| - | ---- | ------- | ---------- |\n')
    for i, path in enumerate(files_to_copy, 1):
        filename = os.path.basename(path)
        dest = os.path.join(chat_dir, filename)
        if os.path.exists(path):
            shutil.copy2(path, dest)
            f.write(f'| {i} | {filename} | Context/Audit | `docs/for_next_chat/{filename}` |\n')
        else:
            f.write(f'| {i} | {filename} | MISSING | `{path}` |\n')

memory_files = [
    'Stage_H_Session_Full_Architectural_Summary.md',
    'Task H5 — Implementation Plan.md',
    'Stage_H4 — Decoupled Load Generator Redesign.md',
    'Stage_H3.2 — Δ-Space Cross-Model Comparison.md',
    'v5_Synthetic_Architecture_Completion_Summary.md',
    'Stage_10_Real_Data_Pilot_Readiness_Protocol.md',
    'H4_Block4_v5_Compatibility_Check.md'
]

with open(os.path.join(chat_dir, 'CHAT_MEMORY_FILES.md'), 'w', encoding='utf-8') as f:
    f.write('# CHAT MEMORY FILES\n\n')
    f.write('These files must be loaded into the initial context window of the next chat.\n\n')
    f.write('| File | Purpose | Path |\n')
    f.write('| ---- | ------- | ---- |\n')
    for fname in memory_files:
        f.write(f'| {fname} | Core Architecture / Summary | `docs/for_next_chat/{fname}` |\n')

print('Script OK')

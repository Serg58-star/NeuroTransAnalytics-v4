import os
import re

base_dir = r"C:\Users\User\Desktop\legacy_SZR\SZR_testing_program_files\Новая версия тестов_Ким_А_02_09_2017\Reactest"
folders = ["Тест 1", "Тест 2", "Тест 3"]
out_dir = r"c:\NeuroTransAnalytics-v4\docs\legacy\stimulus_protocol"
os.makedirs(out_dir, exist_ok=True)

stim_kw = ['sequence', 'arr', 'stim', 'color', 'pos', 'disc', 'circle']
time_kw = ['interval', 'delay', 'rotate', 'timer', 'period']
seq_kw = ['rotation', 'shift', 'sequence', 'pattern', 'arr']

sections_md = ["# Config Sections\n"]
full_idx_md = ["# Config Full Index\n"]
stim_md = ["# Config Stimulus Parameters\n"]
time_md = ["# Config Timing Parameters\n"]
seq_md = ["# Config Sequence Data\n"]

for md_list in [full_idx_md, stim_md, time_md, seq_md]:
    md_list.extend(["| Section | Key | Value |", "|---|---|---|"])

for folder in folders:
    config_path = os.path.join(base_dir, folder, "config.ini")
    sections_md.append(f"\n## `Reactest\\{folder}\\config.ini`\n")
    
    if os.path.exists(config_path):
        current_section = ""
        with open(config_path, "r", encoding="windows-1251", errors="ignore") as f:
            lines = f.readlines()
            
        # Parse logic
        for line in lines:
            line = line.strip()
            if not line or line.startswith(";"):
                continue
            
            section_match = re.match(r"\[(.*?)\]", line)
            if section_match:
                current_section = section_match.group(1)
                sections_md.append(f"- `[{current_section}]`")
                # Add section dividers to the tables
                for md_list in [full_idx_md, stim_md, time_md, seq_md]:
                    md_list.append(f"| **`[{folder}]`** | **`[{current_section}]`** | |")
                continue
                
            if "=" in line:
                parts = line.split("=", 1)
                key = parts[0].strip()
                val = parts[1].strip()
                
                key_lower = key.lower()
                
                # Format value to escape markdown pipes
                safe_val = val.replace("|", "\\|")
                
                row = f"| {current_section} | {key} | {safe_val} |"
                
                full_idx_md.append(row)
                
                if any(kw in key_lower for kw in stim_kw):
                    stim_md.append(row)
                if any(kw in key_lower for kw in time_kw):
                    time_md.append(row)
                if any(kw in key_lower for kw in seq_kw) or "[" in val or "," in val: # heuristics for arrays
                    seq_md.append(row)
    else:
        sections_md.append(f"*(config.ini not found in {folder})*\n")


with open(os.path.join(out_dir, "config_sections.md"), "w", encoding="utf-8") as f:
    f.write("\n".join(sections_md))
with open(os.path.join(out_dir, "config_full_index.md"), "w", encoding="utf-8") as f:
    f.write("\n".join(full_idx_md))
with open(os.path.join(out_dir, "config_stimulus_parameters.md"), "w", encoding="utf-8") as f:
    f.write("\n".join(stim_md))
with open(os.path.join(out_dir, "config_timing_parameters.md"), "w", encoding="utf-8") as f:
    f.write("\n".join(time_md))
with open(os.path.join(out_dir, "config_sequence_data.md"), "w", encoding="utf-8") as f:
    f.write("\n".join(seq_md))

print(f"Generated extraction documents to {out_dir}")

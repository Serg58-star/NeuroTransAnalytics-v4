import os
import re

target_dir = r"C:\Users\User\Desktop\legacy_SZR\SZR_testing_program_files\Новая версия тестов_Ким_А_02_09_2017"
out_dir = r"c:\NeuroTransAnalytics-v4\docs\audit_legacy\code_index"

# 1. Structure
struct_md = ["# Delphi Project Structure\n"]
for root, _, files in os.walk(target_dir):
    for f in files:
        if f.lower().endswith('.dpr') and 'backup' not in root.lower():
            struct_md.append(f"## Project: {f} (in {os.path.relpath(root, target_dir)})\n")
            with open(os.path.join(root, f), 'r', encoding='windows-1251', errors='ignore') as dpr:
                content = dpr.read()
                # find uses
                uses_match = re.search(r'uses(.*?);', content, re.IGNORECASE | re.DOTALL)
                if uses_match:
                    struct_md.append("- **Modules (uses):** " + uses_match.group(1).replace('\n', ' ').strip() + "\n")
                
                # find forms/initialization
                init_lines = [l.strip() for l in content.split('\n') if 'Application.CreateForm' in l or 'Application.Initialize' in l or 'Application.Run' in l]
                if init_lines:
                    struct_md.append("\n- **Initialization/Forms:**\n```pascal\n" + '\n'.join(init_lines) + "\n```\n")

open(os.path.join(out_dir, "Delphi_Project_Structure.md"), "w", encoding='utf-8').write('\n'.join(struct_md))

# 2. Module Index
mod_md = ["# Legacy Module Index\n", "| module | procedures | functions | notes |", "|---|---|---|---|"]
for root, _, files in os.walk(target_dir):
    for f in files:
        if f.lower().endswith('.pas') and 'backup' not in root.lower():
            with open(os.path.join(root, f), 'r', encoding='windows-1251', errors='ignore') as pas:
                content = pas.read()
                procs = re.findall(r'procedure\s+([A-Za-z0-9_\.]+)', content, re.IGNORECASE)
                funcs = re.findall(r'function\s+([A-Za-z0-9_\.]+)', content, re.IGNORECASE)
                procs_str = "<br>".join(set(procs)) if procs else "None"
                funcs_str = "<br>".join(set(funcs)) if funcs else "None"
                mod_md.append(f"| {f} | {procs_str} | {funcs_str} |  |")
                
open(os.path.join(out_dir, "Legacy_Module_Index.md"), "w", encoding='utf-8').write('\n'.join(mod_md))

# 3, 4, 5 Extracts
def extract_snippet(file_path, keywords):
    snippets = []
    lines = open(file_path, 'r', encoding='windows-1251', errors='ignore').readlines()
    pattern = re.compile(r'\b(' + '|'.join(keywords) + r')\b', re.IGNORECASE)
    
    i = 0
    while i < len(lines):
        if pattern.search(lines[i]):
            start = max(0, i-2)
            end = min(len(lines), i+3)
            snip = "".join(lines[start:end])
            snippets.append(snip)
            i = end # skip overlapping contexts
        else:
            i += 1
            
    return snippets

stim_kw = ['stim', 'signal', 'color', 'draw', 'canvas', 'pixel', 'timer', 'interval', 'random', 'position', 'x', 'y', 'rect', 'circle']
resp_kw = ['key', 'mouse', 'click', 'reaction', 'time', 'keypress', 'keydown', 'latency', 'response']
res_kw = ['mean', 'sd', 'average', 'median', 'variance', 'result', 'score', 'stat', 'analysis']

stim_md = ["# Stimulus Code Extracts\n"]
resp_md = ["# Response Handling Code\n"]
res_md = ["# Result Processing Code\n"]

for root, _, files in os.walk(target_dir):
    for f in files:
        if (f.lower().endswith('.pas') or f.lower().endswith('.dpr')) and 'backup' not in root.lower():
            path = os.path.join(root, f)
            rel = os.path.relpath(path, target_dir)
            
            s_snips = extract_snippet(path, stim_kw)
            if s_snips: 
                stim_md.append(f"## {rel}\n```pascal\n" + "\n...\n".join(s_snips) + "\n```\n")
                
            r_snips = extract_snippet(path, resp_kw)
            if r_snips: 
                resp_md.append(f"## {rel}\n```pascal\n" + "\n...\n".join(r_snips) + "\n```\n")
                
            re_snips = extract_snippet(path, res_kw)
            if re_snips: 
                res_md.append(f"## {rel}\n```pascal\n" + "\n...\n".join(re_snips) + "\n```\n")

open(os.path.join(out_dir, "Stimulus_Code_Extracts.md"), "w", encoding='utf-8').write('\n'.join(stim_md))
open(os.path.join(out_dir, "Response_Handling_Code.md"), "w", encoding='utf-8').write('\n'.join(resp_md))
open(os.path.join(out_dir, "Result_Processing_Code.md"), "w", encoding='utf-8').write('\n'.join(res_md))

import os
import shutil
from pathlib import Path

# Configuration
PROJECT_ROOT = Path(r"C:\NeuroTransAnalytics-v4")
TARGET_DIR = PROJECT_ROOT / "docs" / "for_next_chat"

# The specific files requested
TARGET_FILES = [
    "1_Research_Paradigm_NeuroTransAnalytics.md",
    "2_Research_Axes_and_Test_Conditions_v4.md",
    "6_Test_design_and_PSI_metadata_v4.md",
    "11_1_C2_1_Data_Model_v4.md",
    "11_2_C2_2_Physical_Storage_Design.md",
    "12_2_C3_2_Component_Timing_Computation_v4.md",
    "Robust Statistics Standard.md",
    "NeuroTransAnalytics Research Control Document (Chat Bootstrap).md",
    "Protocol_Architecture_Alignment_v4.md",
    "Appendix_A_Data_and_Legacy_Context.md",
    "Как устроено тестирование СЗР в деталях.md",
    "config_stimulus_parameters.md",
    "config_timing_parameters.md",
    "config_sequence_data.md",
    "config_sections.md",
    "config_full_index.md"
]

def prepare_directory():
    if TARGET_DIR.exists():
        print(f"Clearing existing directory: {TARGET_DIR}")
        shutil.rmtree(TARGET_DIR)
    TARGET_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Created clean directory: {TARGET_DIR}")

def find_and_copy_files():
    found_files = []
    missing_files = list(TARGET_FILES)

    # Search the whole project root (or just docs and root)
    for root, dirs, files in os.walk(PROJECT_ROOT):
        # Skip standard ignore dirs to speed up
        if any(ignored in root for ignored in ['.git', '__pycache__', '.venv', '.gemini']):
            continue

        for file in files:
            if file in missing_files:
                source_path = Path(root) / file
                target_path = TARGET_DIR / file
                
                # Copy file
                shutil.copy2(source_path, target_path)
                print(f"Found and copied: {file} (from {source_path})")
                
                found_files.append(file)
                missing_files.remove(file)
                
                if not missing_files:
                    break
        if not missing_files:
            break

    if missing_files:
        print("\nWARNING: The following files were not found:")
        for mf in missing_files:
            print(f"  - {mf}")
            
    return found_files

def generate_index(found_files):
    index_path = TARGET_DIR / "NEXT_CHAT_FILE_INDEX.md"
    with open(index_path, "w", encoding="utf-8") as f:
        f.write("# Next Chat File Index\n\n")
        f.write("This directory contains the context package specifically gathered for the next chat session.\n\n")
        f.write("## Copied Documents:\n\n")
        
        # Sort to output exactly as requested or alphabetically
        for file in TARGET_FILES:
            if file in found_files:
                f.write(f"- [x] {file}\n")
            else:
                f.write(f"- [ ] {file} (MISSING)\n")
                
    print(f"\nGenerated index file: {index_path}")

if __name__ == "__main__":
    prepare_directory()
    found = find_and_copy_files()
    generate_index(found)
    print("Done.")

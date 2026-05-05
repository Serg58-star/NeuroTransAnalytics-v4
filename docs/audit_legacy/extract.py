import os
import datetime

target_dir = r"C:\Users\User\Desktop\legacy_SZR\SZR_testing_program_files\Новая версия тестов_Ким_А_02_09_2017"
output_dir = r"c:\NeuroTransAnalytics-v4\docs\audit_legacy\code_index"
os.makedirs(output_dir, exist_ok=True)

index_file = os.path.join(output_dir, "Legacy_Source_File_Index.md")

with open(index_file, "w", encoding="utf-8") as f:
    f.write("# Legacy Source File Index\n\n")
    f.write("| file_name | path | type | size | modified_date |\n")
    f.write("|---|---|---|---|---|\n")
    for root, dirs, files in os.walk(target_dir):
        for file in files:
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, target_dir)
            ext = os.path.splitext(file)[1]
            size = os.path.getsize(full_path)
            mtime = os.path.getmtime(full_path)
            dt = datetime.datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"| {file} | {rel_path} | {ext} | {size} | {dt} |\n")

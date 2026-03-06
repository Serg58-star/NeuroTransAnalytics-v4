import sqlite3
import pandas as pd
import numpy as np
import datetime
from pathlib import Path

def prepare_stage_9d1_data():
    db_path = 'neuro_data.db'
        
    conn = sqlite3.connect(db_path)
    
    # Extract records using explicit JOIN per protocol 4.1
    query = """
    SELECT
        u.birth_date,
        u.gender,
        t.*
    FROM trials t
    JOIN users u
    ON t.subject_id = u.subject_id;
    """
    
    df_raw = pd.read_sql_query(query, conn)
    conn.close()
    
    total_raw_records = len(df_raw)
    
    # 4.3 Exclusion tracking
    dropped_gender_null = 0
    dropped_birth_null = 0
    dropped_test_null = 0
    dropped_date_parse_error = 0
    
    valid_indices = []
    ages = []
    
    # Iterate and validate manually to cleanly parse dates and track exact exclusion reasons
    for idx, row in df_raw.iterrows():
        # Check basic nulls
        if pd.isna(row['gender']):
            dropped_gender_null += 1
            ages.append(np.nan)
            continue
            
        if pd.isna(row['birth_date']):
            dropped_birth_null += 1
            ages.append(np.nan)
            continue
            
        if pd.isna(row['test_date']):
            dropped_test_null += 1
            ages.append(np.nan)
            continue
            
        # 4.2 Parse dates & calculate age
        try:
            # handle formats like YYYY-MM-DD
            birth_dt = pd.to_datetime(row['birth_date'], format='mixed', dayfirst=True)
            test_dt = pd.to_datetime(row['test_date'], format='mixed', dayfirst=True)
            
            age = (test_dt - birth_dt).days / 365.25
            ages.append(age)
            valid_indices.append(idx)
        except Exception as e:
            dropped_date_parse_error += 1
            ages.append(np.nan)
            continue

    df_raw['age'] = ages
    
    # Retain strictly valid rows
    df_valid = df_raw.loc[valid_indices].copy()
    
    # Format output according to Protocol 5
    # Remove duplicate joined columns
    # We joined t.* which includes subject_id, test_date, trial_id again, usually pandas suffixes columns or keeps both depending on read_sql. 
    # Let's cleanly construct the requested columns explicitly.
    cols_to_keep = ['trial_id', 'subject_id', 'gender', 'age', 'test_date', 'session_condition']
    
    # Get RT fields
    rt_cols = [c for c in df_valid.columns if c.startswith('tst')]
    
    # We must deduplicate columns if pandas `*` produced duplicates
    df_valid = df_valid.loc[:,~df_valid.columns.duplicated()]
    
    final_cols = []
    for c in cols_to_keep:
        if c in df_valid.columns:
            final_cols.append(c)
    
    final_cols.extend(rt_cols)
    
    # remove duplicate columns in the final list
    final_cols = list(dict.fromkeys(final_cols))
    
    df_out = df_valid[final_cols]
    
    final_record_count = len(df_out)
    
    # Ensure directory exists
    out_dir = Path("docs/v5")
    out_dir.mkdir(parents=True, exist_ok=True)
    
    # Save CSV
    df_out.to_csv(out_dir / "stage_9d1_prepared_dataset.csv", index=False)
    
    # 6. Generate Report
    report_path = out_dir / "Stage_9D_1_Data_Preparation_Report.md"
    
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("# Stage 9D.1 Data Preparation Report\n\n")
        f.write("## 1. Общее количество записей до фильтрации\n")
        f.write(f"- Извлечено записей (INNER JOIN trials и users): {total_raw_records}\n\n")
        
        f.write("## 2. Количество исключённых по каждому критерию\n")
        f.write(f"- Отсутствует пол (gender IS NULL): {dropped_gender_null}\n")
        f.write(f"- Отсутствует дата рождения (birth_date IS NULL): {dropped_birth_null}\n")
        f.write(f"- Отсутствует дата теста (test_date IS NULL): {dropped_test_null}\n")
        f.write(f"- Ошибка парсинга дат: {dropped_date_parse_error}\n\n")
        
        f.write("## 3. Итоговый размер датасета\n")
        f.write(f"- Итоговых валидных записей: {final_record_count}\n\n")
        
        f.write("## 4. Подтверждение вычисления возраста\n")
        f.write("- Возраст (Age) успешно вычислен для всех валидных строк на основе разницы test_date и birth_date деленной на 365.25. Сохранен в формате float (например, 23.45).\n\n")
        
        f.write("## 5. Подтверждение сохранения множественных тестов\n")
        f.write("- Все множественные тесты (trial_id) для одного subject_id сохранены как независимые строки.\n")
        f.write("- Агрегирование по субъекту не применялось.\n\n")
        
        f.write("## 6. Подтверждение отсутствия RT-фильтрации\n")
        f.write("- Фильтрация по экстремальным RT, экстремумам или пропускам реакций строго не выполнялась.\n")
        f.write("- Запрещенные операции (trimming, winsorizing, нормализация) не применялись.\n\n")
        
        f.write("---\n")
        f.write("Статистический анализ на этапе Stage 9D.1 не выполнялся.\n")

if __name__ == "__main__":
    prepare_stage_9d1_data()

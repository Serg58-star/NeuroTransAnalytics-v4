# FILE: src/neurotransanalytics/data_adapter/loaders/warmup_loader.py

import pandas as pd
from pathlib import Path


def load_warmup_table(path: Path) -> dict[str, pd.DataFrame]:
    """
    Загружает stimulus_warmup.xlsx.

    Возвращает:
        dict[test_type, DataFrame]

    Где test_type ∈ {"Tst1", "Tst2", "Tst3"}
    и каждый DataFrame содержит warmup-блоки.
    """
    xls = pd.ExcelFile(path)

    tables: dict[str, pd.DataFrame] = {}

    for sheet in xls.sheet_names:
        # ожидаемые имена листов: Tst1_warmup, Tst2_warmup, Tst3_warmup
        if not sheet.endswith("_warmup"):
            continue

        test_type = sheet.replace("_warmup", "")
        df = xls.parse(sheet)

        # базовая нормализация
        df["order"] = df["order"].astype(int)
        df["psi_before_ms"] = df["psi_before_ms"].astype(int)

        tables[test_type] = df

    return tables

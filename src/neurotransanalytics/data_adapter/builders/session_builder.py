# FILE: src/neurotransanalytics/data_adapter/builders/session_builder.py

import pandas as pd


TEST_TYPES = ["Tst1", "Tst2", "Tst3"]


def build_sessions(boxbase_df: pd.DataFrame) -> pd.DataFrame:
    """
    Нормализация TestSession (v1).

    Из одной строки boxbase формирует 3 сессии:
    - Tst1 (simple / ПЗР)
    - Tst2 (color_red)
    - Tst3 (shift)

    Возвращает DataFrame со столбцами:
    - session_id
    - subject_id
    - test_type
    - source_row_index
    """

    sessions = []

    session_counter = 1

    for row_idx, row in boxbase_df.iterrows():
        subject_id = row.get("subject_id") or row.get("SubjectID") or row.get("id")

        for test_type in TEST_TYPES:
            sessions.append(
                {
                    "session_id": session_counter,
                    "subject_id": subject_id,
                    "test_type": test_type,
                    "source_row_index": row_idx,
                }
            )
            session_counter += 1

    return pd.DataFrame(sessions)

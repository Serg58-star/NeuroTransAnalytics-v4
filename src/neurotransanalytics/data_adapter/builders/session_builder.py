# FILE: src/neurotransanalytics/data_adapter/builders/session_builder.py

from typing import List

from ..models.session import Session


def build_sessions(boxbase_df) -> List[Session]:
    """
    Построение Session из boxbase.xlsx.

    Инварианты v4:
    - session_id берётся из колонки 'cnt'
    - test_type определяется по наличию Tst1_*, Tst2_*, Tst3_* колонок
    - warmup_variant НЕ фиксировался в данных:
        -> задаётся детерминированно
        -> в формате идентификатора Excel (например 'NU0')
    """

    sessions: List[Session] = []

    session_ids = boxbase_df["cnt"].unique()

    for session_id in session_ids:
        rows = boxbase_df[boxbase_df["cnt"] == session_id]
        columns = rows.columns

        # Определяем тип теста
        if any(col.startswith("Tst1_") for col in columns):
            test_type = "Tst1"
        elif any(col.startswith("Tst2_") for col in columns):
            test_type = "Tst2"
        elif any(col.startswith("Tst3_") for col in columns):
            test_type = "Tst3"
        else:
            raise ValueError(
                f"Cannot determine test_type for session {session_id}"
            )

        # Реальный warmup-вариант неизвестен → фиксируем допустимый
        warmup_variant = "NU0"

        session = Session(
            session_id=session_id,
            test_type=test_type,
            warmup_variant=warmup_variant,
        )

        sessions.append(session)

    return sessions

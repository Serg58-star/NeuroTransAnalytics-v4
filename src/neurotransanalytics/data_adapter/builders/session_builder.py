# FILE: src/neurotransanalytics/data_adapter/builders/session_builder.py

from dataclasses import dataclass


@dataclass
class Session:
    session_id: int
    test_type: str
    test_length: int


def build_sessions(boxbase_df):
    """
    Строит список Session из boxbase.xlsx.

    Инвариант:
    - идентификатор сессии = колонка 'cnt'
    """

    sessions = []

    # ЖЁСТКО зафиксировано для boxbase.xlsx
    grouped = boxbase_df.groupby("cnt")

    for cnt_value, df in grouped:
        # тип теста определяется по наличию столбцов
        if any(col.startswith("Tst1_") for col in df.columns):
            test_type = "Tst1"
            test_length = 36
        elif any(col.startswith("Tst2_") for col in df.columns):
            test_type = "Tst2"
            test_length = 36
        elif any(col.startswith("Tst3_") for col in df.columns):
            test_type = "Tst3"
            test_length = 36
        else:
            continue

        sessions.append(
            Session(
                session_id=int(cnt_value),
                test_type=test_type,
                test_length=test_length,
            )
        )

    return sessions

# FILE: src/neurotransanalytics/data_adapter/design/warmup_design.py

import pandas as pd


class WarmupDesign:
    """
    Warmup-дизайн v4.

    Источник истины:
      - stimulus_warmup.xlsx

    Структура таблицы:
      test_type | variant | order | psi_before_ms | stimulus_color | stimulus_localization
    """

    def __init__(self, warmup_path):
        self.warmup_path = warmup_path
        self.df = pd.read_excel(warmup_path)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def get_psi(self, test_type: str, variant: str, order: int) -> int:
        """
        Возвращает PSI для warmup-события.
        """

        df = self.df

        mask = (
            (df["test_type"] == test_type) &
            (df["variant"] == variant) &
            (df["order"] == order)
        )

        row = df.loc[mask]

        if row.empty:
            raise KeyError(
                f"No warmup PSI for test_type={test_type}, "
                f"variant={variant}, order={order}"
            )

        psi = row.iloc[0]["psi_before_ms"]

        if pd.isna(psi):
            raise KeyError(
                f"Empty PSI for test_type={test_type}, "
                f"variant={variant}, order={order}"
            )

        return int(psi)

    def get_stimulus_attrs(self, test_type: str, variant: str, order: int):
        """
        Возвращает (stimulus_color, stimulus_localization)
        для warmup-события.
        """

        df = self.df

        mask = (
            (df["test_type"] == test_type) &
            (df["variant"] == variant) &
            (df["order"] == order)
        )

        row = df.loc[mask]

        if row.empty:
            return None, None

        r = row.iloc[0]
        return r["stimulus_color"], r["stimulus_localization"]

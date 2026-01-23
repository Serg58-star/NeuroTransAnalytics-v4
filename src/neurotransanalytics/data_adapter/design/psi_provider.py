# FILE: src/neurotransanalytics/data_adapter/design/psi_provider.py

class PSIProvider:
    def __init__(self, warmup_tables: dict, test_design):
        """
        warmup_tables:
            dict[test_type -> pandas.DataFrame]
        test_design:
            TestDesign
        """
        self.warmup_tables = warmup_tables
        self.test_design = test_design

    # ---------- WARMUP ----------

    def get_warmup_psi(self, test_type: str, variant: str, order: int) -> int:
        df = self.warmup_tables[test_type]

        row = df[
            (df["variant"] == variant) &
            (df["order"] == order)
        ]

        if row.empty:
            raise KeyError(
                f"No warmup PSI for {test_type}, {variant}, order={order}"
            )

        return int(row.iloc[0]["psi_before_ms"])

    # ---------- TEST ----------

    def get_test_psi(self, test_type: str, stimulus_index: int) -> int:
        return self.test_design.get_psi(test_type, stimulus_index)

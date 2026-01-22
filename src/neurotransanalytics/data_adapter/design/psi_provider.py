# FILE: src/neurotransanalytics/data_adapter/design/psi_provider.py

class PSIProvider:
    """
    Источник PSI для warmup и test фаз.
    Инкапсулирует доступ к config_old.ini и test_metadata_old.py.
    """

    def __init__(self, warmup_design, test_design):
        self.warmup_design = warmup_design
        self.test_design = test_design

    # -------- Warmup --------
    def get_warmup_psi(self, test_type: str, warmup_index: int) -> int:
        """
        Возвращает PSI (мс) для warmup-стимула.
        warmup_index: 1..3
        """
        # Минимальная реализация v0:
        # warmup_design уже знает PSI как число (или хранит вычисленное).
        return self.warmup_design.get_psi(test_type, warmup_index)

    # -------- Test --------
    def get_test_psi(self, test_type: str, test_index: int) -> int:
        """
        Возвращает PSI (мс) для test-стимула.
        test_index: 1..36
        """
        return self.test_design.get_psi(test_type, test_index)

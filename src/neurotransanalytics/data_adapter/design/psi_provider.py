# FILE: src/neurotransanalytics/data_adapter/design/psi_provider.py

class PSIProvider:
    """
    Единая точка доступа к PSI для всех типов стимулов.

    Делегирует:
      - warmup PSI -> WarmupDesign
      - test PSI   -> TestDesign
    """

    def __init__(self, warmup_design, test_design):
        self.warmup_design = warmup_design
        self.test_design = test_design

    # ------------------------------------------------------------------
    # Warmup PSI
    # ------------------------------------------------------------------

    def get_warmup_psi(self, test_type: str, variant: int, order: int) -> int:
        """
        PSI перед warmup-стимулом.
        """
        return self.warmup_design.get_psi(
            test_type=test_type,
            variant=variant,
            order=order,
        )

    # ------------------------------------------------------------------
    # Test PSI
    # ------------------------------------------------------------------

    def get_test_psi(self, test_type: str, test_index: int) -> int:
        """
        PSI перед test-стимулом.
        """
        return self.test_design.get_psi(
            test_type=test_type,
            stimulus_index=test_index,
        )

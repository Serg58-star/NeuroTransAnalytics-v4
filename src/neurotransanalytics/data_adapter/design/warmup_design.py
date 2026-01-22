# FILE: src/neurotransanalytics/data_adapter/design/warmup_design.py

class WarmupDesign:
    """
    Warmup-дизайн из config_old.ini.
    v0: возвращает уже вычисленный PSI для каждого warmup-индекса.
    """

    def __init__(self, config):
        self.config = config

    def get_psi(self, test_type: str, warmup_index: int) -> int:
        """
        test_type: 'Tst1' | 'Tst2' | 'Tst3'
        warmup_index: 1..3
        """
        # v0: берём PSI напрямую из конфига по договорённости
        # Пример для ПЗР (Tst1): секция T1_NU*, ключ '1','2','3'
        section = self._resolve_section(test_type)
        return int(self.config[section][str(warmup_index)])

    def _resolve_section(self, test_type: str) -> str:
        # минимальная маршрутизация
        if test_type == "Tst1":
            return "T1_NU0"
        if test_type == "Tst2":
            return "T2_NU0"
        if test_type == "Tst3":
            return "T3_NU0"
        raise ValueError(f"Unknown test_type: {test_type}")

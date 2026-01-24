# FILE: src/neurotransanalytics/data_adapter/design/test_design.py

from pathlib import Path
import importlib.util


class TestDesign:
    """
    Канонический доступ к тестовым метаданным v4.

    Источник истины:
        test_metadata_old.py

    Принцип:
        - ничего не вычисляет
        - только читает через TestMetadataManager
    """

    TEST_TYPE_MAP = {
        "Tst1": "simple",
        "Tst2": "color_red",
        "Tst3": "shift",
    }

    def __init__(self, metadata_path: Path):
        self.module = self._load_module(metadata_path)
        self.manager = self.module.TestMetadataManager()

    # ------------------------------------------------------------------
    # loading
    # ------------------------------------------------------------------

    @staticmethod
    def _load_module(path: Path):
        spec = importlib.util.spec_from_file_location(
            "test_metadata_old", path
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    # ------------------------------------------------------------------
    # Unified API (используется PSIProvider / StimulusBuilder)
    # ------------------------------------------------------------------

    def get_psi(self, test_type: str, stimulus_index: int) -> int:
        meta = self._get_stimulus(test_type, stimulus_index)
        return meta.prestimulus_interval

    def get_color(self, test_type: str, stimulus_index: int):
        meta = self._get_stimulus(test_type, stimulus_index)
        return meta.color

    def get_location(self, test_type: str, stimulus_index: int):
        meta = self._get_stimulus(test_type, stimulus_index)
        return meta.position

    def get_circle_sequence(self, test_type: str, stimulus_index: int):
        meta = self._get_stimulus(test_type, stimulus_index)
        return meta.circle_sequence

    def get_shift_parameter(self, test_type: str, stimulus_index: int):
        meta = self._get_stimulus(test_type, stimulus_index)
        return meta.shift_parameter

    # ------------------------------------------------------------------
    # Aggregated attributes (ТО, ЧЕГО НЕ ХВАТАЛО)
    # ------------------------------------------------------------------

    def get_stimulus_attributes(self, test_type: str, stimulus_index: int) -> dict:
        """
        Возвращает все атрибуты тестового стимула одним словарём.
        Используется в stimulus_builder.py.
        """
        meta = self._get_stimulus(test_type, stimulus_index)

        return {
            "stimulus_color": meta.color,
            "stimulus_location": meta.position,
            "circle_sequence": meta.circle_sequence,
            "shift_parameter": meta.shift_parameter,
        }

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _get_stimulus(self, test_type: str, stimulus_index: int):
        if test_type not in self.TEST_TYPE_MAP:
            raise KeyError(f"Unknown test_type: {test_type}")

        key = self.TEST_TYPE_MAP[test_type]

        try:
            test_meta = self.manager._metadata_cache[key]
            return test_meta.get_stimulus(stimulus_index)
        except Exception as exc:
            raise KeyError(
                f"{test_type}: stimulus_index={stimulus_index} not found"
            ) from exc

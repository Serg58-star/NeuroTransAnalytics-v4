# FILE: src/neurotransanalytics/data_adapter/design/test_design.py

import importlib.util


class TestDesign:
    """
    Адаптер PSI для test-фазы.

    Реальные ключи metadata (по факту legacy-кода):
    - 'simple'     -> ПЗР
    - 'color_red'  -> тест на красный цвет
    - 'shift'      -> тест на сдвиг
    """

    TEST_TYPE_TO_META_KEY = {
        "Tst1": "simple",
        "Tst2": "color_red",
        "Tst3": "shift",
    }

    def __init__(self, path):
        spec = importlib.util.spec_from_file_location("test_metadata_old", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        self.module = module
        self.manager = module.TestMetadataManager()

    def get_psi(self, test_type: str, test_index: int) -> int:
        """
        Возвращает PSI (мс) для test-стимула.

        test_type: 'Tst1' | 'Tst2' | 'Tst3'
        test_index: 1..36
        """

        meta_key = self.TEST_TYPE_TO_META_KEY.get(test_type)
        if meta_key is None:
            raise ValueError(f"Unknown test_type: {test_type}")

        test_meta = self.manager._metadata_cache.get(meta_key)
        if test_meta is None:
            raise KeyError(
                f"Metadata key '{meta_key}' not found. "
                f"Available keys: {list(self.manager._metadata_cache.keys())}"
            )

        try:
            stimulus_meta = test_meta.stimuli[test_index - 1]
        except IndexError:
            raise IndexError(
                f"Test '{meta_key}': stimulus index {test_index} out of range"
            )

        psi = stimulus_meta.prestimulus_interval
        if psi is None:
            raise ValueError(
                f"PSI is None for test '{meta_key}', stimulus {test_index}"
            )

        return int(psi)

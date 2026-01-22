# FILE: src/neurotransanalytics/data_adapter/adapter_v0.py

from pathlib import Path

from .loaders.users_loader import load_users
from .loaders.boxbase_loader import load_boxbase
from .loaders.config_loader import load_config

from .design.warmup_design import WarmupDesign
from .design.test_design import TestDesign

from .builders.subject_builder import build_subjects
from .builders.session_builder import build_sessions
from .builders.stimulus_builder import build_stimulus_events
from .builders.response_builder import build_response_events


class DataAdapterV0:
    """
    Оркестратор data-adapter v0.
    Никакой аналитики. Только сборка C2.1-сущностей.
    """

    def __init__(self, data_dir: Path):
        self.data_dir = data_dir

    def run(self):
        users_df = load_users(self.data_dir / "users.xlsx")
        boxbase_df = load_boxbase(self.data_dir / "boxbase.xlsx")
        config = load_config(self.data_dir / "config_old.ini")

        warmup_design = WarmupDesign(config)
        test_design = TestDesign(self.data_dir / "test_metadata_old.py")

        subjects = build_subjects(users_df)
        sessions = build_sessions(boxbase_df)
        stimuli = build_stimulus_events(sessions, warmup_design, test_design)
        responses = build_response_events(sessions, stimuli)


        return subjects, sessions, stimuli, responses

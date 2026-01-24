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
    Data-adapter v0 for NeuroTransAnalytics v4.

    Responsibilities:
      - load raw input files
      - build domain objects (Subject, Session, StimulusEvent, ResponseEvent)
      - ensure PSI and metadata are attached
    """

    def __init__(self, data_dir: Path):
        self.data_dir = data_dir

    def run(self):
        # ------------------------------------------------------------
        # Load raw data
        # ------------------------------------------------------------
        users_df = load_users(self.data_dir / "users.xlsx")
        boxbase_df = load_boxbase(self.data_dir / "boxbase.xlsx")

        # config_old.ini остаётся только для test_metadata / legacy
        config = load_config(self.data_dir / "config_old.ini")

        # ------------------------------------------------------------
        # Build domain entities
        # ------------------------------------------------------------
        subjects = build_subjects(users_df)
        sessions = build_sessions(boxbase_df)

        # ------------------------------------------------------------
        # Designs
        # ------------------------------------------------------------
        warmup_design = WarmupDesign(
            warmup_path=self.data_dir / "stimulus_warmup.xlsx"
        )

        test_design = TestDesign(
            metadata_path=self.data_dir / "test_metadata_old.py"
        )

        # ------------------------------------------------------------
        # Stimuli & responses
        # ------------------------------------------------------------
        stimuli = build_stimulus_events(
            sessions=sessions,
            warmup_design=warmup_design,
            test_design=test_design,
        )

        responses = build_response_events(
            boxbase_df=boxbase_df,
            stimuli=stimuli,
        )

        return subjects, sessions, stimuli, responses

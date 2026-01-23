# FILE: src/neurotransanalytics/data_adapter/adapter_v0.py

from pathlib import Path

from .loaders.users_loader import load_users
from .loaders.boxbase_loader import load_boxbase
from .loaders.warmup_loader import load_warmup_table

from .design.test_design import TestDesign
from .design.psi_provider import PSIProvider

from .builders.subject_builder import build_subjects
from .builders.session_builder import build_sessions
from .builders.stimulus_builder import build_stimulus_events
from .builders.response_builder import build_response_events


class DataAdapterV0:
    def __init__(self, data_dir: Path):
        self.data_dir = data_dir

    def run(self):
        # --- load raw data ---
        users_df = load_users(self.data_dir / "users.xlsx")
        boxbase_df = load_boxbase(self.data_dir / "boxbase.xlsx")

        # --- build core entities ---
        subjects = build_subjects(users_df)
        sessions = build_sessions(boxbase_df)

        # --- load warmup tables (Excel) ---
        warmup_tables = load_warmup_table(
            self.data_dir / "stimulus_warmup.xlsx"
        )

        # --- load test metadata ---
        test_design = TestDesign(
            self.data_dir / "test_metadata_old.py"
        )

        # --- PSI provider ---
        psi_provider = PSIProvider(
            warmup_tables=warmup_tables,
            test_design=test_design
        )

        # --- stimuli & responses ---
        stimuli = build_stimulus_events(
            sessions=sessions,
            psi_provider=psi_provider,
            warmup_tables=warmup_tables
        )

        responses = build_response_events(boxbase_df, stimuli)

        return subjects, sessions, stimuli, responses


# FILE: src/neurotransanalytics/data_adapter/models/stimulus_event.py

class StimulusEvent:
    def __init__(
        self,
        stimulus_event_id,
        session_id,
        stimulus_role,
        stimulus_index_global,
        stimulus_index_in_phase,
        psi_pre_ms=None,
        psi_source=None,
        design_ref=None
    ):
        self.stimulus_event_id = stimulus_event_id
        self.session_id = session_id
        self.stimulus_role = stimulus_role
        self.stimulus_index_global = stimulus_index_global
        self.stimulus_index_in_phase = stimulus_index_in_phase
        self.psi_pre_ms = psi_pre_ms
        self.psi_source = psi_source
        self.design_ref = design_ref

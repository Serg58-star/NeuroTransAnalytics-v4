# FILE: src/neurotransanalytics/data_adapter/builders/stimulus_builder.py

from uuid import uuid4

from ..models.stimulus_event import StimulusEvent
from ..design.psi_provider import PSIProvider


def build_stimulus_events(sessions, warmup_design, test_design):
    """
    Сборка StimulusEvent для нормализованных TestSession.

    Для каждой сессии:
    - 3 warmup
    - 36 test
    """

    stimulus_events = []
    psi_provider = PSIProvider(warmup_design, test_design)

    for session in sessions.itertuples(index=False):
        session_id = session.session_id
        test_type = session.test_type

        global_index = 1

        # -------- WARMUP --------
        for i in range(1, 4):
            psi = psi_provider.get_warmup_psi(test_type, i)

            stimulus_events.append(
                StimulusEvent(
                    stimulus_event_id=str(uuid4()),
                    session_id=session_id,
                    stimulus_role="warmup",
                    stimulus_index_global=global_index,
                    stimulus_index_in_phase=i,
                    psi_pre_ms=psi,
                    psi_source="config",
                    design_ref="config_old.ini",
                )
            )
            global_index += 1

        # -------- TEST --------
        for i in range(1, 37):
            psi = psi_provider.get_test_psi(test_type, i)

            stimulus_events.append(
                StimulusEvent(
                    stimulus_event_id=str(uuid4()),
                    session_id=session_id,
                    stimulus_role="test",
                    stimulus_index_global=global_index,
                    stimulus_index_in_phase=i,
                    psi_pre_ms=psi,
                    psi_source="metadata",
                    design_ref="test_metadata_old.py",
                )
            )
            global_index += 1

    return stimulus_events

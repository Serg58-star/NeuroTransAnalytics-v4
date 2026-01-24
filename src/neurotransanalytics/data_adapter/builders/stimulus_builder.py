# FILE: src/neurotransanalytics/data_adapter/builders/stimulus_builder.py

from typing import List

from ..models.stimulus_event import StimulusEvent
from ..design.psi_provider import PSIProvider


def build_stimulus_events(
    sessions,
    warmup_design,
    test_design,
) -> List[StimulusEvent]:
    """
    Создание всех StimulusEvent (warmup + test).

    На этом этапе:
    - PSI полностью заполняется
    - Для Tst1 test-стимулов добавляется:
        * stimulus_color
        * stimulus_location
      из test_metadata_old.py
    """

    psi_provider = PSIProvider(
        warmup_design=warmup_design,
        test_design=test_design,
    )

    stimuli: List[StimulusEvent] = []
    stimulus_event_id = 1

    for session in sessions:
        test_type = session.test_type
        session_id = session.session_id

        # ------------------------------------------------------------
        # Warmup-стимулы (без изменений)
        # ------------------------------------------------------------
        warmup_variant = session.warmup_variant

        for order in (1, 2, 3):
            psi = psi_provider.get_warmup_psi(
                test_type=test_type,
                variant=warmup_variant,
                order=order,
            )

            stimulus = StimulusEvent(
                stimulus_event_id=stimulus_event_id,
                session_id=session_id,
                stimulus_role="warmup",
                stimulus_index=order,
                psi_pre_ms=psi,
                psi_source="config",
            )

            stimuli.append(stimulus)
            stimulus_event_id += 1

        # ------------------------------------------------------------
        # Test-стимулы
        # ------------------------------------------------------------
        for stimulus_index in range(1, 37):
            psi = psi_provider.get_test_psi(
                test_type=test_type,
                test_index=stimulus_index,
            )

            attrs = test_design.get_stimulus_attributes(
                test_type=test_type,
                stimulus_index=stimulus_index,
            )

            stimulus = StimulusEvent(
                stimulus_event_id=stimulus_event_id,
                session_id=session_id,
                stimulus_role="test",
                stimulus_index=stimulus_index,
                psi_pre_ms=psi,
                psi_source="metadata",
                stimulus_color=attrs.get("stimulus_color"),
                stimulus_location=attrs.get("stimulus_location"),
            )

            stimuli.append(stimulus)
            stimulus_event_id += 1

    return stimuli

# FILE: src/neurotransanalytics/data_adapter/builders/response_builder.py

from .rt_validation import validate_rt

from uuid import uuid4

from ..models.response_event import ResponseEvent


def build_response_events(sessions_df, stimulus_events):

    """
    Привязка ResponseEvent к test-StimulusEvent.

    Факты:
    - одна строка boxbase = одна сессия;
    - в строке: 3 × 36 RT (Tst1_*, Tst2_*, Tst3_*);
    - warmup-стимулы не имеют ResponseEvent;
    - порядок stimulus_events: warmup(3) → test(36) для каждой сессии.
    """

    response_events = []

    # сгруппируем стимулы по session_id
    stimuli_by_session = {}
    for stim in stimulus_events:
        stimuli_by_session.setdefault(stim.session_id, []).append(stim)

    for row_idx, row in sessions_df.iterrows():
        session_id = row["session_id"]

        session_stimuli = stimuli_by_session.get(session_id, [])
        if not session_stimuli:
            continue

        # оставляем только test-стимулы (36 штук)
        test_stimuli = [
            s for s in session_stimuli
            if s.stimulus_role == "test"
        ]

        # защита от рассинхронизации
        if len(test_stimuli) != 36:
            raise ValueError(
                f"Session {session_id}: expected 36 test stimuli, got {len(test_stimuli)}"
            )

        # --- ПЗР: Tst1_1 .. Tst1_36 ---
        for i in range(1, 37):
            rt = row[f"Tst1_{i}"]
            response_events.append(
                ResponseEvent(
                    response_event_id=str(uuid4()),
                    stimulus_event_id=test_stimuli[i - 1].stimulus_event_id,
                    rt_ms=rt,
                    validity_flag=validate_rt(rt)
                )
            )

        # --- Цвет: Tst2_1 .. Tst2_36 ---
        for i in range(1, 37):
            rt = row[f"Tst2_{i}"]
            response_events.append(
                ResponseEvent(
                    response_event_id=str(uuid4()),
                    stimulus_event_id=test_stimuli[i - 1].stimulus_event_id,
                    rt_ms=rt,
                    validity_flag=validate_rt(rt)
                )
            )

        # --- Сдвиг: Tst3_1 .. Tst3_36 ---
        for i in range(1, 37):
            rt = row[f"Tst3_{i}"]
            response_events.append(
                ResponseEvent(
                    response_event_id=str(uuid4()),
                    stimulus_event_id=test_stimuli[i - 1].stimulus_event_id,
                    rt_ms=rt,
                    validity_flag=validate_rt(rt)
                )
            )

    return response_events

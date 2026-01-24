# FILE: src/neurotransanalytics/analysis/rt_psi/rt_psi_dataset.py

import pandas as pd


def build_rt_psi_dataset_tst1(sessions, stimuli, responses):
    """
    Нормализованный DataFrame RT × PSI для теста Tst1.

    Гарантирует:
      - 1 RT ↔ 1 stimulus_index (1..36)
      - размерность: sessions × 36
    """

    # --- session_id -> test_type ---
    session_type = {s.session_id: s.test_type for s in sessions}

    # --- stimulus_event_id -> StimulusEvent ---
    stim_by_id = {s.stimulus_event_id: s for s in stimuli}

    # --- (session_id, stimulus_index) -> RT ---
    rt_map = {}

    for r in responses:
        if r.validity_flag != "OK":
            continue

        stim = stim_by_id.get(r.stimulus_event_id)
        if stim is None:
            continue

        # только тестовые стимулы
        if stim.stimulus_role != "test":
            continue

        # только Tst1
        if session_type.get(r.session_id) != "Tst1":
            continue

        key = (r.session_id, stim.stimulus_index)

        # защита от дублирования:
        # если RT уже зафиксирован — игнорируем последующие
        if key in rt_map:
            continue

        rt_map[key] = r.reaction_time_ms

    # --- сбор DataFrame ---
    rows = []

    for s in stimuli:
        if s.stimulus_role != "test":
            continue
        if session_type.get(s.session_id) != "Tst1":
            continue

        rt = rt_map.get((s.session_id, s.stimulus_index))
        if rt is None:
            continue

        rows.append(
            {
                "session_id": s.session_id,
                "stimulus_index": s.stimulus_index,
                "psi_ms": s.psi_pre_ms,
                "rt_ms": rt,
                "stimulus_color": getattr(s, "stimulus_color", None),
                "stimulus_location": getattr(s, "stimulus_location", None),
            }
        )

    return pd.DataFrame(rows)

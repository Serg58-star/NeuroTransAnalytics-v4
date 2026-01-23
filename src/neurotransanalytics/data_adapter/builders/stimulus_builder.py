# FILE: src/neurotransanalytics/data_adapter/builders/stimulus_builder.py

from ..models.stimulus_event import StimulusEvent


def build_stimulus_events(
    sessions,
    psi_provider,
    warmup_tables
):
    stimuli = []
    stimulus_id = 1

    # ВРЕМЕННО: фиксированный warmup-вариант
    warmup_variant = "NU0"

    for session in sessions:
        test_type = session.test_type

        # ---------- WARMUP ----------
        if test_type in warmup_tables:
            df = warmup_tables[test_type]

            for order in (1, 2, 3):
                psi = psi_provider.get_warmup_psi(
                    test_type=test_type,
                    variant=warmup_variant,
                    order=order
                )

                row = df[
                    (df["variant"] == warmup_variant) &
                    (df["order"] == order)
                ].iloc[0]

                stimuli.append(
                    StimulusEvent(
                        stimulus_event_id=stimulus_id,
                        session_id=session.session_id,

                        stimulus_role="warmup",
                        stimulus_index=order,

                        psi_pre_ms=psi,
                        psi_source="warmup_excel",

                        warmup_variant=warmup_variant,
                        warmup_order=order,

                        stimulus_color=row.get("test_color"),
                        stimulus_location=row.get("test_signal_position"),
                        test_triple=row.get("test_triple"),
                    )
                )
                stimulus_id += 1

        # ---------- TEST ----------
        for i in range(1, session.test_length + 1):
            psi = psi_provider.get_test_psi(test_type, i)

            stimuli.append(
                StimulusEvent(
                    stimulus_event_id=stimulus_id,
                    session_id=session.session_id,

                    stimulus_role="test",
                    stimulus_index=i,

                    psi_pre_ms=psi,
                    psi_source="metadata",
                )
            )
            stimulus_id += 1

    return stimuli

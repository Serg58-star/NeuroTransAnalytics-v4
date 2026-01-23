# FILE: src/neurotransanalytics/data_adapter/builders/response_builder.py

from ..models.response_event import ResponseEvent


def build_response_events(boxbase_df, stimuli):
    """
    Строит ResponseEvent из boxbase.xlsx.

    Инвариант:
    - идентификатор сессии = колонка 'cnt'
    """

    responses = []
    response_id = 1

    # индексируем стимулы для быстрого доступа
    stimulus_index = {
        (s.session_id, s.stimulus_index): s
        for s in stimuli
        if s.stimulus_role == "test"
    }

    for _, row in boxbase_df.iterrows():
        session_id = int(row["cnt"])

        # определяем тип теста по наличию данных
        for test_type, prefix in (
            ("Tst1", "Tst1_"),
            ("Tst2", "Tst2_"),
            ("Tst3", "Tst3_"),
        ):
            for i in range(1, 37):
                col = f"{prefix}{i}"
                if col not in row:
                    continue

                rt = row[col]

                # пропускаем пустые / невалидные
                if rt is None or rt == "":
                    continue

                stim_key = (session_id, i)
                stimulus = stimulus_index.get(stim_key)

                responses.append(
                    ResponseEvent(
                        response_event_id=response_id,
                        session_id=session_id,
                        stimulus_event_id=stimulus.stimulus_event_id if stimulus else None,
                        reaction_time_ms=float(rt),
                    )
                )
                response_id += 1

    return responses

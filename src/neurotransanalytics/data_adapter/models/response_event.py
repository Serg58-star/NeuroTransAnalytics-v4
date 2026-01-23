# FILE: src/neurotransanalytics/data_adapter/models/response_event.py

from dataclasses import dataclass
from typing import Optional


@dataclass
class ResponseEvent:
    response_event_id: int

    # идентификатор тестовой сессии (cnt)
    session_id: int

    # ссылка на стимул (может отсутствовать)
    stimulus_event_id: Optional[int]

    # время реакции в мс
    reaction_time_ms: float

    # флаг валидности RT (используется в main.py)
    validity_flag: Optional[str] = None

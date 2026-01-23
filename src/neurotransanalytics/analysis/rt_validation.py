# FILE: src/neurotransanalytics/analysis/rt_validation.py

from typing import Iterable
from ..data_adapter.models.response_event import ResponseEvent


class RTValidator:
    """
    Валидатор времени реакции (RT).

    Работает поверх готовых ResponseEvent.
    Ничего не загружает и не строит заново.
    """

    def __init__(
        self,
        min_rt_ms: float = 135.0,
        max_rt_ms: float = 3000.0,
    ):
        self.min_rt_ms = min_rt_ms
        self.max_rt_ms = max_rt_ms

    def validate(self, responses: Iterable[ResponseEvent]) -> None:
        """
        Заполняет поле ResponseEvent.validity_flag inplace.
        """
        for r in responses:
            rt = r.reaction_time_ms

            if rt is None:
                r.validity_flag = "INVALID"
                continue

            try:
                rt_val = float(rt)
            except (TypeError, ValueError):
                r.validity_flag = "INVALID"
                continue

            if rt_val < 0:
                r.validity_flag = "INVALID"
            elif rt_val < self.min_rt_ms:
                r.validity_flag = "TOO_FAST"
            elif rt_val > self.max_rt_ms:
                r.validity_flag = "TOO_SLOW"
            else:
                r.validity_flag = "OK"

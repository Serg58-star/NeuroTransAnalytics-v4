# FILE: src/neurotransanalytics/data_adapter/builders/rt_validation.py

import math


def validate_rt(rt_ms):
    """
    Проверка корректности времени реакции (RT).

    Возвращает строковый validity_flag:
    - MISSING
    - NON_POSITIVE
    - TOO_FAST
    - TOO_SLOW
    - OK
    """

    if rt_ms is None:
        return "MISSING"

    try:
        rt = float(rt_ms)
    except (TypeError, ValueError):
        return "MISSING"

    if math.isnan(rt):
        return "MISSING"

    if rt <= 0:
        return "NON_POSITIVE"

    if rt < 100:
        return "TOO_FAST"

    if rt > 3000:
        return "TOO_SLOW"

    return "OK"

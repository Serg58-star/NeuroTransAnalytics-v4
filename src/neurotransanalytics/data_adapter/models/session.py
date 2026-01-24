# FILE: src/neurotransanalytics/data_adapter/models/session.py

from dataclasses import dataclass


@dataclass
class Session:
    """
    Каноническая модель тестовой сессии (v4).

    Инварианты:
    - session_id: идентификатор сессии (cnt из boxbase.xlsx)
    - test_type: 'Tst1' | 'Tst2' | 'Tst3'
    - warmup_variant: индекс варианта warmup (0–9), фиксированный,
      так как реальный выбор не сохранялся
    """

    session_id: int
    test_type: str
    warmup_variant: int

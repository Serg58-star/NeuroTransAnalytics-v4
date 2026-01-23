# FILE: src/neurotransanalytics/data_adapter/models/stimulus_event.py

from dataclasses import dataclass
from typing import Optional


@dataclass
class StimulusEvent:
    stimulus_event_id: int
    session_id: int

    stimulus_role: str          # "warmup" | "test"
    stimulus_index: int         # порядок в своей фазе

    stimulus_color: Optional[str] = None
    stimulus_location: Optional[str] = None

    psi_pre_ms: Optional[int] = None
    psi_source: Optional[str] = None   # "warmup_excel" | "metadata"

    # ---- warmup-only контекст ----
    warmup_variant: Optional[str] = None   # NU0 … NU9
    warmup_order: Optional[int] = None     # 1 / 2 / 3
    test_triple: Optional[str] = None

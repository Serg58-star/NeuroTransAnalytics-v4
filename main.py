# FILE: main.py

from pathlib import Path
from collections import Counter

from src.neurotransanalytics.data_adapter.adapter_v0 import DataAdapterV0
from src.neurotransanalytics.analysis.rt_validation import RTValidator
from src.neurotransanalytics.analysis.rt_psi.rt_psi_dataset import (
    build_rt_psi_dataset_tst1,
)
from src.neurotransanalytics.analysis.rt_psi.rt_psi_checks import (
    check_tst1_rt_psi,
)


def main() -> None:
    # --- paths ---
    data_dir = Path("data")

    # --- data adapter ---
    adapter = DataAdapterV0(data_dir=data_dir)
    subjects, sessions, stimuli, responses = adapter.run()

    # --- RT validation (analysis layer) ---
    validator = RTValidator(
        min_rt_ms=135,
        max_rt_ms=3000,
    )
    validator.validate(responses)

    # --- RT validity summary (control output) ---
    flags = Counter(r.validity_flag for r in responses)
    print("RT validity summary:", flags)

    # --- basic dataset stats (control output) ---
    print(f"Subjects: {len(subjects)}")
    print(f"Sessions: {len(sessions)}")
    print(f"Stimuli: {len(stimuli)}")
    print(f"Responses: {len(responses)}")
    print("PSI missing:", sum(1 for s in stimuli if s.psi_pre_ms is None))

    # --- RT × PSI analysis: Tst1 (analysis layer) ---
    df_tst1 = build_rt_psi_dataset_tst1(sessions, stimuli, responses)
    check_tst1_rt_psi(df_tst1)


if __name__ == "__main__":
    main()

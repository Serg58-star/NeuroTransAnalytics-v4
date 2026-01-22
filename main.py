# FILE: main.py

from pathlib import Path

from src.neurotransanalytics.data_adapter.adapter_v0 import DataAdapterV0


def main():
    data_dir = Path("data")

    adapter = DataAdapterV0(data_dir=data_dir)
    subjects, sessions, stimuli, responses = adapter.run()
    from collections import Counter

    flags = Counter(r.validity_flag for r in responses)
    print("RT validity summary:", flags)

    print(f"Subjects: {len(subjects)}")
    print(f"Sessions: {len(sessions)}")
    print(f"Stimuli: {len(stimuli)}")
    print(f"Responses: {len(responses)}")
    print("PSI missing:", sum(1 for s in stimuli if s.psi_pre_ms is None))


if __name__ == "__main__":
    main()

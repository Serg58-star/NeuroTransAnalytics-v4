# FILE: analysis/rt_psi/rt_psi_checks.py

def check_tst1_rt_psi(df):
    print("Tst1 RT × PSI dataset")
    print("--------------------")
    print("Rows:", len(df))
    print("Sessions:", df["session_id"].nunique())
    print("Stimulus indices:", sorted(df["stimulus_index"].unique()))
    print("Unique PSI values:", sorted(df["psi_ms"].unique()))
    print()
    print("Head:")
    print(df.head(10))

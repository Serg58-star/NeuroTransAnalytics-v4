import os

sql_str = "DROP VIEW IF EXISTS reactions_view;\nCREATE VIEW reactions_view AS\nWITH\n"

configurations = [
    ("tst1", "metadata_simple", "simple"),
    ("tst2", "metadata_shift", "shift"),
    ("tst3", "metadata_color_red", "color")
]

for tst, meta, name in configurations:
    selects = []
    for i in range(1, 37):
        selects.append(f"SELECT trial_id, subject_id, {i} AS stimulus_index, {tst}_{i} AS rt, '{name}' AS test_type FROM trials")
    
    sql_str += f"unpivoted_{tst} AS (\n    " + " UNION ALL\n    ".join(selects) + "\n),\n"
    sql_str += f"reactions_{tst} AS (\n    SELECT u.trial_id, u.subject_id, u.test_type, u.stimulus_index, u.rt, m.position AS field, m.psi_ms AS psi, m.color \n    FROM unpivoted_{tst} u \n    JOIN {meta} m ON u.stimulus_index = m.stimulus_id \n    WHERE u.rt IS NOT NULL AND u.rt > 0\n)"
    
    if name != "color":
        sql_str += ",\n"
    else:
        sql_str += "\n"

sql_str += "SELECT * FROM reactions_tst1 UNION ALL SELECT * FROM reactions_tst2 UNION ALL SELECT * FROM reactions_tst3;\n"

os.makedirs("sql", exist_ok=True)
with open("sql/boxbase_reactions_view.sql", "w", encoding="utf-8") as f:
    f.write(sql_str)
print("Generated sql/boxbase_reactions_view.sql")

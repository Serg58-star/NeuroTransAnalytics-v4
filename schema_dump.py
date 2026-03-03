import sqlite3

def dump_schema():
    conn = sqlite3.connect('neuro_data.db')
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in c.fetchall()]
    
    with open('schema_audit.txt', 'w') as f:
        for t in tables:
            f.write(f"=== {t} ===\n")
            c.execute(f"PRAGMA table_info({t})")
            columns = c.fetchall()
            for col in columns:
                f.write(str(col) + "\n")
            f.write("\n")

if __name__ == "__main__":
    dump_schema()

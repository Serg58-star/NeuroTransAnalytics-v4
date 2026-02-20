import sqlite3
conn = sqlite3.connect('C:/NeuroTransAnalytics-v4/neuro_data.db')
cursor = conn.cursor()
cursor.execute("SELECT name, sql FROM sqlite_master WHERE type='table' AND name LIKE 'metadata_%'")
for row in cursor.fetchall():
    print(f"--- Table: {row[0]} ---")
    print(row[1])

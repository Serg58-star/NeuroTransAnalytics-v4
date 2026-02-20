import sqlite3
import pandas as pd
conn = sqlite3.connect('C:/NeuroTransAnalytics-v4/neuro_data.db')
print("Unique PSI:", pd.read_sql_query("SELECT distinct psi_ms FROM metadata_simple", conn)['psi_ms'].tolist())
print("Unique Shift:", pd.read_sql_query("SELECT distinct shift_parameter FROM metadata_shift", conn)['shift_parameter'].tolist())
print("Unique Mask Tst2:", pd.read_sql_query("SELECT distinct mask_triples FROM metadata_color_red", conn)['mask_triples'].tolist()[:5])
print("Unique Mask Tst3:", pd.read_sql_query("SELECT distinct mask_triples FROM metadata_shift", conn)['mask_triples'].tolist()[:5])

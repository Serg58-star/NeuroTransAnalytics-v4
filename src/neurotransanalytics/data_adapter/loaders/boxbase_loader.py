# FILE: src/neurotransanalytics/data_adapter/loaders/boxbase_loader.py

import pandas as pd


def load_boxbase(path):
    """Загрузка boxbase.xlsx"""
    return pd.read_excel(path)

# FILE: src/neurotransanalytics/data_adapter/loaders/users_loader.py

import pandas as pd


def load_users(path):
    """Загрузка users.xlsx"""
    return pd.read_excel(path)

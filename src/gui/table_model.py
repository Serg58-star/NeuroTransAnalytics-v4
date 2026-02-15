"""
gui.table_model

Generic PySide6 table model for pandas DataFrames.
"""

import pandas as pd
from PySide6.QtCore import QAbstractTableModel, Qt, QModelIndex

class ScenarioTableModel(QAbstractTableModel):
    """
    Generic table model for displaying pandas DataFrames in QTableView.
    """
    def __init__(self, data: pd.DataFrame):
        super().__init__()
        self._data = data

    def rowCount(self, parent=QModelIndex()):
        return self._data.shape[0]

    def columnCount(self, parent=QModelIndex()):
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                value = self._data.iloc[index.row(), index.column()]
                if pd.isna(value):
                    return ""
                if isinstance(value, float):
                    return f"{value:.2f}"
                return str(value)
        return None

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._data.columns[section])
            if orientation == Qt.Vertical:
                return str(self._data.index[section])
        return None

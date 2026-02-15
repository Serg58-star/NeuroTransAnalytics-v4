"""
gui.widgets.parameter_panels

This module implements dynamic parameter panels for different exploratory procedures.
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QComboBox, 
    QDoubleSpinBox, QSpinBox, QCheckBox, QLabel
)
from PySide6.QtCore import Signal


class ParameterPanel(QWidget):
    """Base class for parameter panels."""
    parametersChanged = Signal(dict)

    def get_parameters(self) -> dict:
        raise NotImplementedError


class MultimodalityParams(ParameterPanel):
    """Parameter panel for Multimodality Detection."""
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QFormLayout(self)

        self.bandwidth = QComboBox()
        self.bandwidth.addItems(["scott", "silverman"])
        layout.addRow("Bandwidth:", self.bandwidth)

        self.prominence = QDoubleSpinBox()
        self.prominence.setRange(0.01, 0.5)
        self.prominence.setSingleStep(0.01)
        self.prominence.setValue(0.05)
        layout.addRow("Prominence Ratio:", self.prominence)

        self.n_grid = QSpinBox()
        self.n_grid.setRange(50, 500)
        self.n_grid.setValue(100)
        layout.addRow("N Grid:", self.n_grid)

        # Scientific/Data Generation Params (Implicitly required for Synthetic First)
        self.n_samples = QSpinBox()
        self.n_samples.setRange(100, 2000)
        self.n_samples.setValue(500)
        layout.addRow("N Samples:", self.n_samples)

        self.modes = QSpinBox()
        self.modes.setRange(1, 3)
        self.modes.setValue(2)
        layout.addRow("Modes:", self.modes)

    def get_parameters(self) -> dict:
        return {
            "bandwidth": self.bandwidth.currentText(),
            "prominence_ratio": self.prominence.value(),
            "n_grid": self.n_grid.value(),
            "n_samples": self.n_samples.value(),
            "modes": self.modes.value()
        }


class ChangePointParams(ParameterPanel):
    """Parameter panel for Change-Point Detection."""
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QFormLayout(self)

        self.window_size = QSpinBox()
        self.window_size.setRange(5, 200)
        self.window_size.setValue(10)
        layout.addRow("Window Size:", self.window_size)

        self.threshold = QDoubleSpinBox()
        self.threshold.setRange(0.01, 5.0)
        self.threshold.setValue(1.0)
        layout.addRow("Threshold:", self.threshold)

        self.normalize = QCheckBox()
        layout.addRow("Normalize:", self.normalize)

        self.search_radius = QSpinBox()
        self.search_radius.setRange(1, 100)
        self.search_radius.setValue(5)
        layout.addRow("Search Radius:", self.search_radius)

        # Data Generation Params
        self.n_samples = QSpinBox()
        self.n_samples.setRange(50, 1000)
        self.n_samples.setValue(200)
        layout.addRow("N Samples:", self.n_samples)

        self.shifts = QSpinBox()
        self.shifts.setRange(1, 5)
        self.shifts.setValue(1)
        layout.addRow("Shifts:", self.shifts)

    def get_parameters(self) -> dict:
        return {
            "window_size": self.window_size.value(),
            "threshold": self.threshold.value(),
            "normalize": self.normalize.isChecked(),
            "search_radius": self.search_radius.value(),
            "n_samples": self.n_samples.value(),
            "shifts": self.shifts.value()
        }

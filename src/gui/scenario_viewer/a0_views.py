"""
gui.scenario_viewer.a0_views

Specific views for A0 scenarios.
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QTableView, QLabel, QHeaderView, QFrame
)
from PySide6.QtCore import Qt
from src.gui.table_model import ScenarioTableModel
from src.gui.scenario_viewer.scenario_viewer import ScenarioLoader
import datetime

class BaseScenarioView(QWidget):
    """Base class for scenario views with metadata footer."""
    def __init__(self, scenario_id: str, title: str):
        super().__init__()
        self.scenario_id = scenario_id
        self.loader = ScenarioLoader()
        
        layout = QVBoxLayout(self)
        
        # Title
        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(title_label)
        
        # Table
        self.table_view = QTableView()
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_view.setAlternatingRowColors(True)
        layout.addWidget(self.table_view)
        
        # Footer
        footer = QFrame()
        footer.setObjectName("footer")
        footer_layout = QVBoxLayout(footer)
        
        disclaimer = QLabel("Exploratory representation. No interpretation.")
        disclaimer.setStyleSheet("color: #666; font-style: italic; font-size: 11px;")
        disclaimer.setAlignment(Qt.AlignCenter)
        footer_layout.addWidget(disclaimer)
        
        self.meta_label = QLabel(f"Version: scenario_v4.0.0 | Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}")
        self.meta_label.setStyleSheet("color: #888; font-size: 10px;")
        self.meta_label.setAlignment(Qt.AlignCenter)
        footer_layout.addWidget(self.meta_label)
        
        layout.addWidget(footer)
        
    def refresh(self):
        df = self.loader.load_scenario(self.scenario_id)
        if df is not None:
            print(f"Refreshing {self.scenario_id}: Loaded {len(df)} rows.")
            model = ScenarioTableModel(df)
            self.table_view.setModel(model)
        else:
            print(f"Refreshing {self.scenario_id}: Failed to load data.")
            self.table_view.setModel(None)

class A0BaselineView(BaseScenarioView):
    def __init__(self):
        super().__init__("A0.0", "Scenario A0.0: ΔV1 Baseline Stability")

class A0VariabilityView(BaseScenarioView):
    def __init__(self):
        super().__init__("A0.1", "Scenario A0.1: ΔV1 Variability Profile")

"""
gui.scenario_viewer.a0_views

Specific views for A0 scenarios.
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QTableView, QLabel, QHeaderView, QFrame, QSplitter
)
from PySide6.QtCore import Qt
from src.gui.table_model import ScenarioTableModel
from src.gui.scenario_viewer.scenario_viewer import ScenarioLoader
from src.gui.widgets.matplotlib_canvas import MplCanvas
from src.c3_core.pipeline_config import PIPELINE_VERSIONS
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
        
        version_str = PIPELINE_VERSIONS.get('scenario_version', 'v4.0.0')
        self.meta_label = QLabel(f"Version: {version_str} | Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}")
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

class A0PopulationView(QWidget):
    """
    A0.2 — Population Structures of ΔV1.
    Features a table and population-level visualizations.
    """
    def __init__(self):
        super().__init__()
        self.scenario_id = "A0.2"
        self.loader = ScenarioLoader()
        
        layout = QVBoxLayout(self)
        
        # Title
        title_label = QLabel("Scenario A0.2: Population Structures of ΔV1")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(title_label)
        
        # Main Splitter
        splitter = QSplitter(Qt.Vertical)
        
        # 1. Table
        self.table_view = QTableView()
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_view.setAlternatingRowColors(True)
        splitter.addWidget(self.table_view)
        
        # 2. Visualizations
        self.canvas = MplCanvas(self)
        splitter.addWidget(self.canvas)
        
        layout.addWidget(splitter)
        
        # Footer
        footer = QFrame()
        footer.setObjectName("footer")
        footer_layout = QVBoxLayout(footer)
        
        disclaimer = QLabel("Exploratory representation. No interpretation.")
        disclaimer.setStyleSheet("color: #666; font-style: italic; font-size: 11px;")
        disclaimer.setAlignment(Qt.AlignCenter)
        footer_layout.addWidget(disclaimer)
        
        version_str = PIPELINE_VERSIONS.get('scenario_version', 'v4.0.0')
        self.meta_label = QLabel(f"Version: {version_str} | Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}")
        self.meta_label.setStyleSheet("color: #888; font-size: 10px;")
        self.meta_label.setAlignment(Qt.AlignCenter)
        footer_layout.addWidget(self.meta_label)
        
        layout.addWidget(footer)
        
    def refresh(self):
        df = self.loader.load_scenario(self.scenario_id)
        if df is not None:
            print(f"Refreshing {self.scenario_id}: Loaded {len(df)} subjects.")
            model = ScenarioTableModel(df)
            self.table_view.setModel(model)
            self.canvas.render_population_structure(df)
        else:
            print(f"Refreshing {self.scenario_id}: Failed to load data.")
            self.table_view.setModel(None)
            self.canvas.clear()
            self.canvas.draw()

class A0SymmetryView(QWidget):
    """
    A0.3 — Architectural Symmetry (ΔV1).
    Features a table and spatial symmetry visualizations.
    """
    def __init__(self):
        super().__init__()
        self.scenario_id = "A0.3"
        self.loader = ScenarioLoader()
        
        layout = QVBoxLayout(self)
        
        # Title
        title_label = QLabel("Scenario A0.3: Architectural Symmetry (ΔV1)")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(title_label)
        
        # Main Splitter
        splitter = QSplitter(Qt.Vertical)
        
        # 1. Table
        self.table_view = QTableView()
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_view.setAlternatingRowColors(True)
        splitter.addWidget(self.table_view)
        
        # 2. Visualizations
        self.canvas = MplCanvas(self)
        splitter.addWidget(self.canvas)
        
        layout.addWidget(splitter)
        
        # Footer
        footer = QFrame()
        footer.setObjectName("footer")
        footer_layout = QVBoxLayout(footer)
        
        disclaimer = QLabel("Exploratory representation. No interpretation.")
        disclaimer.setStyleSheet("color: #666; font-style: italic; font-size: 11px;")
        disclaimer.setAlignment(Qt.AlignCenter)
        footer_layout.addWidget(disclaimer)
        
        from src.c3_core.pipeline_config import PIPELINE_VERSIONS
        version_str = PIPELINE_VERSIONS.get('scenario_version', 'v4.0.0')
        self.meta_label = QLabel(f"Version: {version_str} | Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}")
        self.meta_label.setStyleSheet("color: #888; font-size: 10px;")
        self.meta_label.setAlignment(Qt.AlignCenter)
        footer_layout.addWidget(self.meta_label)
        
        layout.addWidget(footer)
        
    def refresh(self):
        df = self.loader.load_scenario(self.scenario_id)
        if df is not None:
            print(f"Refreshing {self.scenario_id}: Loaded {len(df)} subjects.")
            model = ScenarioTableModel(df)
            self.table_view.setModel(model)
            self.canvas.render_symmetry_structure(df)
        else:
            print(f"Refreshing {self.scenario_id}: Failed to load data.")
            self.table_view.setModel(None)
            self.canvas.clear()
            self.canvas.draw()

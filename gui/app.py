"""
gui.app

The main entry point for the NeuroTransAnalytics-v4 PySide6 Desktop Application.
Implements the MainWindow with a sidebar navigation system.
"""

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QListWidget, QStackedWidget, QLabel, QFrame
)
from gui.screens.exploratory_results import ExploratoryResultsScreen
from gui.scenario_viewer.a0_views import A0BaselineView, A0VariabilityView


class MainWindow(QMainWindow):
    """
    Main Application Window.
    Provides a persistent sidebar for navigation and a central stack for screens.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NeuroTransAnalytics v4")
        self.resize(1100, 750)

        # Main horizontal layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.main_layout = QHBoxLayout(central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # 1. Sidebar
        self.sidebar = QFrame()
        self.sidebar.setFixedWidth(240)
        self.sidebar.setObjectName("sidebar")
        sidebar_layout = QVBoxLayout(self.sidebar)
        
        title_label = QLabel("NeuroTrans v4")
        title_label.setObjectName("app_title")
        sidebar_layout.addWidget(title_label)

        self.nav_list = QListWidget()
        self.nav_list.addItem("Exploratory Results")
        self.nav_list.addItem("Scenario: A0 Baseline")
        self.nav_list.addItem("Scenario: A0 Variability")
        
        sidebar_layout.addWidget(self.nav_list)
        sidebar_layout.addStretch()
        
        self.main_layout.addWidget(self.sidebar)

        # 2. Main Stacked Area
        self.content_stack = QStackedWidget()
        
        # Initialize Screens
        self.exploratory_screen = ExploratoryResultsScreen()
        self.a0_baseline_view = A0BaselineView()
        self.a0_variability_view = A0VariabilityView()
        
        self.content_stack.addWidget(self.exploratory_screen)
        self.content_stack.addWidget(self.a0_baseline_view)
        self.content_stack.addWidget(self.a0_variability_view)
        
        self.main_layout.addWidget(self.content_stack)

        # Connect signals
        self.nav_list.currentRowChanged.connect(self.display_screen)

        # Load QSS
        self.apply_style()

    def display_screen(self, index: int):
        self.content_stack.setCurrentIndex(index)
        # Refresh view if it's a scenario view
        current_widget = self.content_stack.currentWidget()
        if hasattr(current_widget, 'refresh'):
            current_widget.refresh()

    def apply_style(self):
        try:
            with open("gui/style.css", "r", encoding="utf-8") as f:
                self.setStyleSheet(f.read())
        except FileNotFoundError:
            pass


def run_app():
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

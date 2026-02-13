"""
gui.screens.exploratory_results

This module implements the Exploratory Results screen in PySide6.
It provide a read-only interface for browsing and viewing C3.x artifacts.
"""

import os
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QListWidget, 
    QLabel, QTextEdit, QScrollArea, QFrame, QSplitter
)
from PySide6.QtCore import Qt

from src.c3x_exploratory.persistence import load_artifact, ARTIFACT_ROOT
from src.shared.artifacts import DistributionStructureResult, TemporalStructureResult


class ExploratoryResultsController:
    """
    Controller for the Exploratory Results screen.
    Now supports listing all available procedures.
    """

    def __init__(self, root_dir: str = ARTIFACT_ROOT):
        self.root_dir = root_dir
        # Explicit supported procedures
        self.supported_procedures = [
            "MultimodalityDetection",
            "ChangePointDetection"
        ]

    def list_procedures(self) -> list[str]:
        """Lists all supported procedures."""
        return self.supported_procedures

    def list_artifacts(self, procedure_name: str) -> list[str]:
        """Lists available JSON artifacts for a specific procedure, newest first."""
        proc_path = os.path.join(self.root_dir, procedure_name)
        if not os.path.exists(proc_path):
            return []
        files = [f for f in os.listdir(proc_path) if f.endswith(".json")]
        return sorted(files, reverse=True)

    def load_result(self, procedure_name: str, filename: str) -> object:
        """Loads a specific artifact via the persistence layer."""
        path = os.path.join(self.root_dir, procedure_name, filename)
        try:
            return load_artifact(path)
        except Exception as e:
            # QMessageBox handled at screen level if needed, but keeping passive
            return None


from gui.widgets.exploratory_widget import ExploratoryWidget


class ExploratoryResultsScreen(QWidget):
    """
    Interactive PySide6 Screen for exploratory research.
    Bridges selection with execution and visualization.
    """
    def __init__(self):
        super().__init__()
        self.controller = ExploratoryResultsController()
        self.setup_ui()
        self.refresh_procedures()

    def setup_ui(self):
        layout = QHBoxLayout(self)

        # 1. Left Selection Column
        selector_widget = QWidget()
        selector_widget.setFixedWidth(300)
        selector_layout = QVBoxLayout(selector_widget)
        
        selector_layout.addWidget(QLabel("1. Select Procedure:"))
        self.proc_combo = QComboBox()
        self.proc_combo.currentTextChanged.connect(self.on_procedure_changed)
        selector_layout.addWidget(self.proc_combo)

        selector_layout.addWidget(QLabel("2. Select Artifact:"))
        self.art_list = QListWidget()
        self.art_list.currentTextChanged.connect(self.on_artifact_selected)
        selector_layout.addWidget(self.art_list)
        
        layout.addWidget(selector_widget)

        # 2. Right Content Column
        self.exploratory_widget = ExploratoryWidget(self)
        self.exploratory_widget.artifactRequested.connect(self.on_new_artifact_created)
        layout.addWidget(self.exploratory_widget)

    def refresh_procedures(self):
        self.proc_combo.clear()
        procs = self.controller.list_procedures()
        self.proc_combo.addItems(procs)

    def on_procedure_changed(self, procedure_name: str):
        """Update both artifact list and parameter panel."""
        self.refresh_artifacts(procedure_name)
        self.exploratory_widget.set_procedure(procedure_name)

    def refresh_artifacts(self, procedure_name: str):
        self.art_list.clear()
        if not procedure_name:
            return
        artifacts = self.controller.list_artifacts(procedure_name)
        self.art_list.addItems(artifacts)

    def on_artifact_selected(self, filename: str):
        if not filename:
            self.exploratory_widget.clear_ui()
            return
        
        proc_name = self.proc_combo.currentText()
        artifact = self.controller.load_result(proc_name, filename)
        self.exploratory_widget.display_artifact(artifact)

    def on_new_artifact_created(self):
        """Called when Run finishes to refresh the UI."""
        proc_name = self.proc_combo.currentText()
        self.refresh_artifacts(proc_name)
        
        # Newest artifact is first in sorted list
        if self.art_list.count() > 0:
            self.art_list.setCurrentRow(0)

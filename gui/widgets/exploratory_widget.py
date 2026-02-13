"""
gui.widgets.exploratory_widget

Dedicated widget for rendering C3.x exploratory results.
Handles visualization dispatch and provenance display.
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit, QFrame, QMessageBox
from PySide6.QtCore import Qt

from gui.widgets.matplotlib_canvas import MplCanvas
from gui.adapters.exploratory_adapters import get_distribution_plot_data, get_temporal_plot_data
from src.shared.artifacts import DistributionStructureResult, TemporalStructureResult


class ExploratoryWidget(QWidget):
    """
    Handles the central visualization and metadata display for exploratory artifacts.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        # 1. Visualization Panel (Matplotlib Canvas)
        self.canvas = MplCanvas(self)
        layout.addWidget(self.canvas)

        # 2. Metadata Panel
        self.metadata_area = QTextEdit()
        self.metadata_area.setReadOnly(True)
        self.metadata_area.setPlaceholderText("Artifact metadata...")
        self.metadata_area.setMaximumHeight(150)
        layout.addWidget(self.metadata_area)

        # 3. Mandatory Non-Interpretation Clause
        self.clause_box = QLabel("No artifact selected.")
        self.clause_box.setWordWrap(True)
        self.clause_box.setObjectName("clause_box")
        # Style matches existing style.css
        layout.addWidget(self.clause_box)

    def display_artifact(self, artifact):
        """
        Updates the UI with artifact data.
        """
        if not artifact:
            self.clear_ui()
            return

        # Provenance Update
        meta_text = (
            f"Procedure: {artifact.procedure_name}\n"
            f"Version: {artifact.procedure_version}\n"
            f"Timestamp: {artifact.timestamp}\n"
            f"Input Parameters: {artifact.input_parameters}\n"
        )
        self.metadata_area.setText(meta_text)
        self.clause_box.setText(artifact.non_interpretation_clause)

        # Visualization Update
        try:
            if isinstance(artifact, DistributionStructureResult):
                data = get_distribution_plot_data(artifact)
                self.canvas.render_multimodality(data)
                
            elif isinstance(artifact, TemporalStructureResult):
                data = get_temporal_plot_data(artifact)
                self.canvas.render_change_point(data)
            else:
                self.canvas.clear()
                self.canvas.draw()
        except Exception as e:
            QMessageBox.critical(self, "Rendering Error", f"Failed to render artifact: {e}")

    def clear_ui(self):
        self.metadata_area.clear()
        self.clause_box.setText("No artifact selected.")
        self.canvas.clear()
        self.canvas.draw()

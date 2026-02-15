"""
gui.widgets.exploratory_widget

Dedicated widget for rendering C3.x exploratory results.
Handles visualization dispatch, parameter configuration, and provenance display.
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, 
    QFrame, QMessageBox, QPushButton, QSplitter, QGroupBox
)
from PySide6.QtCore import Qt, Signal

from src.gui.widgets.matplotlib_canvas import MplCanvas
from src.gui.widgets.parameter_panels import MultimodalityParams, ChangePointParams
from src.gui.adapters.exploratory_adapters import get_distribution_plot_data, get_temporal_plot_data
from src.shared.artifacts import DistributionStructureResult, TemporalStructureResult
from src.c35_visualization.exploratory_controller import ExploratoryController


class ExploratoryWidget(QWidget):
    """
    Handles the central visualization, parameter configuration, 
    and metadata display for exploratory procedures.
    """
    artifactRequested = Signal()  # Emitted when a new artifact is created

    def __init__(self, parent=None):
        super().__init__(parent)
        self.controller = ExploratoryController()
        self.current_procedure = None
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        # 1. Parameter & Action Header
        self.param_group = QFrame()
        self.param_group.setObjectName("param_group")
        param_layout = QHBoxLayout(self.param_group)
        
        self.param_stack = QWidget()
        self.param_stack_layout = QVBoxLayout(self.param_stack)
        self.param_stack_layout.setContentsMargins(0, 0, 0, 0)
        param_layout.addWidget(self.param_stack)

        self.run_button_panel = QWidget()
        run_vbox = QVBoxLayout(self.run_button_panel)
        self.btn_run = QPushButton("Run Procedure")
        self.btn_run.setFixedWidth(150)
        self.btn_run.clicked.connect(self.run_procedure)
        run_vbox.addWidget(self.btn_run)
        param_layout.addWidget(self.run_button_panel)
        
        layout.addWidget(self.param_group)

        # 2. Visualization Panel (Matplotlib Canvas)
        self.canvas = MplCanvas(self)
        layout.addWidget(self.canvas)

        # 3. Metadata & Info Bottom Area
        bottom_splitter = QSplitter(Qt.Horizontal)
        
        self.metadata_area = QTextEdit()
        self.metadata_area.setReadOnly(True)
        self.metadata_area.setPlaceholderText("Artifact metadata...")
        self.metadata_area.setMaximumHeight(200)
        bottom_splitter.addWidget(self.metadata_area)

        # 4. Refactored Non-Interpretation Block
        self.info_group = QGroupBox("Methodological Boundary")
        info_layout = QVBoxLayout(self.info_group)
        self.clause_box = QLabel(
            "This procedure identifies structural features of the data.\n"
            "It does not perform interpretation or diagnosis."
        )
        self.clause_box.setWordWrap(True)
        self.clause_box.setStyleSheet("font-size: 11px; color: #666;")
        info_layout.addWidget(self.clause_box)
        bottom_splitter.addWidget(self.info_group)
        
        layout.addWidget(bottom_splitter)

    def set_procedure(self, proc_name: str):
        """Switches the parameter panel based on the selected procedure."""
        self.current_procedure = proc_name
        
        # Clear existing
        for i in reversed(range(self.param_stack_layout.count())): 
            widget = self.param_stack_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        if proc_name == "MultimodalityDetection":
            self.active_params = MultimodalityParams()
        elif proc_name == "ChangePointDetection":
            self.active_params = ChangePointParams()
        else:
            self.active_params = QLabel("Select a procedure to configure parameters.")
            self.btn_run.setEnabled(False)
            self.param_stack_layout.addWidget(self.active_params)
            return

        self.param_stack_layout.addWidget(self.active_params)
        self.btn_run.setEnabled(True)

    def run_procedure(self):
        """Triggers execution via controller."""
        if not self.current_procedure:
            return

        params = self.active_params.get_parameters()
        self.btn_run.setEnabled(False)
        self.btn_run.setText("Computing...")
        
        try:
            if self.current_procedure == "MultimodalityDetection":
                self.controller.run_multimodality(params)
            else:
                self.controller.run_change_point(params)
            
            # Notify screen to refresh list
            self.artifactRequested.emit()
            
        except Exception as e:
            QMessageBox.critical(self, "Execution Error", f"Operation failed: {e}")
        finally:
            self.btn_run.setEnabled(True)
            self.btn_run.setText("Run Procedure")

    def display_artifact(self, artifact):
        """Updates the UI with artifact data."""
        if not artifact:
            self.clear_ui()
            return

        meta_text = (
            f"Procedure: {artifact.procedure_name}\n"
            f"Version: {artifact.procedure_version}\n"
            f"Timestamp: {artifact.timestamp}\n"
            f"Input Parameters: {artifact.input_parameters}\n"
        )
        self.metadata_area.setText(meta_text)

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
            QMessageBox.critical(self, "Rendering Error", f"Failed to render: {e}")

    def clear_ui(self):
        self.metadata_area.clear()
        self.canvas.clear()
        self.canvas.draw()

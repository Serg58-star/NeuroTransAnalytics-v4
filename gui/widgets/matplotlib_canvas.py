"""
gui.widgets.matplotlib_canvas

Implements a PySide6-compatible Matplotlib canvas for rendering 
exploratory results without interpretation.
"""

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure


class MplCanvas(FigureCanvasQTAgg):
    """
    A reusable Matplotlib canvas integrated into the PySide6 UI.
    Follows strictly read-only and zero-computation constraints.
    """

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        super().__init__(self.fig)
        self.setParent(parent)

    def clear(self):
        """Clears the axes for a new plot."""
        self.axes.clear()

    def render_multimodality(self, data: dict):
        """
        Renders Multimodality Detection results (Task 8/13).
        Expects: x_values, density_values, peak_positions.
        """
        self.clear()
        
        # Plot density curve
        self.axes.plot(data["x_values"], data["density_values"], 
                       label="Density", color="#1f77b4", linewidth=2)
        
        # Plot vertical lines for peaks
        if len(data["peak_positions"]) > 0:
            for i, peak_x in enumerate(data["peak_positions"]):
                label = "Detected Peaks" if i == 0 else ""
                self.axes.axvline(x=peak_x, color="red", linestyle="--", 
                                  alpha=0.7, label=label)
        
        self.axes.set_title("Distribution Density")
        self.axes.set_xlabel("Value")
        self.axes.set_ylabel("Density")
        self.axes.legend()
        self.axes.grid(True, linestyle=":", alpha=0.6)
        
        self.draw()

    def render_change_point(self, data: dict):
        """
        Renders Change-Point Detection results (Task 9/13).
        Expects: time_index, signal_values, change_points.
        """
        self.clear()
        
        # Plot signal
        self.axes.plot(data["time_index"], data["signal_values"], 
                       label="Signal/Statistic", color="#2ca02c", linewidth=1.5)
        
        # Plot vertical lines for change points
        if len(data["change_points"]) > 0:
            for i, cp in enumerate(data["change_points"]):
                label = "Change Points" if i == 0 else ""
                self.axes.axvline(x=cp, color="orange", linestyle="--", 
                                  alpha=0.8, label=label)
        
        self.axes.set_title("Time Series with Change Points")
        self.axes.set_xlabel("Time Index")
        self.axes.set_ylabel("Value")
        self.axes.legend()
        self.axes.grid(True, linestyle=":", alpha=0.6)
        
        self.draw()

"""
gui.widgets.matplotlib_canvas

Implements a PySide6-compatible Matplotlib canvas for rendering 
exploratory results without interpretation.
"""

import pandas as pd
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

    def render_population_structure(self, df: pd.DataFrame):
        """
        Renders A0.2 Population Structure (Task 24).
        Scatter (Median vs MAD) and Histogram of Medians.
        """
        self.fig.clear()
        
        # 1. Scatter Plot (Median vs MAD)
        ax1 = self.fig.add_subplot(121)
        ax1.scatter(df['median_delta_v1_subject'], df['mad_delta_v1_subject'], 
                    alpha=0.6, color='#1f77b4', edgecolors='white')
        ax1.set_title("Median vs MAD (ΔV1)")
        ax1.set_xlabel("Median (ms)")
        ax1.set_ylabel("MAD (ms)")
        ax1.grid(True, linestyle=":", alpha=0.6)

        # 2. Histogram (Median)
        ax2 = self.fig.add_subplot(122)
        ax2.hist(df['median_delta_v1_subject'], bins=15, 
                 color='#2ca02c', alpha=0.7, edgecolor='black')
        ax2.set_title("Median Distribution")
        ax2.set_xlabel("Median (ms)")
        ax2.set_ylabel("Frequency")
        ax2.grid(True, linestyle=":", alpha=0.6)

        self.fig.tight_layout()
        self.draw()

    def render_symmetry_structure(self, df: pd.DataFrame):
        """
        Renders A0.3 Architectural Symmetry (Task 25).
        Scatter (Diff L-R vs Center) and Boxplot of Medians.
        """
        self.fig.clear()
        
        # 1. Scatter Plot (Diff Left-Right vs Median Center)
        ax1 = self.fig.add_subplot(121)
        ax1.scatter(df['diff_left_right'], df['median_center'], 
                    alpha=0.6, color='#9467bd', edgecolors='white')
        ax1.set_title("Symmetry vs Central Field")
        ax1.set_xlabel("Diff Left - Right (ms)")
        ax1.set_ylabel("Median Center (ms)")
        ax1.axvline(x=0, color='black', linestyle='--', alpha=0.3)
        ax1.grid(True, linestyle=":", alpha=0.6)

        # 2. Boxplot (Left, Center, Right)
        ax2 = self.fig.add_subplot(122)
        box_data = [
            df['median_left'].dropna(),
            df['median_center'].dropna(),
            df['median_right'].dropna()
        ]
        ax2.boxplot(box_data, labels=['Left', 'Center', 'Right'], 
                    patch_artist=True, 
                    boxprops=dict(facecolor='#ff7f0e', alpha=0.7))
        ax2.set_title("Spatial Distribution")
        ax2.set_ylabel("Median ΔV1 (ms)")
        ax2.grid(True, linestyle=":", alpha=0.6)

        self.fig.tight_layout()
        self.draw()

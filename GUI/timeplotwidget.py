import numpy as np
import matplotlib.pyplot as plt
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class TimePlotWidget(QWidget):
    """Single-plot widget showing speed (left axis) and distance (right axis).

    The widget generates a time axis at 60 FPS when needed. It accepts
    two main datasets (speeds, distances) and optional post segments.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.layout = QVBoxLayout(self)
        self.figure, self.ax_main = plt.subplots(figsize=(8, 4))
        self.ax_twin = self.ax_main.twinx()

        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)

        self._style_axes()

    def _style_axes(self):
        self.figure.patch.set_facecolor('#2e2e2e')
        for ax in (self.ax_main, self.ax_twin):
            ax.set_facecolor('#2e2e2e')
            ax.tick_params(colors='white')
            for spine in ax.spines.values():
                spine.set_color('#00ffff')

        self.ax_main.set_xlabel('Time (s)', color='white')
        self.ax_main.set_ylabel('Speed (km/h)', color='white')
        self.ax_twin.set_ylabel('Distance (m)', color='white')
        self.ax_twin.yaxis.set_label_position('right')
        self.ax_twin.yaxis.tick_right()
        self.ax_main.grid(True, color='#444444', linestyle='--', linewidth=0.5, alpha=0.7)

    def _ensure_array(self, x):
        return np.array(x, dtype=float) if x is not None else np.array([])

    def _to_kmh_and_meters(self, speeds, times=None):
        s = self._ensure_array(speeds)
        if times is None:
            if len(s) == 0:
                return s, np.array([])
            dt = 1.0 / 60.0
        else:
            t = self._ensure_array(times)
            dt = float(t[1] - t[0]) if len(t) > 1 else 1.0 / 60.0

        speeds_ms = s * (1000.0 / 3600.0)
        distances = np.cumsum(speeds_ms * dt)
        return s, distances

    def update_data(self, speeds1, dist1, speeds2, dist2, labels, post1=None, post2=None):
        """Update the plot.

        speedsN: array-like of speeds in km/h.
        distN: optional array-like distances in meters (if absent they are computed).
        labels: (label1, label2)
        postN: optional post segments (2- or 3-tuples) or None.
        """
        self.ax_main.cla()
        self.ax_twin.cla()
        self._style_axes()

        s1 = self._ensure_array(speeds1)
        s2 = self._ensure_array(speeds2)

        t1 = np.arange(len(s1)) / 60.0 if len(s1) else np.array([])
        t2 = np.arange(len(s2)) / 60.0 if len(s2) else np.array([])

        if dist1 is None or len(self._ensure_array(dist1)) == 0:
            s1_kmh, d1 = self._to_kmh_and_meters(s1, times=t1)
        else:
            s1_kmh = s1
            d1 = self._ensure_array(dist1) * 1000  # convert km to meters

        if dist2 is None or len(self._ensure_array(dist2)) == 0:
            s2_kmh, d2 = self._to_kmh_and_meters(s2, times=t2)
        else:
            s2_kmh = s2
            d2 = self._ensure_array(dist2) * 1000  # convert km to meters

        color1 = '#2244FF'
        color2 = '#FF2222'

        if len(t1):
            self.ax_main.plot(t1, s1_kmh, color=color1, linestyle='-', label=f"{labels[0]} speed")
        if len(t2):
            self.ax_main.plot(t2, s2_kmh, color=color2, linestyle='-', label=f"{labels[1]} speed")

        if len(t1) and len(d1):
            self.ax_twin.plot(t1, d1, color=color1, linestyle='--', label=f"{labels[0]} distance")
        if len(t2) and len(d2):
            self.ax_twin.plot(t2, d2, color=color2, linestyle='--', label=f"{labels[1]} distance")

        self.ax_main.set_title('Speed and Distance vs Time', color='white')

        def plot_post(post, color, prefix):
            if post is None:
                return
            
            if len(post) == 3:
                ptimes, pspeeds, _ = post
            elif len(post) == 2:
                pspeeds, _ = post
                ptimes = np.arange(len(pspeeds)) / 60.0
            else:
                return

            ps, pd = self._to_kmh_and_meters(pspeeds, times=ptimes)
            self.ax_main.plot(ptimes, ps, color=color, linestyle=':', label=f"{prefix} post speed")
            self.ax_twin.plot(ptimes, pd, color=color, linestyle=':', label=f"{prefix} post distance")

        plot_post(post1, color1, labels[0])
        plot_post(post2, color2, labels[1])

        h1, l1 = self.ax_main.get_legend_handles_labels()
        h2, l2 = self.ax_twin.get_legend_handles_labels()
        handles = h1 + h2
        labels_all = l1 + l2
        if handles:
            leg = self.ax_main.legend(handles, labels_all, loc='lower right')
            frame = leg.get_frame()
            frame.set_facecolor('#2e2e2e')
            frame.set_edgecolor('#00ffff')
            for text in leg.get_texts():
                text.set_color('white')

        self.figure.tight_layout()
        self.canvas.update()
        self.canvas.draw()

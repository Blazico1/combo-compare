import sys
import numpy as np
import matplotlib.pyplot as plt

from matplotlib.patches import RegularPolygon
from matplotlib.path import Path
from matplotlib.projections import register_projection
from matplotlib.projections.polar import PolarAxes
from matplotlib.spines import Spine
from matplotlib.transforms import Affine2D
from PyQt6.QtWidgets import QApplication, QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


def radar_factory(num_vars, frame='circle'):
    """
    Create a radar chart with `num_vars` Axes.

    This function creates a RadarAxes projection and registers it.

    Parameters
    ----------
    num_vars : int
        Number of variables for radar chart.
    frame : {'circle', 'polygon'}
        Shape of frame surrounding Axes.

    Source: https://matplotlib.org/stable/gallery/specialty_plots/radar_chart.html
    """
    # calculate evenly-spaced axis angles
    theta = np.linspace(0, 2*np.pi, num_vars, endpoint=False)

    class RadarTransform(PolarAxes.PolarTransform):

        def transform_path_non_affine(self, path):
            # Paths with non-unit interpolation steps correspond to gridlines,
            # in which case we force interpolation (to defeat PolarTransform's
            # autoconversion to circular arcs).
            if path._interpolation_steps > 1:
                path = path.interpolated(num_vars)
            return Path(self.transform(path.vertices), path.codes)

    class RadarAxes(PolarAxes):

        name = 'radar'
        PolarTransform = RadarTransform

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # rotate plot such that the first axis is at the top
            self.set_theta_zero_location('N')

        def fill(self, *args, closed=True, **kwargs):
            """Override fill so that line is closed by default"""
            return super().fill(closed=closed, *args, **kwargs)

        def plot(self, *args, **kwargs):
            """Override plot so that line is closed by default"""
            lines = super().plot(*args, **kwargs)
            for line in lines:
                self._close_line(line)

        def _close_line(self, line):
            x, y = line.get_data()
            # FIXME: markers at x[0], y[0] get doubled-up
            if x[0] != x[-1]:
                x = np.append(x, x[0])
                y = np.append(y, y[0])
                line.set_data(x, y)

        def set_varlabels(self, labels):
            self.set_thetagrids(np.degrees(theta), labels)

        def _gen_axes_patch(self):
            # The Axes patch must be centered at (0.5, 0.5) and of radius 0.5
            # in axes coordinates.
            if frame == 'circle':
                return Circle((0.5, 0.5), 0.5)
            elif frame == 'polygon':
                return RegularPolygon((0.5, 0.5), num_vars,
                                      radius=.5, edgecolor="k")
            else:
                raise ValueError("Unknown value for 'frame': %s" % frame)

        def _gen_axes_spines(self):
            if frame == 'circle':
                return super()._gen_axes_spines()
            elif frame == 'polygon':
                # spine_type must be 'left'/'right'/'top'/'bottom'/'circle'.
                spine = Spine(axes=self,
                              spine_type='circle',
                              path=Path.unit_regular_polygon(num_vars))
                # unit_regular_polygon gives a polygon of radius 1 centered at
                # (0, 0) but we want a polygon of radius 0.5 centered at (0.5,
                # 0.5) in axes coordinates.
                spine.set_transform(Affine2D().scale(.5).translate(.5, .5)
                                    + self.transAxes)
                return {'polar': spine}
            else:
                raise ValueError("Unknown value for 'frame': %s" % frame)

    register_projection(RadarAxes)
    return theta

class RadarChartWidget(QWidget):
    def __init__(self, data_sets, labels, title, frame='polygon', show_legend=False, show_numbers=True, legend_labels=None, parent=None):
        super().__init__(parent)
        self.show_legend = show_legend
        self.show_numbers = show_numbers
        self.legend_labels = legend_labels if legend_labels is not None else [f'Data {i+1}' for i in range(len(data_sets))]
        self.data_sets = data_sets
        self.labels = labels
        self.title = title
        self.frame = frame

        num_vars = len(self.labels)
        self.theta = radar_factory(num_vars, frame=self.frame)

        self.layout = QVBoxLayout(self)
        self.figure, self.ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(projection='radar'))
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)
    
        self.create_radar_chart()

    def create_radar_chart(self):
        
        self.ax.clear()
        self.ax.set_theta_zero_location('N')
        self.ax.set_theta_direction(-1)
        self.ax.set_ylim(0, 1.1)

        colors = ['b', 'r']  # Add more colors if you have more data sets
        for data, color, label in zip(self.data_sets, colors, self.legend_labels):
            self.ax.plot(self.theta, data, color=color, label=label)
            self.ax.fill(self.theta, data, facecolor=color, alpha=0.25)

        self.ax.set_varlabels(self.labels)
        self.ax.set_title(self.title, weight='bold', size='medium', position=(0.5, 1.1),
                          horizontalalignment='center', verticalalignment='center')

        if not self.show_numbers:
            self.ax.set_yticklabels([])

        if self.show_legend:
            self.ax.legend(loc='upper right', bbox_to_anchor=(1.1, 1.1))

        self.figure.subplots_adjust(top=0.85, bottom=0.05)

    def update_data(self, data_sets, legend_labels=None):
        self.data_sets = data_sets
        self.legend_labels = legend_labels if legend_labels is not None else [f'Data {i+1}' for i in range(len(data_sets))]

        # Recreate the radar chart with the new data
        self.create_radar_chart()

        # Redraw the canvas
        self.canvas.draw()
        
if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Custom data and labels
    labels = ['Speed', 'Weight', 'Acceleration', 'Handling', 'Drift', 'Offroad', 'Mini-Turbo']
    data1 = [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2]
    data2 = [0.6, 0.7, 0.8, 0.5, 0.4, 0.3, 0.9]
    title = None
    legend_labels = ['Standard Kart', 'Standard Bike']

    # Create and display the radar chart widget with custom data and labels
    radar_chart_widget = RadarChartWidget([data1, data2], labels, title, frame='polygon', show_legend=True, show_numbers=False, legend_labels=legend_labels)
    radar_chart_widget.show()
    import time
    time.sleep(2)
    radar_chart_widget.update_data([data1, data1], legend_labels=['Standard Bike', 'Standard Kart'])
    
    sys.exit(app.exec())

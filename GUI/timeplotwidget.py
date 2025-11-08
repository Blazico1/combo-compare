import numpy as np
import matplotlib.pyplot as plt
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class TimePlotWidget(QWidget):
    """Dynamic layout widget: single-plot (normal) or dual-plot (differential).

    Normal: speed/distance on single plot with dual y-axes.
    Differential: speed diff (top), distance diff (bottom) on separate plots.
    Generates 60 FPS time axis, converts sim units to meters.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.layout = QVBoxLayout(self)
        self.figure = None
        self.ax_main = None
        self.ax_twin = None
        self.ax_speed = None
        self.ax_distance = None
        self.current_diff_mode = False

        self.canvas = None
        self._create_single_plot()

    def _create_single_plot(self):
        """Create single plot with dual y-axes for normal mode.
        
        Sets up matplotlib figure with primary axis for speed and twin axis
        for distance. Applies dark theme styling and grid.
        """
        if self.figure is not None:
            plt.close(self.figure)

        self.figure, self.ax_main = plt.subplots(figsize=(8, 4))
        self.ax_twin = self.ax_main.twinx()
        self.ax_speed = None
        self.ax_distance = None

        if self.canvas is not None:
            self.layout.removeWidget(self.canvas)
            self.canvas.deleteLater()

        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)

        self._style_single_plot()

    def _create_dual_plot(self):
        """Create two stacked plots for differential mode.
        
        Sets up matplotlib figure with two subplots: top for speed difference,
        bottom for distance difference. Applies dark theme styling.
        """
        if self.figure is not None:
            plt.close(self.figure)

        self.figure, (self.ax_speed, self.ax_distance) = plt.subplots(
            2, 1, figsize=(8, 6))
        self.ax_main = None
        self.ax_twin = None

        if self.canvas is not None:
            self.layout.removeWidget(self.canvas)
            self.canvas.deleteLater()

        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)

        self._style_dual_plot()

    def _style_single_plot(self):
        """Apply dark theme styling to single plot layout.
        
        Configures colors, spines, labels, and grid for the dual-axis plot.
        Distance axis uses dashed spine to distinguish from speed axis.
        """
        self.figure.patch.set_facecolor('#2e2e2e')
        for ax in (self.ax_main, self.ax_twin):
            ax.set_facecolor('#2e2e2e')
            ax.tick_params(colors='white')
            for spine in ax.spines.values():
                spine.set_color('#00ffff')
                spine.set_visible(True)

        # Make the distance axis (right spine) dashed
        self.ax_twin.spines['right'].set_position(('outward', 0))
        self.ax_twin.spines['right'].set_linestyle((0, (4, 2)))
        self.ax_twin.spines['right'].set_linewidth(2)

        self.ax_main.set_xlabel('Time (s)', color='white')
        self.ax_main.set_ylabel('Speed (km/h)', color='white')
        self.ax_twin.set_ylabel('Distance (m)', color='white')
        self.ax_twin.yaxis.set_label_position('right')
        self.ax_twin.yaxis.tick_right()
        self.ax_main.grid(True, color='#444444', linestyle='--',
                          linewidth=0.5, alpha=0.7)

    def _style_dual_plot(self):
        """Apply dark theme styling to dual plot layout.
        
        Configures colors, spines, labels, titles, and grids for both
        speed and distance difference subplots.
        """
        self.figure.patch.set_facecolor('#2e2e2e')

        # Style speed plot (top)
        self.ax_speed.set_facecolor('#2e2e2e')
        self.ax_speed.tick_params(colors='white')
        for spine in self.ax_speed.spines.values():
            spine.set_color('#00ffff')
            spine.set_visible(True)
        self.ax_speed.set_ylabel('Speed Difference (km/h)', color='white')
        self.ax_speed.grid(True, color='#444444', linestyle='--',
                           linewidth=0.5, alpha=0.7)
        self.ax_speed.set_title('Speed Difference', color='white', fontsize=12)

        # Style distance plot (bottom)
        self.ax_distance.set_facecolor('#2e2e2e')
        self.ax_distance.tick_params(colors='white')
        for spine in self.ax_distance.spines.values():
            spine.set_color('#00ffff')
            spine.set_visible(True)
        self.ax_distance.set_xlabel('Time (s)', color='white')
        self.ax_distance.set_ylabel('Distance Difference (m)', color='white')
        self.ax_distance.grid(True, color='#444444', linestyle='--',
                              linewidth=0.5, alpha=0.7)
        self.ax_distance.set_title('Distance Difference', color='white',
                                   fontsize=12)

        # Adjust spacing
        self.figure.subplots_adjust(hspace=0.3)

    def _plot_differential_dual(self, s1, s2, d1, d2, t):
        """Plot differential curves on dual axes for differential mode.
        
        Args:
            s1, s2: Speed arrays (km/h) for combo 1 and 2
            d1, d2: Distance arrays (sim units) for combo 1 and 2
            t: Time array (seconds)
            
        Computes differences and plots color-coded segments with zero
        crossings. Blue segments show combo 1 advantage, red shows combo 2
        advantage.
        """
        if len(s1) == 0 or len(s2) == 0 or len(d1) == 0 or len(d2) == 0:
            return

        # Ensure all arrays have the same length (use minimum length)
        min_len = min(len(s1), len(s2), len(d1), len(d2), len(t))
        s1 = s1[:min_len]
        s2 = s2[:min_len]
        d1 = d1[:min_len]
        d2 = d2[:min_len]
        t = t[:min_len]

        # Calculate differences
        speed_diff = s1 - s2
        dist_diff = d1 - d2

        # Plot speed difference on top axis
        self._plot_colored_segments(t, speed_diff, self.ax_speed, solid=True)

        # Plot distance difference on bottom axis
        self._plot_colored_segments(t, dist_diff, self.ax_distance,
                                    solid=False)

        # Add horizontal zero lines
        self.ax_speed.axhline(y=0, color='white', linestyle='-',
                              alpha=0.7, linewidth=1)
        self.ax_distance.axhline(y=0, color='white', linestyle='-',
                                 alpha=0.7, linewidth=1)

    def _plot_colored_segments(self, t, values, ax, solid=True):
        """Plot values with color-coded segments based on sign.
        
        Args:
            t: Time array (seconds)
            values: Value array to plot (differences)
            ax: Matplotlib axis to plot on
            solid: True for solid lines, False for dashed
            
        Segments are colored blue when positive (combo 1 better) and red when
        negative (combo 2 better). Zero crossings are interpolated for smooth
        color transitions.
        """
        if len(values) < 2:
            return

        linestyle = '-' if solid else '--'
        linewidth = 2 if solid else 1.5

        segments = []
        i = 0
        while i < len(values):
            val = values[i]
            start_idx = i

            if val > 0:
                segment_type = 'positive'
            elif val < 0:
                segment_type = 'negative'
            else:
                segment_type = 'zero'

            i += 1
            while i < len(values):
                next_val = values[i]
                if ((segment_type == 'positive' and next_val <= 0) or
                        (segment_type == 'negative' and next_val >= 0) or
                        (segment_type == 'zero' and next_val != 0)):
                    break
                i += 1

            end_idx = i - 1
            segments.append({
                'type': segment_type,
                'start_idx': start_idx,
                'end_idx': end_idx
            })

        for j, segment in enumerate(segments):
            segment_type = segment['type']
            start_idx = segment['start_idx']
            end_idx = segment['end_idx']

            if segment_type == 'positive':
                color = '#2244FF'
            elif segment_type == 'negative':
                color = '#FF2222'
            else:
                color = '#FF00FF'

            segment_plot_t = []
            segment_plot_vals = []

            if j > 0:
                prev_end_idx = segments[j-1]['end_idx']
                curr_start_idx = start_idx

                prev_val = values[prev_end_idx]
                curr_val = values[curr_start_idx]
                prev_t = t[prev_end_idx]
                curr_t = t[curr_start_idx]

                if ((prev_val > 0 and curr_val < 0) or
                        (prev_val < 0 and curr_val > 0)):
                    fraction = -prev_val / (curr_val - prev_val)
                    cross_time = prev_t + fraction * (curr_t - prev_t)
                    segment_plot_t.append(cross_time)
                    segment_plot_vals.append(0.0)

            segment_t = t[start_idx:end_idx+1]
            segment_vals = values[start_idx:end_idx+1]
            segment_plot_t.extend(segment_t)
            segment_plot_vals.extend(segment_vals)

            if j < len(segments) - 1:
                curr_end_idx = end_idx
                next_start_idx = segments[j+1]['start_idx']

                curr_val = values[curr_end_idx]
                next_val = values[next_start_idx]
                curr_t = t[curr_end_idx]
                next_t = t[next_start_idx]

                if ((curr_val > 0 and next_val < 0) or
                        (curr_val < 0 and next_val > 0)):
                    fraction = -curr_val / (next_val - curr_val)
                    cross_time = curr_t + fraction * (next_t - curr_t)
                    segment_plot_t.append(cross_time)
                    segment_plot_vals.append(0.0)

            ax.plot(segment_plot_t, segment_plot_vals, color=color,
                    linestyle=linestyle, linewidth=linewidth)

    def update_data(self, speeds1, dist1, speeds2, dist2,
                    left_selected=False, right_selected=False,
                    post1=None, post2=None, diff_mode=False,
                    left_hidden=False, right_hidden=False):
        """Update the plot with new simulation data.
        
        Args:
            speeds1, speeds2: Speed arrays (km/h) for left/right combos
            dist1, dist2: Distance arrays (sim units) for left/right combos
            left_selected, right_selected: Whether combos are selected
            post1, post2: Optional post-simulation segments (2-3 tuples)
            diff_mode: True for differential plotting, False for normal
            left_hidden, right_hidden: Whether to hide left/right combos
            
        Converts distances from sim units to meters, generates time axis,
        and switches plot layout if differential mode changed.
        """
        # Switch layout if differential mode changed
        if diff_mode != self.current_diff_mode:
            self.current_diff_mode = diff_mode
            if diff_mode:
                self._create_dual_plot()
            else:
                self._create_single_plot()

        # Clear current axes
        if diff_mode:
            self.ax_speed.cla()
            self.ax_distance.cla()
            self._style_dual_plot()
        else:
            self.ax_main.cla()
            self.ax_twin.cla()
            self._style_single_plot()

        s1 = np.array(speeds1, dtype=float) if speeds1 is not None \
            else np.array([])
        s2 = np.array(speeds2, dtype=float) if speeds2 is not None \
            else np.array([])
        d1 = (np.array(dist1, dtype=float) if dist1 is not None
              else np.array([])) / 216
        d2 = (np.array(dist2, dtype=float) if dist2 is not None
              else np.array([])) / 216

        t1 = np.arange(len(s1)) / 60.0 if len(s1) else np.array([])
        t2 = np.arange(len(s2)) / 60.0 if len(s2) else np.array([])

        if not left_selected and not right_selected:
            if diff_mode:
                self.ax_speed.text(0.5, 0.5,
                                   'Pick at least one vehicle-character combo',
                                   ha='center', va='center',
                                   transform=self.ax_speed.transAxes,
                                   fontsize=14, color='white')
            else:
                self.ax_main.text(0.5, 0.5,
                                  'Pick at least one vehicle-character combo',
                                  ha='center', va='center',
                                  transform=self.ax_main.transAxes,
                                  fontsize=14, color='white')
            self.canvas.update()
            self.canvas.draw()
            return

        if diff_mode and left_selected and right_selected:
            self._plot_differential_dual(s1, s2, d1, d2, t1)
        else:
            if len(t1) and not left_hidden:
                self.ax_main.plot(t1, s1, color='#2244FF', linestyle='-')
            if len(t2) and not right_hidden:
                self.ax_main.plot(t2, s2, color='#FF2222', linestyle='-')

            if len(t1) and len(d1) and not left_hidden:
                self.ax_twin.plot(t1, d1, color='#2244FF', linestyle='--')
            if len(t2) and len(d2) and not right_hidden:
                self.ax_twin.plot(t2, d2, color='#FF2222', linestyle='--')

        # Handle post segments (only for normal mode)
        if not diff_mode:
            def plot_post(post, color):
                if post is None:
                    return

                if len(post) == 3:
                    ptimes, pspeeds, pdist = post
                    pd = np.array(pdist, dtype=float) / 216
                elif len(post) == 2:
                    pspeeds, pdist = post
                    ptimes = np.arange(len(pspeeds)) / 60.0
                    pd = np.array(pdist, dtype=float) / 216
                else:
                    return

                self.ax_main.plot(ptimes, pspeeds, color=color, linestyle=':')
                self.ax_twin.plot(ptimes, pd, color=color, linestyle=':')

            if not left_hidden:
                plot_post(post1, '#2244FF')
            if not right_hidden:
                plot_post(post2, '#FF2222')

        self.canvas.update()
        self.canvas.draw()

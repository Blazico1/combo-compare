from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QTextEdit,
    QFileDialog,
    QMessageBox,
    QTabWidget,
    QComboBox,
    QLabel,
    QCheckBox,
    QScrollArea,
    QFrame,
    QGridLayout,
    )
from PyQt6.QtCore import Qt
from GUI.radarchartwidget import RadarChartWidget
from GUI.timeplotwidget import TimePlotWidget

CATEGORIES = ["Speed", "Mini-Turbo", "Drift", "Acceleration", "Off-Road", "Weight", "Handling"] 
    
class View(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Combo Compare")
        self.setGeometry(100, 100, 800, 600)

        self.tabs = QTabWidget()
        self.file_tab = QWidget()
        self.basic_stats_tab = QWidget()
        self.simulation_tab = QWidget()
        self.advanced_stats_tab = QWidget()

        self.tabs.addTab(self.file_tab, "File")
        self.tabs.addTab(self.basic_stats_tab, "Basic stats")
        self.tabs.addTab(self.simulation_tab, "Simulation")
        self.tabs.addTab(self.advanced_stats_tab, "Advanced stats")

        self.init_file_tab()
        self.init_basic_stats_tab()
        self.init_sim_tab()
        self.init_advanced_stats_tab()

        layout = QVBoxLayout()
        layout.addWidget(self.tabs)
        self.setLayout(layout)

    def init_file_tab(self):
        layout = QVBoxLayout()

        self.choose_file_button = QPushButton("Choose File")
        layout.addWidget(self.choose_file_button)

        self.extract_files_button = QPushButton("Extract Files")
        layout.addWidget(self.extract_files_button)

        self.status_textbox = QTextEdit()
        self.status_textbox.setReadOnly(True)
        layout.addWidget(self.status_textbox)

        self.file_tab.setLayout(layout)

    def init_basic_stats_tab(self):
        main_layout = QHBoxLayout()

        # Define the stylesheet for the labels
        label_stylesheet = """
            QLabel {
                font-weight: bold;
                font-size: 14pt;
                text-align: center;
            }
        """

        # Define the stylesheet for the QComboBox
        dropdown_stylesheet = """
            QComboBox {
                background-color: #3e3e3e;
                color: #ffffff;
                border: 1px solid #00ffff;
            }
            QComboBox QAbstractItemView {
                background-color: #3e3e3e;
                color: #ffffff;
                selection-background-color: #00ffff;
                selection-color: #2e2e2e;
            }
        """

        # Left column layout
        left_container = QWidget()
        left_container.setStyleSheet("background-color: darkblue;")
        left_layout = QVBoxLayout(left_container)
        self.left_label = QLabel("Combo 1")
        self.left_label.setStyleSheet(label_stylesheet)
        self.left_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.left_dropdown_v = QComboBox()
        self.left_dropdown_v.setStyleSheet(dropdown_stylesheet)
        self.left_dropdown_c = QComboBox()
        self.left_dropdown_c.setStyleSheet(dropdown_stylesheet)
        left_layout.addStretch()  # Add a stretchable space at the top
        left_layout.addWidget(self.left_label)
        left_layout.addWidget(self.left_dropdown_v)
        left_layout.addWidget(self.left_dropdown_c)
        left_layout.addStretch()  # Add a stretchable space at the bottom

        # Right column layout
        right_container = QWidget()
        right_container.setStyleSheet("background-color: darkred;")
        right_layout = QVBoxLayout(right_container)
        self.right_label = QLabel("Combo 2")
        self.right_label.setStyleSheet(label_stylesheet)
        self.right_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.right_dropdown_v = QComboBox()
        self.right_dropdown_v.setStyleSheet(dropdown_stylesheet)
        self.right_dropdown_c = QComboBox()
        self.right_dropdown_c.setStyleSheet(dropdown_stylesheet)
        right_layout.addStretch()  # Add a stretchable space at the top
        right_layout.addWidget(self.right_label)
        right_layout.addWidget(self.right_dropdown_v)
        right_layout.addWidget(self.right_dropdown_c)
        right_layout.addStretch()  # Add a stretchable space at the bottom

        # Middle column layout
        middle_layout = QVBoxLayout()
        self.status_label = QLabel("Please select a Common.szs file to extract.")
        middle_layout.addWidget(self.status_label)
        self.chart_view = RadarChartWidget([], CATEGORIES, None, frame='polygon', show_legend=True, show_numbers=False)
        middle_layout.addWidget(self.chart_view)

        # Add layouts to the main layout
        main_layout.addWidget(left_container)
        main_layout.addLayout(middle_layout, stretch=3)  # Middle column takes up most of the space
        main_layout.addWidget(right_container)

        self.basic_stats_tab.setLayout(main_layout)

    def init_sim_tab(self):
        main_layout = QHBoxLayout()

        # Define the stylesheet for the labels
        label_stylesheet = """
            QLabel {
                font-weight: bold;
                font-size: 14pt;
                text-align: center;
            }
        """

        # Define the stylesheet for the QComboBox
        dropdown_stylesheet = """
            QComboBox {
                background-color: #3e3e3e;
                color: #ffffff;
                border: 1px solid #00ffff;
            }
            QComboBox QAbstractItemView {
                background-color: #3e3e3e;
                color: #ffffff;
                selection-background-color: #00ffff;
                selection-color: #2e2e2e;
            }
        """

        # Left column layout
        left_container = QWidget()
        left_container.setStyleSheet("background-color: darkblue;")
        left_layout = QVBoxLayout(left_container)
        self.sim_left_label = QLabel("Combo 1")
        self.sim_left_label.setStyleSheet(label_stylesheet)
        self.sim_left_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.sim_left_dropdown_v = QComboBox()
        self.sim_left_dropdown_v.setStyleSheet(dropdown_stylesheet)
        self.sim_left_dropdown_c = QComboBox()
        self.sim_left_dropdown_c.setStyleSheet(dropdown_stylesheet)
        # Per-combo options
        self.sim_left_hide_cb = QCheckBox("Hide")
        self.sim_left_wheelie_cb = QCheckBox("Wheelie")
        self.sim_left_smt_cb = QCheckBox("SMT")
        self.sim_left_ssmt_cb = QCheckBox("SSMT")
        left_layout.addStretch()  # Add a stretchable space at the top
        left_layout.addWidget(self.sim_left_label)
        left_layout.addWidget(self.sim_left_dropdown_v)
        left_layout.addWidget(self.sim_left_dropdown_c)
        left_layout.addWidget(self.sim_left_hide_cb)
        left_layout.addWidget(self.sim_left_wheelie_cb)
        left_layout.addWidget(self.sim_left_smt_cb)
        left_layout.addWidget(self.sim_left_ssmt_cb)
        left_layout.addStretch()  # Add a stretchable space at the bottom

        # Right column layout
        right_container = QWidget()
        right_container.setStyleSheet("background-color: darkred;")
        right_layout = QVBoxLayout(right_container)
        self.sim_right_label = QLabel("Combo 2")
        self.sim_right_label.setStyleSheet(label_stylesheet)
        self.sim_right_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.sim_right_dropdown_v = QComboBox()
        self.sim_right_dropdown_v.setStyleSheet(dropdown_stylesheet)
        self.sim_right_dropdown_c = QComboBox()
        self.sim_right_dropdown_c.setStyleSheet(dropdown_stylesheet)
        self.sim_right_hide_cb = QCheckBox("Hide")
        self.sim_right_wheelie_cb = QCheckBox("Wheelie")
        self.sim_right_smt_cb = QCheckBox("SMT")
        self.sim_right_ssmt_cb = QCheckBox("SSMT")
        right_layout.addStretch()  # Add a stretchable space at the top
        right_layout.addWidget(self.sim_right_label)
        right_layout.addWidget(self.sim_right_dropdown_v)
        right_layout.addWidget(self.sim_right_dropdown_c)
        right_layout.addWidget(self.sim_right_hide_cb)
        right_layout.addWidget(self.sim_right_wheelie_cb)
        right_layout.addWidget(self.sim_right_smt_cb)
        right_layout.addWidget(self.sim_right_ssmt_cb)
        right_layout.addStretch()  # Add a stretchable space at the bottom

        # Middle column layout
        middle_layout = QVBoxLayout()
        self.sim_status_label = QLabel("Please select a Common.szs file to extract.")
        middle_layout.addWidget(self.sim_status_label)

        # Simulation settings row
        settings_row = QHBoxLayout()
        self.sim_type_dropdown = QComboBox()
        self.sim_type_dropdown.addItems(["Acceleration", "Mini-turbo"])
        self.sim_diff_checkbox = QCheckBox("Differential Mode")
        self.sim_export_button = QPushButton("Export Plot")
        settings_row.addWidget(self.sim_type_dropdown)
        settings_row.addWidget(self.sim_diff_checkbox)
        settings_row.addWidget(self.sim_export_button)
        middle_layout.addLayout(settings_row)

        # Time plots widget
        self.sim_widget = TimePlotWidget()
        middle_layout.addWidget(self.sim_widget)

        # Add layouts to the main layout
        main_layout.addWidget(left_container)
        main_layout.addLayout(middle_layout, stretch=3)  # Middle column takes up most of the space
        main_layout.addWidget(right_container)

        self.simulation_tab.setLayout(main_layout)

    def init_advanced_stats_tab(self):
        """Create the advanced stats tab with three columns (left values, stat name, right values).
        Similar stats are grouped and separated by horizontal lines.
        """
        # Scroll area in case there are many rows
        scroll = QScrollArea()
        container = QWidget()
        grid = QGridLayout(container)

        # List of stats as (display_name, key)
        stats = [
            ("Number of Tires", "num_tires"),
            ("Drift Type", "drift_type"),
            ("Weight Class", "weight_class"),
            ("Unknown", "unknown"),
            ("Weight", "weight"),
            ("Bump Deviation", "bump_deviation"),
            ("Speed", "speed"),
            ("Speed in Turn", "speed_in_turn"),
            ("Tilt", "tilt"),
            ("Std Accel A0", "std_accel_a0"),
            ("Std Accel A1", "std_accel_a1"),
            ("Std Accel A2", "std_accel_a2"),
            ("Std Accel A3", "std_accel_a3"),
            ("Std Accel T1", "std_accel_t1"),
            ("Std Accel T2", "std_accel_t2"),
            ("Std Accel T3", "std_accel_t3"),
            ("Drift Accel A0", "drift_accel_a0"),
            ("Drift Accel A1", "drift_accel_a1"),
            ("Drift Accel T1", "drift_accel_t1"),
            ("Manual Handling", "manual_handling"),
            ("Auto Handling", "auto_handling"),
            ("Handling Reactivity", "handling_reactivity"),
            ("Manual Drift", "manual_drift"),
            ("Auto Drift", "auto_drift"),
            ("Drift Reactivity", "drift_reactivity"),
            ("Outside Drift Angle", "outside_drift_angle"),
            ("Outside Drift Decrement", "outside_drift_decrement"),
            ("Mini Turbo Duration", "mini_turbo_duration"),
            ("Rotating Items Z Radius", "rotating_items_z_radius"),
            ("Rotating Items X Radius", "rotating_items_x_radius"),
            ("Rotating Items Y Distance", "rotating_items_y_distance"),
            ("Rotating Items Z Distance", "rotating_items_z_distance"),
            ("Max Normal Accel", "max_normal_accel"),
            ("Mega Mushroom Scale", "mega_mushroom_scale"),
            ("Tire Distance", "tire_distance"),
        ]

        # Where to place separators (row indices after which to add a horizontal line)
        # Group: basic, acceleration, handling, drift, items, misc
        separator_after = [8, 18, 25, 28, 32]

        # Keep references to labels so controller can update values
        self.advanced_left_labels = {}
        self.advanced_right_labels = {}

        # Top two rows: Vehicle and Character selectors
        self.advanced_left_dropdown_v = QComboBox()
        mid_vehicle = QLabel("Vehicle")
        mid_vehicle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        mid_vehicle.setStyleSheet("font-weight: bold;")
        self.advanced_right_dropdown_v = QComboBox()

        self.advanced_left_dropdown_c = QComboBox()
        mid_character = QLabel("Character")
        mid_character.setAlignment(Qt.AlignmentFlag.AlignCenter)
        mid_character.setStyleSheet("font-weight: bold;")
        self.advanced_right_dropdown_c = QComboBox()

        # place the top rows
        grid.addWidget(self.advanced_left_dropdown_v, 0, 0)
        grid.addWidget(mid_vehicle, 0, 1)
        grid.addWidget(self.advanced_right_dropdown_v, 0, 2)
        grid.addWidget(self.advanced_left_dropdown_c, 1, 0)
        grid.addWidget(mid_character, 1, 1)
        grid.addWidget(self.advanced_right_dropdown_c, 1, 2)

        row = 2
        for i, (disp, key) in enumerate(stats):
            # Left value (for combo 1)
            left_label = QLabel("-")
            left_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            # Middle stat name
            mid_label = QLabel(disp)
            mid_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            mid_label.setStyleSheet("font-weight: bold;")
            # Right value (for combo 2)
            right_label = QLabel("-")
            right_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

            grid.addWidget(left_label, row, 0)
            grid.addWidget(mid_label, row, 1)
            grid.addWidget(right_label, row, 2)

            self.advanced_left_labels[key] = left_label
            self.advanced_right_labels[key] = right_label

            row += 1

            if i in separator_after:
                sep = QFrame()
                sep.setFrameShape(QFrame.Shape.HLine)
                sep.setFrameShadow(QFrame.Shadow.Sunken)
                grid.addWidget(sep, row, 0, 1, 3)
                row += 1

        container.setLayout(grid)
        scroll.setWidget(container)
        scroll.setWidgetResizable(True)

        layout = QVBoxLayout()
        layout.addWidget(scroll)
        self.advanced_stats_tab.setLayout(layout)

    def update_advanced_stats(self, left_stats: dict, right_stats: dict):
        """Update the advanced stats labels for left and right combos.
        Both `left_stats` and `right_stats` are dicts keyed by the internal keys used above.
        If a key is missing, show '-'.
        """
        def fmt(v):
            """Format a value to 5 significant digits. Handles numbers and lists/tuples.
            Non-numeric values are returned as-is (stringified).
            """
            if v is None:
                return '-'
            # If it's a list/tuple, format each element
            if isinstance(v, (list, tuple)):
                parts = []
                for x in v:
                    try:
                        parts.append("{:.5g}".format(float(x)))
                    except Exception:
                        parts.append(str(x))
                return '[' + ', '.join(parts) + ']'
            # Try to format as float
            try:
                # If it's an integer, show as integer
                if isinstance(v, int) and not isinstance(v, bool):
                    return str(v)
                fv = float(v)
                return "{:.5g}".format(fv)
            except Exception:
                return str(v)

        # Mapping dicts for special keys
        wc_map = {0: 'Light', 1: 'Medium', 2: 'Heavy'}
        tires_map = {
            0: '4 Tires', 1: '2 Tires (Handle Rel)',
            2: '2 Tires (Vehicle Rel)', 3: '3 Tires'
        }
        drift_map = {0: 'Outside (Kart)', 1: 'Outside (Bike)', 2: 'Inside'}

        # Update vehicle/character name rows - removed since now combos

        # Handle weight_class specially: map 0/1/2 to labels and if both sides have a value
        # and they mismatch, leave the field empty as requested.
        l_wc_raw = left_stats.get('weight_class', None) if left_stats else None
        r_wc_raw = right_stats.get('weight_class', None) if right_stats else None

        # Show per-side mapping (the model will set None when a vehicle/character combo has internal mismatch)
        self.advanced_left_labels['weight_class'].setText(
            wc_map.get(l_wc_raw, str(l_wc_raw)) if l_wc_raw is not None else '-')
        self.advanced_right_labels['weight_class'].setText(
            wc_map.get(r_wc_raw, str(r_wc_raw)) if r_wc_raw is not None else '-')

        # Handle num_tires specially
        l_nt_raw = left_stats.get('num_tires', None) if left_stats else None
        r_nt_raw = right_stats.get('num_tires', None) if right_stats else None
        
        self.advanced_left_labels['num_tires'].setText(
            tires_map.get(l_nt_raw, str(l_nt_raw)) if l_nt_raw is not None else '-')
    
        self.advanced_right_labels['num_tires'].setText(
            tires_map.get(r_nt_raw, str(r_nt_raw)) if r_nt_raw is not None else '-')

        # Handle drift_type specially
        l_dt_raw = left_stats.get('drift_type', None) if left_stats else None
        r_dt_raw = right_stats.get('drift_type', None) if right_stats else None
        self.advanced_left_labels['drift_type'].setText(
            drift_map.get(l_dt_raw, str(l_dt_raw)) if l_dt_raw is not None else '-')
        self.advanced_right_labels['drift_type'].setText(
            drift_map.get(r_dt_raw, str(r_dt_raw)) if r_dt_raw is not None else '-')

        # Now set all other keys (skip special ones)
        for key, label in self.advanced_left_labels.items():
            if key in ('weight_class', 'num_tires', 'drift_type'):
                continue
            val = left_stats.get(key, '-') if left_stats else '-'
            label.setText(fmt(val))

        for key, label in self.advanced_right_labels.items():
            if key in ('weight_class', 'num_tires', 'drift_type'):
                continue
            val = right_stats.get(key, '-') if right_stats else '-'
            label.setText(fmt(val))

    def update_status(self, message):
        self.status_textbox.setText(message)

    def show_error_message(self, message):
        QMessageBox.critical(self, "Error", message)

    def get_file_path(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Select Common.szs file", "", "SZS Files (*.szs);;All Files (*)")
        return file_path

    def update_basic_stats_tab(self, available):
        # Enable/disable all non-file tabs so callers don't need to guard
        # UI actions with file-existence checks.
        # Tab order: 0=File, 1=Basic stats, 2=Simulation, 3=Advanced stats
        for idx in range(1, self.tabs.count()):
            self.tabs.setTabEnabled(idx, bool(available))

        if available:
            # show the components inside the Basic stats tab
            self.status_label.hide()
            self.left_dropdown_v.show()
            self.left_dropdown_c.show()
            self.right_dropdown_v.show()
            self.right_dropdown_c.show()
            self.chart_view.show()
            # show sim controls
            self.sim_left_dropdown_v.show()
            self.sim_left_dropdown_c.show()
            self.sim_right_dropdown_v.show()
            self.sim_right_dropdown_c.show()
            self.sim_left_hide_cb.show()
            self.sim_left_wheelie_cb.show()
            self.sim_left_smt_cb.show()
            self.sim_left_ssmt_cb.show()
            self.sim_right_hide_cb.show()
            self.sim_right_wheelie_cb.show()
            self.sim_right_smt_cb.show()
            self.sim_right_ssmt_cb.show()
            self.sim_type_dropdown.show()
            self.sim_diff_checkbox.show()
            self.sim_export_button.show()
            self.sim_widget.show()
            self.sim_status_label.hide()
        else:
            # ensure the File tab is selected and show the status message
            self.tabs.setCurrentIndex(0)
            self.status_label.show()
            self.left_dropdown_v.hide()
            self.left_dropdown_c.hide()
            self.right_dropdown_v.hide()
            self.right_dropdown_c.hide()
            self.chart_view.hide()
            # hide sim controls
            self.sim_left_dropdown_v.hide()
            self.sim_left_dropdown_c.hide()
            self.sim_right_dropdown_v.hide()
            self.sim_right_dropdown_c.hide()
            self.sim_left_hide_cb.hide()
            self.sim_left_wheelie_cb.hide()
            self.sim_left_smt_cb.hide()
            self.sim_left_ssmt_cb.hide()
            self.sim_right_hide_cb.hide()
            self.sim_right_wheelie_cb.hide()
            self.sim_right_smt_cb.hide()
            self.sim_right_ssmt_cb.hide()
            self.sim_type_dropdown.hide()
            self.sim_diff_checkbox.hide()
            self.sim_export_button.hide()
            self.sim_widget.hide()
            self.sim_status_label.show()

    def update_dropdowns(self, characters, vehicles):
        self.left_dropdown_v.clear()
        self.left_dropdown_c.clear()
        self.right_dropdown_v.clear()
        self.right_dropdown_c.clear()

        self.left_dropdown_v.addItems(vehicles)
        self.right_dropdown_v.addItems(vehicles)
        self.left_dropdown_c.addItems(characters)
        self.right_dropdown_c.addItems(characters)

        # Also update advanced tab combos
        self.advanced_left_dropdown_v.clear()
        self.advanced_right_dropdown_v.clear()
        self.advanced_left_dropdown_c.clear()
        self.advanced_right_dropdown_c.clear()

        self.advanced_left_dropdown_v.addItems(vehicles)
        self.advanced_right_dropdown_v.addItems(vehicles)
        self.advanced_left_dropdown_c.addItems(characters)
        self.advanced_right_dropdown_c.addItems(characters)

        # Also update simulation tab combos
        self.sim_left_dropdown_v.clear()
        self.sim_right_dropdown_v.clear()
        self.sim_left_dropdown_c.clear()
        self.sim_right_dropdown_c.clear()
        self.sim_left_dropdown_v.addItems(vehicles)
        self.sim_right_dropdown_v.addItems(vehicles)
        self.sim_left_dropdown_c.addItems(characters)
        self.sim_right_dropdown_c.addItems(characters)

    def update_chart(self, stats, names):
        self.chart_view.update_data(stats, names)

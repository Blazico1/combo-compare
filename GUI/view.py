from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit, QFileDialog, QMessageBox, QTabWidget, QComboBox, QLabel
from PyQt6.QtCore import Qt
from GUI.radarchartwidget import RadarChartWidget

CATEGORIES = ["Speed", "Mini-Turbo", "Drift", "Acceleration", "Off-Road", "Weight", "Handling"] 
        
class View(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Combo Compare")
        self.setGeometry(100, 100, 800, 600)

        self.tabs = QTabWidget()
        self.file_tab = QWidget()
        self.basic_stats_tab = QWidget()
        self.advanced_stats_tab = QWidget()

        self.tabs.addTab(self.file_tab, "File")
        self.tabs.addTab(self.basic_stats_tab, "Basic stats")
        self.tabs.addTab(self.advanced_stats_tab, "Advanced stats")

        self.init_file_tab()
        self.init_basic_stats_tab()

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

    def update_status(self, message):
        self.status_textbox.setText(message)

    def show_error_message(self, message):
        QMessageBox.critical(self, "Error", message)

    def get_file_path(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Select Common.szs file", "", "SZS Files (*.szs);;All Files (*)")
        return file_path

    def update_basic_stats_tab(self, available):
        if available:
            self.status_label.hide()
            self.left_dropdown_v.show()
            self.left_dropdown_c.show()	
            self.right_dropdown_v.show()
            self.right_dropdown_c.show()
            self.chart_view.show()
        else:
            self.status_label.show()
            self.left_dropdown_v.hide()
            self.left_dropdown_c.hide()
            self.right_dropdown_v.hide()
            self.right_dropdown_c.hide()
            self.chart_view.hide()

    def update_dropdowns(self, characters, vehicles):
        self.left_dropdown_v.clear()
        self.left_dropdown_c.clear()
        self.right_dropdown_v.clear()
        self.right_dropdown_c.clear()

        self.left_dropdown_v.addItems(vehicles)
        self.right_dropdown_v.addItems(vehicles)
        self.left_dropdown_c.addItems(characters)
        self.right_dropdown_c.addItems(characters)


    def update_chart(self, stats, names):
        self.chart_view.update_data(stats, names)
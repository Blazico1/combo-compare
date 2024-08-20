from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTextEdit, QFileDialog, QMessageBox, QTabWidget, QComboBox, QLabel

from GUI.radarchartwidget import RadarChartWidget

CATEGORIES = ["Speed", "Weight", "Acceleration", "Handling", "Drift", "Off-Road", "Mini-Turbo"]
        
class View(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Stats GUI")
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
        layout = QVBoxLayout()

        self.status_label = QLabel("Please select a Common.szs file to extract.")
        layout.addWidget(self.status_label)

        self.left_dropdown_v = QComboBox()
        self.left_dropdown_c = QComboBox()
        self.right_dropdown_v = QComboBox()
        self.right_dropdown_c = QComboBox()

        layout.addWidget(self.left_dropdown_v)
        layout.addWidget(self.left_dropdown_c)
        layout.addWidget(self.right_dropdown_v)
        layout.addWidget(self.right_dropdown_c)

        self.chart_view = RadarChartWidget([], CATEGORIES, None, frame='polygon', show_legend=True, show_numbers=False)
        layout.addWidget(self.chart_view)

        self.basic_stats_tab.setLayout(layout)

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
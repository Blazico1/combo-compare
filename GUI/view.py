from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTextEdit, QFileDialog, QMessageBox, QTabWidget

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

    def update_status(self, message):
        self.status_textbox.setText(message)

    def show_error_message(self, message):
        QMessageBox.critical(self, "Error", message)

    def get_file_path(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Select Common.szs file", "", "SZS Files (*.szs);;All Files (*)")
        return file_path
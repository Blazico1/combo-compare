import sys
from PyQt6.QtWidgets import QApplication
from GUI.model import Model
from GUI.view import View
from GUI.controller import Controller

def main():
    app = QApplication(sys.argv)

    # Define the global stylesheet
    stylesheet = """
        QWidget {
            background-color: #2e2e2e;
            color: #ffffff;
        }
        QLabel {
            color: #ffffff;
        }
        QComboBox {
            background-color: #3e3e3e;
            color: #ffffff;
            border: 1px solid #00ffff;
        }
        QPushButton {
            background-color: #3e3e3e;
            color: #ffffff;
            border: 1px solid #00ffff;
        }
        QTabWidget::pane {
            border: 1px solid #00ffff;
        }
        QTabBar::tab {
            background: #3e3e3e;
            color: #ffffff;
            padding: 10px;
        }
        QTabBar::tab:selected {
            background: #00ffff;
            color: #2e2e2e;
        }
    """

    # Apply the stylesheet to the application
    app.setStyleSheet(stylesheet)

    model = Model()
    view = View()
    controller = Controller(model, view)

    view.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
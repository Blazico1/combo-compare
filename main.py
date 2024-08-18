import sys
from PyQt6.QtWidgets import QApplication
from GUI.model import Model
from GUI.view import View
from GUI.controller import Controller

def main():
    app = QApplication(sys.argv)

    model = Model()
    view = View()
    controller = Controller(model, view)

    view.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view

        self.view.choose_file_button.clicked.connect(self.choose_file)
        self.view.extract_files_button.clicked.connect(self.extract_files)

        self.update_status()

    def update_status(self):
        if self.model.check_files():
            self.view.update_status("kartParam.bin and driverParam.bin are present in the bins folder.")
        else:
            self.view.update_status("Please select a Common.szs file to extract.")

    def choose_file(self):
        file_path = self.view.get_file_path()
        if file_path:
            self.model.set_selected_file(file_path)
            self.view.update_status(f"Selected file: {file_path}")

    def extract_files(self):
        try:
            self.model.extract_files()
            self.update_status()
        except Exception as e:
            self.view.show_error_message(str(e))
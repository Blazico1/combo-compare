class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view

        self.view.choose_file_button.clicked.connect(self.choose_file)
        self.view.extract_files_button.clicked.connect(self.extract_files)
        self.view.left_dropdown_v.currentIndexChanged.connect(self.update_chart)
        self.view.left_dropdown_c.currentIndexChanged.connect(self.update_chart)
        self.view.right_dropdown_v.currentIndexChanged.connect(self.update_chart)
        self.view.right_dropdown_c.currentIndexChanged.connect(self.update_chart)

        self.update_status()
        self.populate_dropdowns()

    def update_status(self):
        if self.model.check_files():
            self.view.update_status("kartParam.bin and driverParam.bin are present in the bins folder.")
            self.view.update_basic_stats_tab(True)
        else:
            self.view.update_status("Please select a Common.szs file to extract.")
            self.view.update_basic_stats_tab(False)

    def choose_file(self):
        file_path = self.view.get_file_path()
        if file_path:
            self.model.set_selected_file(file_path)
            self.view.update_status(f"Selected file: {file_path}")

    def extract_files(self):
        try:
            self.model.extract_files()
            self.update_status()
            self.populate_dropdowns()
        except Exception as e:
            self.view.show_error_message(str(e))

    def populate_dropdowns(self):
        characters = self.model.get_characters()
        vehicles = self.model.get_vehicles()
        self.view.update_dropdowns(characters, vehicles)

    def update_chart(self):
        
        vehicle1 = self.view.left_dropdown_v.currentText()
        character1 = self.view.left_dropdown_c.currentText()
        
        vehicle2 = self.view.right_dropdown_v.currentText()
        character2 = self.view.right_dropdown_c.currentText()
    
        stats1 = self.model.get_basic_stats(vehicle1, character1)
        stats2 = self.model.get_basic_stats(vehicle2, character2)

        label1 = f"{vehicle1} + {character1}"
        label2 = f"{vehicle2} + {character2}"

        self.view.update_chart([stats1, stats2], [label1, label2])
        
        
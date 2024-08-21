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
        characters = ['Character', 'Baby Daisy', 'Baby Luigi', 'Baby Mario', 
                      'Baby Peach', 'Birdo', 'Bowser', 'Bowser Jr.', 'Daisy', 
                      'Diddy Kong', 'Donkey Kong', 'Dry Bones', 'Dry Bowser', 
                      'Funky Kong', 'King Boo', 'Koopa Troopa', 'Luigi', 
                      'Mario', 'Mii L', 'Mii M', 'Mii S', 'Peach', 'Rosalina', 
                      'Toad', 'Toadette', 'Waluigi', 'Wario', 'Yoshi']
        vehicles = ['Vehicle', 'Bit Bike', 'Blue Falcon', 'Booster Seat', 
                    'Bullet Bike', 'Cheep Charger', 'Classic Dragster', 
                    'Daytripper', 'Dolphin Dasher', 'Flame Flyer', 'Flame Runner', 
                    'Honeycoupe', 'Jet Bubble', 'Jetsetter', 'Mach Bike', 
                    'Magikruiser', 'Mini Beast', 'Offroader', 'Piranha Prowler', 
                    'Quacker', 'Shooting Star', 'Sneakster', 'Spear', 'Standard Bike L', 
                    'Standard Bike M', 'Standard Bike S', 'Standard Kart L', 'Standard Kart M', 
                    'Standard Kart S', 'Sugarscoot', 'Super Blooper', 'Tiny Titan', 'Wild Wing', 
                    'Wario Bike', 'Zip Zip']
        self.view.update_dropdowns(characters, vehicles)

    def update_chart(self):
        
        vehicle1 = self.view.left_dropdown_v.currentText()
        character1 = self.view.left_dropdown_c.currentText()
        
        vehicle2 = self.view.right_dropdown_v.currentText()
        character2 = self.view.right_dropdown_c.currentText()
    
        stats1 = self.model.get_basic_stats(vehicle1, character1)
        stats2 = self.model.get_basic_stats(vehicle2, character2)

        if vehicle1 == "Vehicle":
            if character1 == "Character":
                label1 = "No selection"
            else:
                label1 = character1
        else:
            if character1 == "Character":
                label1 = vehicle1
            else:
                label1 = f"{vehicle1} + {character1}"

        if vehicle2 == "Vehicle":
            if character2 == "Character":
                label2 = "No selection"
            else:
                label2 = character2
        else:
            if character2 == "Character":
                label2 = vehicle2
            else:
                label2 = f"{vehicle2} + {character2}"
        
        self.view.update_chart([stats1, stats2], [label1, label2])
        
        
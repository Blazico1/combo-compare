import os
from GUI.model import global_vehicles, global_characters

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

        # Advanced tab connections
        self.view.advanced_left_dropdown_v.currentIndexChanged.connect(self.update_advanced)
        self.view.advanced_left_dropdown_c.currentIndexChanged.connect(self.update_advanced)
        self.view.advanced_right_dropdown_v.currentIndexChanged.connect(self.update_advanced)
        self.view.advanced_right_dropdown_c.currentIndexChanged.connect(self.update_advanced)

        # Simulation tab connections
        self.view.sim_left_dropdown_v.currentIndexChanged.connect(self.update_simulation)
        self.view.sim_left_dropdown_c.currentIndexChanged.connect(self.update_simulation)
        self.view.sim_right_dropdown_v.currentIndexChanged.connect(self.update_simulation)
        self.view.sim_right_dropdown_c.currentIndexChanged.connect(self.update_simulation)

        # Simulation settings connections
        self.view.sim_type_dropdown.currentIndexChanged.connect(self.update_simulation)
        self.view.sim_diff_checkbox.toggled.connect(self.update_simulation)
        self.view.sim_left_wheelie_cb.toggled.connect(self.update_simulation)
        self.view.sim_right_wheelie_cb.toggled.connect(self.update_simulation)
        self.view.sim_left_ssmt_cb.toggled.connect(self.update_simulation)
        self.view.sim_right_ssmt_cb.toggled.connect(self.update_simulation)
        self.view.sim_export_button.clicked.connect(lambda: self.view.show_error_message('Export not implemented'))

        self.update_status()
        self.populate_dropdowns()

    def update_status(self):
        if os.path.exists('kartParam.bin') and os.path.exists('driverParam.bin'):
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
            # Update dropdowns with parsed names
            vehicle_names = sorted([v.name for v in global_vehicles])
            character_names = sorted([c.name for c in global_characters])
            self.view.update_dropdowns(character_names, vehicle_names)
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
                    'Magikruiser', 'Mini Beast', 'Offroader', 'Phantom', 'Piranha Prowler', 
                    'Quacker', 'Shooting Star', 'Sneakster', 'Spear', 'Sprinter', 'Standard Bike L', 
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

        # Turn dicts into lists
        keys = ["speed", "mini_turbo", "drift", "acceleration", "offroad", "weight", "handling"]
        stats1 = [stats1[k] for k in keys]
        stats2 = [stats2[k] for k in keys]
        self.view.update_chart([stats1, stats2], [label1, label2])

        # Also update advanced stats panel with raw per-field values
        # Request advanced stats if either a vehicle or character (or both) is selected
        adv1 = self.model.get_advanced_stats(vehicle1, character1) if (vehicle1 != 'Vehicle' or character1 != 'Character') else {}
        adv2 = self.model.get_advanced_stats(vehicle2, character2) if (vehicle2 != 'Vehicle' or character2 != 'Character') else {}
        self.view.update_advanced_stats(adv1, adv2)

        # Sync advanced combos to basic selections
        self.view.advanced_left_dropdown_v.blockSignals(True)
        self.view.advanced_left_dropdown_c.blockSignals(True)
        self.view.advanced_right_dropdown_v.blockSignals(True)
        self.view.advanced_right_dropdown_c.blockSignals(True)
        self.view.advanced_left_dropdown_v.setCurrentText(vehicle1)
        self.view.advanced_left_dropdown_c.setCurrentText(character1)
        self.view.advanced_right_dropdown_v.setCurrentText(vehicle2)
        self.view.advanced_right_dropdown_c.setCurrentText(character2)
        self.view.advanced_left_dropdown_v.blockSignals(False)
        self.view.advanced_left_dropdown_c.blockSignals(False)
        self.view.advanced_right_dropdown_v.blockSignals(False)
        self.view.advanced_right_dropdown_c.blockSignals(False)

        # Sync simulation combos to basic selections
        self.view.sim_left_dropdown_v.blockSignals(True)
        self.view.sim_left_dropdown_c.blockSignals(True)
        self.view.sim_right_dropdown_v.blockSignals(True)
        self.view.sim_right_dropdown_c.blockSignals(True)
        self.view.sim_left_dropdown_v.setCurrentText(vehicle1)
        self.view.sim_left_dropdown_c.setCurrentText(character1)
        self.view.sim_right_dropdown_v.setCurrentText(vehicle2)
        self.view.sim_right_dropdown_c.setCurrentText(character2)
        self.view.sim_left_dropdown_v.blockSignals(False)
        self.view.sim_left_dropdown_c.blockSignals(False)
        self.view.sim_right_dropdown_v.blockSignals(False)
        self.view.sim_right_dropdown_c.blockSignals(False)


    def update_simulation(self):
        # Get simulation tab selections
        left_vehicle = self.view.sim_left_dropdown_v.currentText()
        left_character = self.view.sim_left_dropdown_c.currentText()
        right_vehicle = self.view.sim_right_dropdown_v.currentText()
        right_character = self.view.sim_right_dropdown_c.currentText()

        # Sync basic combos to simulation selections
        self.view.left_dropdown_v.blockSignals(True)
        self.view.left_dropdown_c.blockSignals(True)
        self.view.right_dropdown_v.blockSignals(True)
        self.view.right_dropdown_c.blockSignals(True)
        self.view.left_dropdown_v.setCurrentText(left_vehicle)
        self.view.left_dropdown_c.setCurrentText(left_character)
        self.view.right_dropdown_v.setCurrentText(right_vehicle)
        self.view.right_dropdown_c.setCurrentText(right_character)
        self.view.left_dropdown_v.blockSignals(False)
        self.view.left_dropdown_c.blockSignals(False)
        self.view.right_dropdown_v.blockSignals(False)
        self.view.right_dropdown_c.blockSignals(False)

        # Sync advanced combos to simulation selections
        self.view.advanced_left_dropdown_v.blockSignals(True)
        self.view.advanced_left_dropdown_c.blockSignals(True)
        self.view.advanced_right_dropdown_v.blockSignals(True)
        self.view.advanced_right_dropdown_c.blockSignals(True)
        self.view.advanced_left_dropdown_v.setCurrentText(left_vehicle)
        self.view.advanced_left_dropdown_c.setCurrentText(left_character)
        self.view.advanced_right_dropdown_v.setCurrentText(right_vehicle)
        self.view.advanced_right_dropdown_c.setCurrentText(right_character)
        self.view.advanced_left_dropdown_v.blockSignals(False)
        self.view.advanced_left_dropdown_c.blockSignals(False)
        self.view.advanced_right_dropdown_v.blockSignals(False)
        self.view.advanced_right_dropdown_c.blockSignals(False)

        # After syncing without signals, manually refresh the shared UI
        # so the Basic stats tab and advanced stats reflect the simulation selection.
        self.update_chart()

        # Get checkbox states
        left_wheelie = self.view.sim_left_wheelie_cb.isChecked()
        left_ssmt = self.view.sim_left_ssmt_cb.isChecked()
        right_wheelie = self.view.sim_right_wheelie_cb.isChecked()
        right_ssmt = self.view.sim_right_ssmt_cb.isChecked()

        # Simulate acceleration
        if left_vehicle != 'Vehicle' and left_character != 'Character':
            left_result = self.model.simulate_accel(left_vehicle, left_character, wheelie=left_wheelie, ssmt=left_ssmt)
            if left_result:
                left_speeds, left_distances = left_result
            else:
                left_speeds, left_distances = [], []
        else:
            left_speeds, left_distances = [], []

        if right_vehicle != 'Vehicle' and right_character != 'Character':
            right_result = self.model.simulate_accel(right_vehicle, right_character, wheelie=right_wheelie, ssmt=right_ssmt)
            if right_result:
                right_speeds, right_distances = right_result
            else:
                right_speeds, right_distances = [], []
        else:
            right_speeds, right_distances = [], []

        # Update time plot
        self.view.sim_widget.update_data(left_speeds, left_distances, right_speeds, right_distances, (f"{left_vehicle} + {left_character}", f"{right_vehicle} + {right_character}"))


    def update_advanced(self):
        left_vehicle = self.view.advanced_left_dropdown_v.currentText()
        left_character = self.view.advanced_left_dropdown_c.currentText()
        right_vehicle = self.view.advanced_right_dropdown_v.currentText()
        right_character = self.view.advanced_right_dropdown_c.currentText()
        adv1 = self.model.get_advanced_stats(left_vehicle, left_character) if (left_vehicle != 'Vehicle' or left_character != 'Character') else {}
        adv2 = self.model.get_advanced_stats(right_vehicle, right_character) if (right_vehicle != 'Vehicle' or right_character != 'Character') else {}
        self.view.update_advanced_stats(adv1, adv2)

        # Sync basic combos to advanced selections
        self.view.left_dropdown_v.blockSignals(True)
        self.view.left_dropdown_c.blockSignals(True)
        self.view.right_dropdown_v.blockSignals(True)
        self.view.right_dropdown_c.blockSignals(True)
        self.view.left_dropdown_v.setCurrentText(left_vehicle)
        self.view.left_dropdown_c.setCurrentText(left_character)
        self.view.right_dropdown_v.setCurrentText(right_vehicle)
        self.view.right_dropdown_c.setCurrentText(right_character)
        self.view.left_dropdown_v.blockSignals(False)
        self.view.left_dropdown_c.blockSignals(False)
        self.view.right_dropdown_v.blockSignals(False)
        self.view.right_dropdown_c.blockSignals(False)
        # After syncing without signals, manually refresh the shared UI
        # so the Basic stats tab reflects the advanced selection.
        self.update_chart()
        
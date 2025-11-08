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
        self.view.sim_left_smt_cb.toggled.connect(self.update_simulation)
        self.view.sim_right_smt_cb.toggled.connect(self.update_simulation)
        self.view.sim_left_ssmt_cb.toggled.connect(self.update_simulation)
        self.view.sim_right_ssmt_cb.toggled.connect(self.update_simulation)
        self.view.sim_left_hide_cb.toggled.connect(self.update_simulation)
        self.view.sim_right_hide_cb.toggled.connect(self.update_simulation)
        self.view.sim_time_slider.valueChanged.connect(self.update_simulation_time)
        self.view.sim_export_button.clicked.connect(lambda: self.view.show_error_message('Export not implemented'))

        self.update_status()
        self.populate_dropdowns()

    # Helper methods for code reuse
    def get_combo_label(self, vehicle, character):
        """Generate a display label for a vehicle/character combo."""
        if vehicle == "Vehicle":
            if character == "Character":
                return "No selection"
            else:
                return character
        else:
            if character == "Character":
                return vehicle
            else:
                return f"{vehicle} + {character}"

    def is_valid_combo(self, vehicle, character):
        """Check if vehicle/character combo is valid."""
        return vehicle != 'Vehicle' and character != 'Character'

    def block_dropdown_signals(self, prefix):
        """Block signals for dropdowns with given prefix."""
        getattr(self.view, f"{prefix}_dropdown_v").blockSignals(True)
        getattr(self.view, f"{prefix}_dropdown_c").blockSignals(True)

    def unblock_dropdown_signals(self, prefix):
        """Unblock signals for dropdowns with given prefix."""
        getattr(self.view, f"{prefix}_dropdown_v").blockSignals(False)
        getattr(self.view, f"{prefix}_dropdown_c").blockSignals(False)

    def sync_dropdown_pair(self, source_prefix, target_prefix,
                          vehicle, character):
        """Sync dropdown values from source to target."""
        self.block_dropdown_signals(target_prefix)
        getattr(self.view, f"{target_prefix}_dropdown_v") \
            .setCurrentText(vehicle)
        getattr(self.view, f"{target_prefix}_dropdown_c") \
            .setCurrentText(character)
        self.unblock_dropdown_signals(target_prefix)

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

        label1 = self.get_combo_label(vehicle1, character1)
        label2 = self.get_combo_label(vehicle2, character2)

        # Turn dicts into lists
        keys = ["speed", "mini_turbo", "drift", "acceleration", "offroad", "weight", "handling"]
        stats1 = [stats1[k] for k in keys]
        stats2 = [stats2[k] for k in keys]
        self.view.update_chart([stats1, stats2], [label1, label2])

        # Also update advanced stats panel with raw per-field values
        # Request advanced stats if either a vehicle or character (or both) is selected
        adv1 = self.model.get_advanced_stats(vehicle1, character1) \
            if self.is_valid_combo(vehicle1, character1) else {}
        adv2 = self.model.get_advanced_stats(vehicle2, character2) \
            if self.is_valid_combo(vehicle2, character2) else {}
        self.view.update_advanced_stats(adv1, adv2)

        # Sync advanced combos to basic selections
        self.sync_dropdown_pair("left", "advanced_left", vehicle1, character1)
        self.sync_dropdown_pair("right", "advanced_right", vehicle2, character2)

        # Sync simulation combos to basic selections
        self.sync_dropdown_pair("left", "sim_left", vehicle1, character1)
        self.sync_dropdown_pair("right", "sim_right", vehicle2, character2)

        # Update simulation UI to reflect the synced selections
        self.update_simulation_ui()


    def update_simulation(self):
        # Get simulation tab selections
        left_vehicle = self.view.sim_left_dropdown_v.currentText()
        left_character = self.view.sim_left_dropdown_c.currentText()
        right_vehicle = self.view.sim_right_dropdown_v.currentText()
        right_character = self.view.sim_right_dropdown_c.currentText()

        # Sync basic combos to simulation selections
        self.sync_dropdown_pair("sim_left", "left", left_vehicle, left_character)
        self.sync_dropdown_pair("sim_right", "right", right_vehicle, right_character)

        # Sync advanced combos to simulation selections
        self.sync_dropdown_pair("sim_left", "advanced_left", left_vehicle, left_character)
        self.sync_dropdown_pair("sim_right", "advanced_right", right_vehicle, right_character)

        # After syncing without signals, manually refresh the shared UI
        # so the Basic stats tab and advanced stats reflect the simulation selection.
        self.update_chart()

        # Update simulation-specific UI (timeplot and stats labels)
        self.update_simulation_ui()


    def update_simulation_ui(self):
        # Get simulation tab selections
        left_vehicle = self.view.sim_left_dropdown_v.currentText()
        left_character = self.view.sim_left_dropdown_c.currentText()
        right_vehicle = self.view.sim_right_dropdown_v.currentText()
        right_character = self.view.sim_right_dropdown_c.currentText()

        # Get simulation type
        sim_type = self.view.sim_type_dropdown.currentText()
        sim_time = self.view.sim_time_slider.value()

        # Get checkbox states (only consider logically enabled checkboxes)
        left_wheelie = self.view.sim_left_wheelie_cb.isChecked()
        left_ssmt = self.view.sim_left_ssmt_cb.isChecked() and sim_type == "Acceleration"  # SSMT only for acceleration
        left_smt = self.view.sim_left_smt_cb.isChecked() and sim_type == "Mini-turbo"  # SMT only for mini-turbo
        right_wheelie = self.view.sim_right_wheelie_cb.isChecked()
        right_ssmt = self.view.sim_right_ssmt_cb.isChecked() and sim_type == "Acceleration"  # SSMT only for acceleration
        right_smt = self.view.sim_right_smt_cb.isChecked() and sim_type == "Mini-turbo"  # SMT only for mini-turbo

        # Simulate based on type
        if sim_type == "Acceleration":
            if left_vehicle != 'Vehicle' and left_character != 'Character':
                left_result = self.model.simulate_accel(left_vehicle, left_character, total_time=sim_time, wheelie=left_wheelie, ssmt=left_ssmt)
                if left_result:
                    left_speeds, left_distances = left_result
                else:
                    left_speeds, left_distances = [], []
            else:
                left_speeds, left_distances = [], []

            if right_vehicle != 'Vehicle' and right_character != 'Character':
                right_result = self.model.simulate_accel(right_vehicle, right_character, total_time=sim_time, wheelie=right_wheelie, ssmt=right_ssmt)
                if right_result:
                    right_speeds, right_distances = right_result
                else:
                    right_speeds, right_distances = [], []
            else:
                right_speeds, right_distances = [], []
        else:  # "Mini-turbo"
            if left_vehicle != 'Vehicle' and left_character != 'Character':
                left_result = self.model.simulate_mini_turbo(left_vehicle, left_character, post_time=sim_time, wheelie=left_wheelie, SMT=left_smt)
                if left_result:
                    left_speeds, left_distances = left_result
                else:
                    left_speeds, left_distances = [], []
            else:
                left_speeds, left_distances = [], []

            if right_vehicle != 'Vehicle' and right_character != 'Character':
                right_result = self.model.simulate_mini_turbo(right_vehicle, right_character, post_time=sim_time, wheelie=right_wheelie, SMT=right_smt)
                if right_result:
                    right_speeds, right_distances = right_result
                else:
                    right_speeds, right_distances = [], []
            else:
                right_speeds, right_distances = [], []

        # Update time plot
        left_selected = left_vehicle != 'Vehicle' and \
            left_character != 'Character'
        right_selected = right_vehicle != 'Vehicle' and \
            right_character != 'Character'
        diff_mode = self.view.sim_diff_checkbox.isChecked()
        left_hidden = self.view.sim_left_hide_cb.isChecked()
        right_hidden = self.view.sim_right_hide_cb.isChecked()
        self.view.sim_widget.update_data(
            left_speeds, left_distances, right_speeds, right_distances,
            left_selected, right_selected, diff_mode=diff_mode,
            left_hidden=left_hidden, right_hidden=right_hidden)

        # Update stats display
        left_stats = self.model.get_advanced_stats(left_vehicle,
                                                   left_character) \
            if left_selected else {}
        right_stats = self.model.get_advanced_stats(right_vehicle,
                                                    right_character) \
            if right_selected else {}
        self.view.update_sim_stats(left_stats, right_stats, sim_type)

        # Update UI element enabled states based on current selections
        left_valid = self.is_valid_combo(left_vehicle, left_character)
        right_valid = self.is_valid_combo(right_vehicle, right_character)
        has_valid_combo = left_valid or right_valid
        has_both_valid = left_valid and right_valid

        # Define stylesheets for enabled/disabled checkboxes
        normal_style = """
            QCheckBox {
                color: #ffffff;
            }
            QCheckBox::indicator {
                background-color: #3e3e3e;
                border: 1px solid #00ffff;
            }
            QCheckBox::indicator:checked {
                background-color: #00ffff;
            }
        """
        disabled_style = """
            QCheckBox {
                color: #888888;
            }
            QCheckBox::indicator {
                background-color: #cccccc;
                border: 1px solid #888888;
            }
            QCheckBox::indicator:checked {
                background-color: #888888;
            }
        """

        # SMT checkboxes: enabled only for mini-turbo
        smt_enabled = sim_type == "Mini-turbo"
        self.view.sim_left_smt_cb.setEnabled(True)
        self.view.sim_right_smt_cb.setEnabled(True)
        style = normal_style if smt_enabled else disabled_style
        self.view.sim_left_smt_cb.setStyleSheet(style)
        self.view.sim_right_smt_cb.setStyleSheet(style)
        if not smt_enabled:
            self.view.sim_left_smt_cb.setChecked(False)
            self.view.sim_right_smt_cb.setChecked(False)

        # SSMT checkboxes: enabled only for acceleration
        ssmt_enabled = sim_type == "Acceleration"
        self.view.sim_left_ssmt_cb.setEnabled(True)
        self.view.sim_right_ssmt_cb.setEnabled(True)
        style = normal_style if ssmt_enabled else disabled_style
        self.view.sim_left_ssmt_cb.setStyleSheet(style)
        self.view.sim_right_ssmt_cb.setStyleSheet(style)
        if not ssmt_enabled:
            self.view.sim_left_ssmt_cb.setChecked(False)
            self.view.sim_right_ssmt_cb.setChecked(False)

        # Differential mode: enabled only when both combos are valid
        self.view.sim_diff_checkbox.setEnabled(True)
        style = normal_style if has_both_valid else disabled_style
        self.view.sim_diff_checkbox.setStyleSheet(style)
        if not has_both_valid:
            self.view.sim_diff_checkbox.setChecked(False)

        # Hide checkboxes: disabled when differential mode is active
        hide_enabled = not diff_mode
        style = normal_style if hide_enabled else disabled_style
        self.view.sim_left_hide_cb.setEnabled(hide_enabled)
        self.view.sim_right_hide_cb.setEnabled(hide_enabled)
        self.view.sim_left_hide_cb.setStyleSheet(style)
        self.view.sim_right_hide_cb.setStyleSheet(style)
        if not hide_enabled:
            self.view.sim_left_hide_cb.setChecked(False)
            self.view.sim_right_hide_cb.setChecked(False)

        # Export button: enabled only when there's at least one valid combo
        self.view.sim_export_button.setEnabled(has_valid_combo)

    def update_simulation_time(self, value):
        self.view.sim_time_value_label.setText(str(value))
        self.update_simulation()

    def update_advanced(self):
        left_vehicle = self.view.advanced_left_dropdown_v.currentText()
        left_character = self.view.advanced_left_dropdown_c.currentText()
        right_vehicle = self.view.advanced_right_dropdown_v.currentText()
        right_character = self.view.advanced_right_dropdown_c.currentText()
        adv1 = self.model.get_advanced_stats(left_vehicle, left_character) \
            if self.is_valid_combo(left_vehicle, left_character) else {}
        adv2 = self.model.get_advanced_stats(right_vehicle, right_character) \
            if self.is_valid_combo(right_vehicle, right_character) else {}
        self.view.update_advanced_stats(adv1, adv2)

        # Sync basic combos to advanced selections
        self.sync_dropdown_pair("advanced_left", "left", left_vehicle,
                                left_character)
        self.sync_dropdown_pair("advanced_right", "right", right_vehicle,
                                right_character)
        # After syncing without signals, manually refresh the shared UI
        # so the Basic stats tab reflects the advanced selection.
        self.update_chart()
        
import os
from logic.u8archive import U8Archive
from logic.stats import parse_stats, normalise_stats, set_names

class Model:
    def __init__(self):
        self.selected_file = None

    def check_files(self):
        # Return True if both files exist, False otherwise
        if os.path.exists('bins/kartParam.bin') and os.path.exists('bins/driverParam.bin'):
            return True
        return False

    def set_selected_file(self, file_path):
        self.selected_file = file_path

    def extract_files(self):
        if not self.selected_file:
            raise Exception("No file selected")
        
        archive = U8Archive(self.selected_file)
        archive.extract_file('kartParam.bin')
        archive.extract_file('driverParam.bin')

    def get_basic_stats(self, vehicle:str, character:str) -> list:
        # Return stats for the given character or vehicle
        vehicles = parse_stats('bins/kartParam.bin')
        set_names(vehicles, False)
        characters = parse_stats('bins/driverParam.bin')
        set_names(characters, True)
        vehicle_stats = None
        character_stats = None

        for v in vehicles:
            if v.name == vehicle:
                vehicle_stats = v.get_basic_stats()
                break

        for c in characters:
            if c.name == character:
                character_stats = c.get_basic_stats()
                break
        
        if vehicle_stats is None and character_stats is None:
            return [0] * 7
        elif vehicle_stats is None:
            norm_stats = normalise_stats(character_stats, characters=characters)
        elif character_stats is None:
            norm_stats = normalise_stats(vehicle_stats, vehicles=vehicles)
        else:
            stats = [v + c for v, c in zip(vehicle_stats, character_stats)]
            norm_stats = normalise_stats(stats, vehicles=vehicles, characters=characters)

        return norm_stats
        
        





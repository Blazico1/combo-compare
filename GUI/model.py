import os
from logic.u8archive import U8Archive
from logic.stats import parse_stats, normalise_stats, set_names, EMPTY_DICT
import logic.simulation as sim

# Global objects for parsed stats, loaded once when files are available
global_vehicles = None
global_characters = None

def load_global_stats():
    """Parse the two param files and cache globally.

    This should be called once after extraction or whenever the underlying
    bin files change. Keeping the parsed objects globally lets all code reuse them
    without reparsing.
    """
    global global_vehicles, global_characters
    if global_vehicles is not None and global_characters is not None:
        return  # Already loaded

    # Attempt to parse the bins; don't gate behavior on file checks here.
    # If parsing fails (missing files or parse error) we gracefully set
    # the cached values to None and allow the controller/view to handle
    # the user-visible gating.
    vehicles = None
    characters = None
    try:
        vehicles = parse_stats('kartParam.bin')
        set_names(vehicles, False)
    except Exception:
        vehicles = None

    try:
        characters = parse_stats('driverParam.bin')
        set_names(characters, True)
    except Exception:
        characters = None

    global_vehicles = vehicles
    global_characters = characters

class Model:
    def __init__(self):
        self.selected_file = None
        load_global_stats()

    def set_selected_file(self, file_path):
        self.selected_file = file_path

    def extract_files(self):
        if not self.selected_file:
            raise Exception("No file selected")
        
        archive = U8Archive(self.selected_file)
        archive.extract_file('kartParam.bin')
        archive.extract_file('driverParam.bin')
        # Parse and cache the stats globally after extraction
        load_global_stats()
        # Check if loading succeeded
        if global_vehicles is None or global_characters is None:
            raise Exception("Failed to load stats from extracted files.")

    def get_basic_stats(self, vehicle: str, character: str) -> list:
        # Return stats for the given character or vehicle
        # Stats are globally loaded; assume available since tabs are gated
        vehicles = global_vehicles
        characters = global_characters
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
            return EMPTY_DICT()
        elif vehicle_stats is None:
            norm_stats = normalise_stats(c_stats=character_stats, characters=characters)
        elif character_stats is None:
            norm_stats = normalise_stats(v_stats=vehicle_stats, vehicles=vehicles)
        else:
            norm_stats = normalise_stats(v_stats=vehicle_stats, c_stats=character_stats, vehicles=vehicles, characters=characters)

        return norm_stats

    def simulate_accel(self, vehicle: str, character: str, total_time: float = 10.0, wheelie: bool = False, ssmt: bool = False):
        """Wrapper that delegates simulation to the logic layer (logic.simulation).

        Keeps the Model API stable while moving logic out of the GUI module.
        """
        # Use globally cached StatsBase objects and pass basic-stats dicts into the
        # pure simulation function.
        v_unit = next((v for v in global_vehicles if v.name == vehicle), None)
        c_unit = next((c for c in global_characters if c.name == character), None)

        vstats = v_unit.get_basic_stats() if v_unit else None
        cstats = c_unit.get_basic_stats() if c_unit else None

        return sim.simulate_accel(vstats, cstats, wheelie=wheelie, ssmt=ssmt, time=total_time)

    def simulate_mini_turbo(self, vehicle: str, character: str, post_time: float = 3.0):
        """Wrapper that delegates post-release simulation to logic.simulation.

        The initial speed used for the post-release simulation is the combo's
        drifting top speed (vehicle.speed_in_turn + character.speed_in_turn).
        """
        v_unit = next((v for v in global_vehicles if v.name == vehicle), None)
        c_unit = next((c for c in global_characters if c.name == character), None)

        # Note: simulation expects basic-stats dicts; use get_basic_stats()
        vstats = v_unit.get_basic_stats() if v_unit else None
        cstats = c_unit.get_basic_stats() if c_unit else None

        return sim.simulate_mini_turbo(vstats, cstats, time=post_time)
    
    def get_advanced_stats(self, vehicle: str, character: str) -> dict:
        """Return advanced stats from stored attributes, summed for combo."""
        v_unit = next((v for v in global_vehicles if v.name == vehicle), None)
        c_unit = next(
            (c for c in global_characters if c.name == character), None)

        v_dict = v_unit.get_advanced_stats() if v_unit else {}
        c_dict = c_unit.get_advanced_stats() if c_unit else {}

        out = {}
        all_keys = set(v_dict.keys()) | set(c_dict.keys())
        for key in all_keys:
            v_val = v_dict.get(key)
            c_val = c_dict.get(key)
            if key in ('weight_class', 'num_tires', 'drift_type'):
                # Special: do not sum, use common value or vehicle stats if differ
                if v_val is not None and c_val is not None:
                    out[key] = v_val
                else:
                    out[key] = v_val if v_val is not None else c_val
            else:
                # Sum if both present, else use the available one
                if v_val is not None and c_val is not None:
                    out[key] = v_val + c_val
                else:
                    out[key] = v_val if v_val is not None else c_val

        return out
        
        





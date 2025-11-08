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

    # Helper methods for code reuse
    def _find_vehicle_unit(self, name):
        """Find a vehicle unit by name."""
        return next((v for v in global_vehicles if v.name == name), None)

    def _find_character_unit(self, name):
        """Find a character unit by name."""
        return next((c for c in global_characters if c.name == name), None)

    def _get_unit_stats(self, unit):
        """Get basic stats from a unit, returning None if unit is None."""
        return unit.get_basic_stats() if unit else None

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
        vehicle_stats = self._get_unit_stats(self._find_vehicle_unit(vehicle))
        character_stats = self._get_unit_stats(self._find_character_unit(character))
        
        if vehicle_stats is None and character_stats is None:
            return EMPTY_DICT()
        elif vehicle_stats is None:
            norm_stats = normalise_stats(c_stats=character_stats, characters=global_characters)
        elif character_stats is None:
            norm_stats = normalise_stats(v_stats=vehicle_stats, vehicles=global_vehicles)
        else:
            norm_stats = normalise_stats(v_stats=vehicle_stats, c_stats=character_stats, 
                                       vehicles=global_vehicles, characters=global_characters)

        return norm_stats

    def simulate_accel(self, vehicle: str, character: str, total_time: float = 10.0, wheelie: bool = False, ssmt: bool = False):
        """Wrapper that delegates simulation to the logic layer (logic.simulation).

        Keeps the Model API stable while moving logic out of the GUI module.
        Returns (speeds, distances) in units per frame (u/f).
        """
        # Use globally cached StatsBase objects and pass basic-stats dicts into the
        # pure simulation function.
        vstats = self._get_unit_stats(self._find_vehicle_unit(vehicle))
        cstats = self._get_unit_stats(self._find_character_unit(character))

        return sim.simulate_accel(vstats, cstats, wheelie=wheelie, ssmt=ssmt, time=total_time)

    def simulate_mini_turbo(self, vehicle: str, character: str, post_time: float = 3.0, wheelie: bool = False, SMT: bool = False):
        """Wrapper that delegates post-release simulation to logic.simulation.

        The initial speed used for the post-release simulation is the combo's
        drifting top speed (vehicle.speed_in_turn + character.speed_in_turn).
        Returns (speeds, distances) in units per frame (u/f).
        """
        # Note: simulation expects basic-stats dicts; use get_basic_stats()
        vstats = self._get_unit_stats(self._find_vehicle_unit(vehicle))
        cstats = self._get_unit_stats(self._find_character_unit(character))

        return sim.simulate_mini_turbo(vstats, cstats, wheelie=wheelie, SMT=SMT, time=post_time)
    
    def get_advanced_stats(self, vehicle: str, character: str) -> dict:
        """Return advanced stats from stored attributes, summed for combo."""
        v_unit = self._find_vehicle_unit(vehicle)
        c_unit = self._find_character_unit(character)

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
        
        





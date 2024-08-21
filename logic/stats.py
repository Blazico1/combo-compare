import struct
from logic.id import id_to_vehicle, id_to_driver

class StatsBase:
    '''
    Class to store the stats of a vehicle or character
    '''

    def __init__(self, id, num_tires, drift_type, weight_class, unknown, weight, bump_deviation, speed, speed_in_turn, tilt,
                 std_accel_a0, std_accel_a1, std_accel_a2, std_accel_a3, std_accel_t1, std_accel_t2, std_accel_t3,
                 drift_accel_a0, drift_accel_a1, drift_accel_t1, manual_handling, auto_handling, handling_reactivity,
                 manual_drift, auto_drift, drift_reactivity, outside_drift_angle, outside_drift_decrement, mini_turbo_duration,
                 speed_multipliers, rotation_multipliers, rotating_items_z_radius, rotating_items_x_radius,
                 rotating_items_y_distance, rotating_items_z_distance, max_normal_accel, mega_mushroom_scale, tire_distance):
        self.name = None
        self.id = id
        self.num_tires = num_tires
        self.drift_type = drift_type
        self.weight_class = weight_class
        self.unknown = unknown
        self.weight = weight
        self.bump_deviation = bump_deviation
        self.speed = speed
        self.speed_in_turn = speed_in_turn
        self.tilt = tilt
        self.std_accel_a0 = std_accel_a0
        self.std_accel_a1 = std_accel_a1
        self.std_accel_a2 = std_accel_a2
        self.std_accel_a3 = std_accel_a3
        self.std_accel_t1 = std_accel_t1
        self.std_accel_t2 = std_accel_t2
        self.std_accel_t3 = std_accel_t3
        self.drift_accel_a0 = drift_accel_a0
        self.drift_accel_a1 = drift_accel_a1
        self.drift_accel_t1 = drift_accel_t1
        self.manual_handling = manual_handling
        self.auto_handling = auto_handling
        self.handling_reactivity = handling_reactivity
        self.manual_drift = manual_drift
        self.auto_drift = auto_drift
        self.drift_reactivity = drift_reactivity
        self.outside_drift_angle = outside_drift_angle
        self.outside_drift_decrement = outside_drift_decrement
        self.mini_turbo_duration = mini_turbo_duration
        self.speed_multipliers = speed_multipliers
        self.rotation_multipliers = rotation_multipliers
        self.rotating_items_z_radius = rotating_items_z_radius
        self.rotating_items_x_radius = rotating_items_x_radius
        self.rotating_items_y_distance = rotating_items_y_distance
        self.rotating_items_z_distance = rotating_items_z_distance
        self.max_normal_accel = max_normal_accel
        self.mega_mushroom_scale = mega_mushroom_scale
        self.tire_distance = tire_distance

    def __repr__(self):
        return (f"StatsBase(name={self.name}, id={self.id:X}, num_tires={self.num_tires}, drift_type={self.drift_type}, "
                f"weight_class={self.weight_class}, weight={self.weight:.2f}, ...)")
    
    def is_vehicle(self):
        self.name = id_to_vehicle(self.id)
    
    def is_driver(self):
        self.name = id_to_driver(self.id)

    def get_basic_stats(self):
        speed = self.speed
        weight = self.weight
        accel = self.std_accel_a0
        handling = self.manual_handling
        drift = self.manual_drift
        offroad = self.speed_multipliers[3]
        mini_turbo = self.mini_turbo_duration

        return [speed, mini_turbo, drift, accel, offroad, weight, handling]


def normalise_stats(stats: list, vehicles = None, characters = None) -> list:
    '''
    Normalise the stats of the given vehicles and characters
    '''
    
    if vehicles is None and characters is None:
        raise ValueError("At least one of vehicles or characters must be provided")
    
    # Get the max stats for each category
    max_vehicle_stats = [0] * 7
    if vehicles is not None:
        for vehicle in vehicles:
            vstats = vehicle.get_basic_stats()
            for i in range(7):
                max_vehicle_stats[i] = max(max_vehicle_stats[i], vstats[i])

    max_character_stats = [0] * 7
    if characters is not None:
        for character in characters:
            cstats = character.get_basic_stats()
            for i in range(7):
                max_character_stats[i] = max(max_character_stats[i], cstats[i])
    
    max_totals = []
    for i in range(7):
        max_totals.append(max_vehicle_stats[i] + max_character_stats[i])
    
    # Raise an error if one of the max stats is 0
    if 0 in max_totals:
        raise ValueError("One of the max stats is 0")
    
    # Get the min stats for each category
    min_vehicle_stats = [float('inf')] * 7
    if vehicles is not None:
        for vehicle in vehicles:
            vstats = vehicle.get_basic_stats()
            for i in range(7):
                min_vehicle_stats[i] = min(min_vehicle_stats[i], vstats[i])
    else:
        min_vehicle_stats = [0] * 7

    min_character_stats = [float('inf')] * 7
    if characters is not None:
        for character in characters:
            cstats = character.get_basic_stats()
            for i in range(7):
                min_character_stats[i] = min(min_character_stats[i], cstats[i])
    else:
        min_character_stats = [0] * 7

    min_totals = []
    for i in range(7):
        min_totals.append(min_vehicle_stats[i] + min_character_stats[i])

    # Raise an error if one of the min stats is inf
    if float('inf') in min_totals:
        raise ValueError("One of the min stats is inf")  
    
    # Normalise the stats
    norm_stats = []
    for i in range(len(stats)):
        norm_stats.append((stats[i] - min_totals[i]) / (max_totals[i] - min_totals[i]))

    return norm_stats       

def parse_stats(file_path: str) -> list[StatsBase]:
    with open(file_path, 'rb') as f:
        data = f.read()

    num_units = struct.unpack_from('>I', data, 0x00)[0]
    offset = 0x04

    units = []

    for i in range(num_units):
        section_data = struct.unpack_from('>3I24f1I71f', data, offset)
        unit = StatsBase(
            id=i,
            num_tires=section_data[0],
            drift_type=section_data[1],
            weight_class=section_data[2],
            unknown=section_data[3],
            weight=section_data[4],
            bump_deviation=section_data[5],
            speed=section_data[6],
            speed_in_turn=section_data[7],
            tilt=section_data[8],
            std_accel_a0=section_data[9],
            std_accel_a1=section_data[10],
            std_accel_a2=section_data[11],
            std_accel_a3=section_data[12],
            std_accel_t1=section_data[13],
            std_accel_t2=section_data[14],
            std_accel_t3=section_data[15],
            drift_accel_a0=section_data[16],
            drift_accel_a1=section_data[17],
            drift_accel_t1=section_data[18],
            manual_handling=section_data[19],
            auto_handling=section_data[20],
            handling_reactivity=section_data[21],
            manual_drift=section_data[22],
            auto_drift=section_data[23],
            drift_reactivity=section_data[24],
            outside_drift_angle=section_data[25],
            outside_drift_decrement=section_data[26],
            mini_turbo_duration=section_data[27],
            speed_multipliers=section_data[28:60],
            rotation_multipliers=section_data[60:92],
            rotating_items_z_radius=section_data[92],
            rotating_items_x_radius=section_data[93],
            rotating_items_y_distance=section_data[94],
            rotating_items_z_distance=section_data[95],
            max_normal_accel=section_data[96],
            mega_mushroom_scale=section_data[97],
            tire_distance=section_data[98]
        )
        units.append(unit)
        offset += 99 * 4  # Each section is 99 32-bit values

    return units

def set_names(units: list[StatsBase], is_driver: bool):
    '''
    Set the names of the units
    '''

    for unit in units:
        if is_driver:
            unit.is_driver()
        else:
            unit.is_vehicle()

# Example usage
if __name__ == "__main__":
    units = parse_stats('bins\\driverParam.bin')
    for unit in units:
        print(unit)
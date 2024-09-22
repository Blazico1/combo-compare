import struct
import numpy as np
from logic.id import id_to_vehicle, id_to_driver

def EMPTY_DICT():
    return {"speed": 0, "mini_turbo": 0, "drift": 0, "As": [0,0,0,0], "Ts": [0,0,0], "offroad": 0, "weight": 0, "handling": 0, "acceleration": 0}

def INF_DICT():
    return {"speed": float('inf'), "mini_turbo": float('inf'), "drift": float('inf'), "As": [float('inf'),float('inf'),float('inf'),float('inf')], "Ts": [float('inf'),float('inf'),float('inf')], "offroad": float('inf'), "weight": float('inf'), "handling": float('inf'), "acceleration": float('inf')}

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
        self.vehicle_flag = False

    def __repr__(self):
        return (f"StatsBase(name={self.name}, id={self.id:X}, num_tires={self.num_tires}, drift_type={self.drift_type}, "
                f"weight_class={self.weight_class}, weight={self.weight:.2f}, ...)")
    
    def is_vehicle(self):
        self.name = id_to_vehicle(self.id)
        self.vehicle_flag = True
    
    def is_driver(self):
        self.name = id_to_driver(self.id)
        self.vehicle_flag = False

    def get_basic_stats(self):
        speed = self.speed
        mini_turbo = self.mini_turbo_duration
        drift = self.manual_drift

        As = [self.std_accel_a0, self.std_accel_a1, self.std_accel_a2, self.std_accel_a3]
        Ts = [self.std_accel_t1, self.std_accel_t2, self.std_accel_t3]
        
        offroad = self.speed_multipliers[2] + self.speed_multipliers[3] + self.speed_multipliers[4]
        weight = self.weight
        handling = self.manual_handling

        stats = {
            "speed": speed,
            "mini_turbo": mini_turbo,
            "drift": drift,
            "As": As,
            "Ts": Ts,	
            "offroad": offroad,
            "weight": weight,
            "handling": handling,
            "acceleration": np.sum(As)

        }
        return stats

def normalise_stats(v_stats: dict = EMPTY_DICT(), c_stats: dict = EMPTY_DICT(), vehicles: list = [], characters: list = []) -> dict:
    '''
    Normalise the stats of the given vehicles and characters
    '''
    
    keys = ["speed", "mini_turbo", "drift", "offroad", "weight", "handling", "acceleration"]

    if not vehicles and not characters:
        raise ValueError("At least one of vehicles or characters must be provided")
    
    # Get the max stats for each category
    max_vehicle_stats = EMPTY_DICT()
    if vehicles:
        for vehicle in vehicles:
            vstats = vehicle.get_basic_stats()
            for key in keys:
                max_vehicle_stats[key] = max(max_vehicle_stats[key], vstats[key])

    max_character_stats = EMPTY_DICT()
    if characters:
        for character in characters:
            cstats = character.get_basic_stats()
            for key in keys:
                max_character_stats[key] = max(max_character_stats[key], cstats[key])
    
    max_totals = EMPTY_DICT()
    for key in keys:
        max_totals[key] = (max_vehicle_stats[key] + max_character_stats[key])
    
    # Get the min stats for each category
    min_vehicle_stats = INF_DICT()
    if vehicles:
        for vehicle in vehicles:
            vstats = vehicle.get_basic_stats()
            for key in keys:
                min_vehicle_stats[key] = min(min_vehicle_stats[key], vstats[key])
    else:
        min_vehicle_stats = EMPTY_DICT()

    min_character_stats = INF_DICT()
    if characters:
        for character in characters:
            cstats = character.get_basic_stats()
            for key in keys:
                min_character_stats[key] = min(min_character_stats[key], cstats[key])
    else:
        min_character_stats = EMPTY_DICT()

    min_totals = EMPTY_DICT()
    for key in keys:
        min_totals[key] = (min_vehicle_stats[key] + min_character_stats[key])

    # Handle acceleration separately
    max_accel = 0
    min_accel = float('inf')

    if vehicles:
        for vehicle in vehicles:
            vstats = vehicle.get_basic_stats()
            v_As = vstats["As"]
            v_Ts = vstats["Ts"]
            accel = calc_distance_traveled(0, vstats["speed"], v_As, v_Ts, 5)
            max_accel = max(max_accel, accel)
            min_accel = min(min_accel, accel)

        max_totals["acceleration"] = max_accel
        min_totals["acceleration"] = min_accel

    # Raise an error if one of the max stats is 0
    for key in keys:
        if max_totals[key] == 0:
            if max_totals[key] != min_totals[key]:
                raise ValueError("One of the max stats is 0")
    
    # Raise an error if one of the min stats is inf
    if float('inf') in min_totals.values():
        raise ValueError("One of the min stats is inf")  
    
    # Combine vehicle and character stats
    stats = EMPTY_DICT()
    for key in keys:
        stats[key] = v_stats[key] + c_stats[key]

    if vehicles:
        stats["As"] = [v + c for v, c in zip(v_stats["As"], c_stats["As"])]
        stats["Ts"] = v_stats["Ts"]
        stats["acceleration"] = calc_distance_traveled(0, stats["speed"], stats["As"], stats["Ts"], 5)


    # Normalise the stats
    norm_stats = EMPTY_DICT()
    for key in keys:
        norm_stats[key] = (stats[key] - min_totals[key]) / (max_totals[key] - min_totals[key])

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

def calc_acceleration(speed, top_speed, acceleration_values, t_values):
    """
    Calculate the acceleration based on the current speed and top speed.

    :param speed: Current speed of the vehicle.
    :param top_speed: Top speed of the vehicle.
    :param acceleration_values: List of acceleration values (A0 to A4).
    :param t_values: List of T values (T1 to T3).
    :return: Calculated acceleration.
    """
    T = speed / top_speed

    if T <= 0:
        return acceleration_values[0]
    elif T >= 1:
        return 0

    # Interpolate between the data points
    T_values_with_zero = [0] + t_values
    for i in range(1, len(T_values_with_zero)):
        if T < T_values_with_zero[i]:
            T0 = T_values_with_zero[i - 1]
            T1 = T_values_with_zero[i]
            A0 = acceleration_values[i - 1]
            A1 = acceleration_values[i]
            return A0 + (A1 - A0) * ((T - T0) / (T1 - T0))


    return acceleration_values[-1]

def generate_data_points(initial_speed, top_speed, acceleration_values, t_values, total_time):
    """
    Generate data points for speed, acceleration and distance over time.

    :param initial_speed: Initial speed of the vehicle.
    :param top_speed: Top speed of the vehicle.
    :param acceleration_values: List of acceleration values (A0 to A4).
    :param t_values: List of T values (T1 to T3).
    :param total_time: Total time to generate data points for.
    :return: Tuple of lists (times, speeds, accelerations).
    """
    times = np.arange(0, total_time, 1/60)  # 60 FPS
    speeds = []
    accelerations = []
    distances = []
    current_speed = initial_speed

    for t in times:
        acceleration = calc_acceleration(current_speed, top_speed, acceleration_values, t_values)
        current_speed += acceleration  # Update speed based on acceleration
        if current_speed > top_speed:
            current_speed = top_speed
        speeds.append(current_speed)
        accelerations.append(acceleration)

    distances = np.cumsum(speeds)
    return times, speeds, accelerations, distances

def calc_distance_traveled(speed, top_speed, acceleration_values, t_values, total_time):
    """
    Calculate the distance traveled over time.

    :param speed: Current speed of the vehicle.
    :param top_speed: Top speed of the vehicle.
    :param acceleration_values: List of acceleration values (A0 to A4).
    :param t_values: List of T values (T1 to T3).
    :param total_time: Total time to calculate the distance traveled.
    :return: Distance traveled over time.
    """
    times, speeds, accelerations, distances = generate_data_points(speed, top_speed, acceleration_values, t_values, total_time)
    return distances[-1]

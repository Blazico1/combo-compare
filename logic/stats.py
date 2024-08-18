import struct

class StatsBase:
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
    
    def set_name(self, name):
        self.name = name

def parse_stats(file_path):
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

# Example usage
if __name__ == "__main__":
    units = parse_stats('bins\\driverParam.bin')
    for unit in units:
        print(unit)
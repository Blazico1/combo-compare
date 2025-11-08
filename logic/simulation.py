import numpy as np

def simulate_accel(vstats, cstats, wheelie=False, ssmt=False, time=10.0):
    """Simulate a full combo given vehicle and character basic-stats dicts.

    vstats and cstats are expected to be the dicts returned by
    StatsBase.get_basic_stats() (keys: 'speed', 'As', 'Ts', ...).
    This function no longer parses files; the caller should provide the
    already-parsed stats (keeps simulation pure and testable).
    Returns (speeds, distances).
    """
    if vstats is None and cstats is None:
        return None

    v_speed = vstats.get('speed', 0)
    c_speed = cstats.get('speed', 0) 
    top_speed = v_speed + c_speed

    if wheelie:
        top_speed *= 1.15

    v_As = vstats.get('As', [0, 0, 0, 0])
    c_As = cstats.get('As', [0, 0, 0, 0])
    As = [v + c for v, c in zip(v_As, c_As)]

    Ts = vstats.get('Ts', [0, 0, 0]) if vstats else [0, 0, 0]

    boost_top_speed = top_speed * (1.35 if wheelie else 1.2) if ssmt else top_speed

    # Simulation loop
    speeds = []
    distances = []
    current_speed = 0.0
    current_distance = 0.0
    frame_count = int(time * 60)

    for frame in range(frame_count):
        if ssmt:
            if frame < 76:
                # Charging phase
                acceleration = 0
            elif frame < 76 + 30:
                # Boost phase
                acceleration = 3
            else:
                # Normal acceleration after boost
                acceleration = calc_acceleration(current_speed, top_speed, As, Ts)
        else:
            acceleration = calc_acceleration(current_speed, top_speed, As, Ts)

        current_speed += acceleration

        # Apply speed caps
        if ssmt and frame < 76 + 30:
            current_speed = min(current_speed, boost_top_speed)
        else:
            current_speed = min(current_speed, top_speed)

        # Prevent negative speed
        current_speed = max(current_speed, 0)

        current_distance += current_speed
        speeds.append(current_speed)
        distances.append(current_distance)

    return speeds, distances


def simulate_mini_turbo(vstats, cstats, wheelie=False, SMT=False, time=10.0):
    """Simulate a short window after releasing a mini-turbo.

    The initial speed for the post-mini-turbo window is set to the combo's
    drifting top speed (vehicle.speed_in_turn + character.speed_in_turn).
    """
    if vstats is None and cstats is None:
        return None

    # Compute combined speed and accel arrays similar to simulate_combo
    v_speed = vstats.get('speed', 0)
    c_speed = cstats.get('speed', 0)
    speed = v_speed + c_speed

    v_As = vstats.get('As', [0, 0, 0, 0])
    c_As = cstats.get('As', [0, 0, 0, 0])
    As = [v + c for v, c in zip(v_As, c_As)]

    Ts = vstats.get('Ts', [0, 0, 0])

    v_MT = vstats.get('mini_turbo', 0)
    c_MT = cstats.get('mini_turbo', 0)
    MT = v_MT + c_MT

    # MT boost model
    if wheelie:
        top_speed_boost = speed * 1.35
        top_speed = speed * 1.15
    else:
        top_speed_boost = speed * 1.2
        top_speed = speed

    speeds = [speed]
    distances = [0]
    current_speed = speed
    current_distance = 0

    for t in np.arange(0, time*60):  # 60 FPS
        current_speed = speeds[-1]
        current_distance = distances[-1]
        
        if t <= MT or (SMT and t <= 3*MT):
            #MT is active
            current_speed = min(current_speed + 3, top_speed_boost)
        else:
            #MT ended
            current_speed = max(current_speed - 3, top_speed)

        current_distance =+ current_speed

        speeds.append(current_speed)
        distances.append(current_distance)

    return speeds, distances


def calc_acceleration(speed, top_speed, acceleration_values, t_values):
    """Port of calc_acceleration from stats: compute instantaneous accel given speed fraction."""
    if speed > top_speed:
        return -3  # deceleration due to overspeed

    T = speed / top_speed

    if T <= 0:
        return acceleration_values[0]
    elif T >= 1:
        return 0

    T_values_with_zero = [0] + t_values
    for i in range(1, len(T_values_with_zero)):
        if T < T_values_with_zero[i]:
            T0 = T_values_with_zero[i - 1]
            T1 = T_values_with_zero[i]
            A0 = acceleration_values[i - 1]
            A1 = acceleration_values[i]
            return A0 + (A1 - A0) * ((T - T0) / (T1 - T0))

    return acceleration_values[-1]

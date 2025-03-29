import math

def calculate_reward(intersection_data, global_data, params):
    """
    Calculate the reward for an intersection based on both local and global data.
    
    intersection_data: dict with keys like:
        - 'vehicles_cleared': number of vehicles that exited in a timestep
        - 'waiting_times': list of waiting times for vehicles at the intersection
        - 'queue_length': current queue length
    
    global_data: dict with keys like:
        - 'total_waiting_vehicles': total vehicles not cleared in the region
    
    params: dict containing weights and thresholds, e.g.,
        {
            'cleared_reward': 1.0,
            'wait_penalty_weight': 0.5,
            'max_wait_time': 60,  # seconds, threshold for harsh penalty
            'infinite_penalty': 10.0,  # extra penalty for exceeding max wait time
            'global_penalty_weight': 0.2
        }
    """
    # Base reward from vehicles cleared
    reward = params['cleared_reward'] * intersection_data['vehicles_cleared']
    
    # Local penalty for waiting times (using log(1 + waiting time))
    for wait_time in intersection_data['waiting_times']:
        reward -= params['wait_penalty_weight'] * math.log(1 + wait_time)
        # Apply additional penalty if wait_time exceeds maximum threshold
        if wait_time > params['max_wait_time']:
            reward -= params['infinite_penalty']
    
    # Global penalty for overall congestion (if applicable)
    reward -= params['global_penalty_weight'] * global_data['total_waiting_vehicles']
    
    return reward

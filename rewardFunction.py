import math

def calculate_reward(system_data, params):
    """
    Tek bir RL ajanı tarafından kontrol edilen tüm sistemin (tüm kavşaklar) toplam ödülünü hesaplar.

    system_data: dict, tüm kavşaklara ait veriler
        {
            'vehicles_cleared_total': int,
            'waiting_times_all': list of floats,
            'total_waiting_vehicles': int
        }

    params: dict, ağırlıklar ve eşikler
        {
            'cleared_reward': 1.0,
            'wait_penalty_weight': 0.5,
            'max_wait_time': 60,
            'infinite_penalty': 10.0,
            'global_penalty_weight': 0.2
        }
    """
    reward = 0

    # Tüm sistemden çıkan araçlar için pozitif ödül
    reward += params['cleared_reward'] * system_data['vehicles_cleared_total']

    # Her bir bekleme süresi için ceza
    for wait_time in system_data['waiting_times_all']:
        reward -= params['wait_penalty_weight'] * math.log(1 + wait_time)
        if wait_time > params['max_wait_time']:
            reward -= params['infinite_penalty']

    # Tüm sistemde bekleyen toplam araç sayısı için genel ceza
    reward -= params['global_penalty_weight'] * system_data['total_waiting_vehicles']

    return reward

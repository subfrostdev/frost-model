import math
from typing import List

def calculate_cubic_coefficients(duration_blocks: int, estimated_growth_T: float):
    expected_yield = estimated_growth_T - 1.0
    c_mint = 0.30 * expected_yield
    one_minus_c_mint = 1.0 - c_mint
    p_0 = c_mint / one_minus_c_mint if one_minus_c_mint!=0 else 0.0
    p_1 = 1.0 - 1.0 / (one_minus_c_mint * estimated_growth_T) if one_minus_c_mint*estimated_growth_T!=0 else 0.0
    c_0 = p_0
    c_1 = 0.0
    delta_p = p_1 - p_0
    c_2 = -2.0 * delta_p
    c_3 = 3.0 * delta_p
    return [c_0, c_1, c_2, c_3, c_mint]

def calculate_early_exercise_premium(blocks_elapsed: int, duration_blocks: int, coeffs: List[float]):
    c_0, c_1, c_2, c_3, c_mint = coeffs
    t = min(max(blocks_elapsed / duration_blocks, 0.0), 1.0)
    p_t = c_0 + c_1 * t + c_2 * (t**2) + c_3 * (t**3)
    return p_t

def estimate_growth_over_duration(duration_blocks: int, twap_growth_per_block: float):
    excess_per_block = twap_growth_per_block - 1.0
    estimated_growth_T = 1.0 + (excess_per_block * duration_blocks)
    return estimated_growth_T

def check_miner_break_even(frbtc_deposited: float, blocks_held: int, rate_at_mint: float, rate_at_exercise: float, duration=52560, twap_growth_per_block=1.0):
    estimated_growth = estimate_growth_over_duration(duration, twap_growth_per_block)
    coeffs = calculate_cubic_coefficients(duration, estimated_growth)
    c_mint = coeffs[4]
    initial_shares = frbtc_deposited / rate_at_mint if rate_at_mint>0 else 0.0
    shares_after_mint = initial_shares * (1 - c_mint)
    p_t = calculate_early_exercise_premium(blocks_held, duration, coeffs)
    shares_after_exercise = shares_after_mint * (1 - p_t)
    frbtc_received = shares_after_exercise * rate_at_exercise
    growth_actual = rate_at_exercise / rate_at_mint if rate_at_mint>0 else 0.0
    break_even_ratio = frbtc_received / frbtc_deposited if frbtc_deposited>0 else 0.0
    total_premiums_burned = c_mint + (1 - c_mint) * p_t
    return {
        'frbtc_deposited': frbtc_deposited,
        'frbtc_received': frbtc_received,
        'break_even_ratio': break_even_ratio,
        'growth_actual': growth_actual,
        'mint_premium': c_mint,
        'exercise_premium': p_t,
        'total_premiums_burned': total_premiums_burned
    }

def calculate_utilization_rate(utilization_buffer, base_reward):
    total_minted = sum(utilization_buffer)
    total_possible = base_reward * len(utilization_buffer) if len(utilization_buffer)>0 else 0.0
    if total_possible == 0:
        return 0.0
    return total_minted / total_possible

def adjust_coefficients_for_utilization(base_coeffs, utilization_rate):
    min_factor = 0.1
    max_factor = 1.0
    adjustment_factor = min_factor + (max_factor - min_factor) * utilization_rate
    adjusted = [c * adjustment_factor for c in base_coeffs]
    return adjusted

def get_base_block_reward(height: int):
    halvings = height // 210000
    if halvings >= 64:
        return 0
    initial_reward = 50 * 1e8
    return initial_reward / (2**halvings)

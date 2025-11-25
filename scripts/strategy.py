from typing import Dict, Any
from lbtc import calculate_discount_recovery_apy
from lp_gauges import calculate_lp_fees_earned, calculate_gauge_base_rewards, calculate_boost_multiplier, calculate_boosted_rewards

def calculate_yvfrBTC_yield(total_frbtc: float, strategy_allocations: Dict[str, float], strategy_apys: Dict[str, float]):
    weighted_apy = 0.0
    for strategy, allocation in strategy_allocations.items():
        apy = strategy_apys.get(strategy, 0.0)
        weighted_apy += allocation * apy
    return weighted_apy

def calculate_dxBTC_APY(dxBTC_tvl: float, yvfrBTC_strategy_apy: float, utilization_rate: float):
    dxBTC_apy = yvfrBTC_strategy_apy * utilization_rate
    return dxBTC_apy

def calculate_pLBTC_LP_strategy_apy(frbtc_allocated, pLBTC_frBTC_pool_tvl, daily_volume_pLBTC_pool, pLBTC_discount=0.04, time_to_maturity_years=1.0):
    fee_apy = calculate_lp_fees_earned(frbtc_allocated, pLBTC_frBTC_pool_tvl, daily_volume_pLBTC_pool, fee_rate=0.0004, admin_fee=0.5)
    pLBTC_price = 1.0 - pLBTC_discount
    discount_apy = calculate_discount_recovery_apy(pLBTC_price, time_to_maturity_years)
    total_apy = fee_apy + discount_apy
    return {'fee_apy': fee_apy, 'discount_apy': discount_apy, 'total_apy': total_apy}

def calculate_gauge_strategy_apy(frbtc_allocated, gauge_pool: Dict[str, Any], user_vxFROST_locked=0):
    base_apy = calculate_gauge_base_rewards(
        LP_staked=frbtc_allocated,
        total_LP_staked=gauge_pool['total_lp'],
        reward_token_per_day=gauge_pool['daily_rewards'],
        reward_token_price=gauge_pool['reward_price'],
        lp_token_price=1.0
    )
    if user_vxFROST_locked > 0:
        boost = calculate_boost_multiplier(frbtc_allocated, gauge_pool['total_lp'], user_vxFROST_locked, gauge_pool['total_vxFROST'])
        boosted_apy = calculate_boosted_rewards(base_apy, boost)
        return boosted_apy
    return base_apy

def simulate_full_system(params: Dict):
    pLBTC_allocated = params['yvfrBTC_allocation_pLBTC'] * params['yvfrBTC_tvl']
    pLBTC_lp = calculate_pLBTC_LP_strategy_apy(
        pLBTC_allocated,
        params['pLBTC_pool_tvl'],
        params['pLBTC_daily_volume'],
        params.get('pLBTC_discount', 0.04),
        params.get('pLBTC_time_to_maturity', 1.0)
    )
    gauge_apys = {}
    for gauge_name, gauge_params in params['gauges'].items():
        gauge_apys[gauge_name] = calculate_gauge_strategy_apy(
            params.get(f'yvfrBTC_allocation_{gauge_name}', 0.0) * params['yvfrBTC_tvl'],
            gauge_params,
            params.get('user_vxFROST', 0)
        )
    strategy_allocations = {
        'pLBTC_frBTC_LP': params['yvfrBTC_allocation_pLBTC'],
        **{k: params.get(f'yvfrBTC_allocation_{k}', 0.0) for k in params['gauges'].keys()},
        'idle_reserve': params['yvfrBTC_allocation_reserve']
    }
    strategy_apys = {
        'pLBTC_frBTC_LP': pLBTC_lp['total_apy'],
        **gauge_apys,
        'idle_reserve': 0.0
    }
    yvfrBTC_apy = calculate_yvfrBTC_yield(params['yvfrBTC_tvl'], strategy_allocations, strategy_apys)
    dxBTC_apy = calculate_dxBTC_APY(params['dxBTC_tvl'], yvfrBTC_apy, params['utilization_rate'])
    futures_utilization = params.get('futures_utilization_rate', 0.0)
    total_premiums_burned = futures_utilization * params['dxBTC_tvl'] * 0.03
    deflation_boost = total_premiums_burned / params['dxBTC_tvl'] if params['dxBTC_tvl']>0 else 0.0
    effective_dxBTC_apy = dxBTC_apy + deflation_boost
    return {
        'yvfrBTC_apy': yvfrBTC_apy,
        'dxBTC_base_apy': dxBTC_apy,
        'deflation_boost': deflation_boost,
        'effective_dxBTC_apy': effective_dxBTC_apy,
        'breakdown': {
            'pLBTC_lp': pLBTC_lp,
            'gauges': gauge_apys,
            'strategy_allocations': strategy_allocations,
            'strategy_apys': strategy_apys
        }
    }

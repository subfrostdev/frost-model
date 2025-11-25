from strategy import simulate_full_system
import json

base_params = {
    'dxBTC_tvl': 1000,
    'yvfrBTC_tvl': 1000,
    'utilization_rate': 0.70,
    'yvfrBTC_allocation_pLBTC': 0.40,
    'yvfrBTC_allocation_DIESEL_frBTC': 0.30,
    'yvfrBTC_allocation_reserve': 0.30,
    'pLBTC_pool_tvl': 5000,
    'pLBTC_daily_volume': 50,
    'pLBTC_discount': 0.04,
    'pLBTC_time_to_maturity': 1.0,
    'gauges': {
        'DIESEL_frBTC': {
            'total_lp': 1000,
            'daily_rewards': 500,
            'reward_price': 0.5,
            'total_vxFROST': 50000
        }
    },
    'user_vxFROST': 0,
    'futures_utilization_rate': 0.10
}

if __name__ == "__main__":
    res = simulate_full_system(base_params)
    print(json.dumps(res, indent=2))

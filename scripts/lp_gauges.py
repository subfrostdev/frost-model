def calculate_lp_fees_earned(LP_owned, total_LP, daily_volume, fee_rate=0.0004, admin_fee=0.5):
    daily_fees_total = daily_volume * fee_rate
    daily_fees_to_lp = daily_fees_total * (1 - admin_fee)
    lp_share = (LP_owned / total_LP) if total_LP>0 else 0.0
    daily_fees_earned = daily_fees_to_lp * lp_share
    annual_fees = daily_fees_earned * 365
    lp_value = LP_owned if LP_owned>0 else 1.0
    fee_apy = annual_fees / lp_value
    return fee_apy

def calculate_gauge_base_rewards(LP_staked, total_LP_staked, reward_token_per_day, reward_token_price, lp_token_price=1.0):
    lp_share = (LP_staked / total_LP_staked) if total_LP_staked>0 else 0.0
    daily_rewards_token = reward_token_per_day * lp_share
    daily_rewards_usd = daily_rewards_token * reward_token_price
    annual_rewards = daily_rewards_usd * 365
    lp_value = LP_staked * lp_token_price if lp_token_price>0 else LP_staked
    base_apy = annual_rewards / lp_value if lp_value>0 else 0.0
    return base_apy

def calculate_boost_multiplier(user_LP_staked, total_LP_staked, user_vxFROST, total_vxFROST, min_boost=1.0, max_boost=2.5):
    if total_vxFROST == 0:
        return min_boost
    vxFROST_share = user_vxFROST / total_vxFROST
    boost = min_boost + vxFROST_share * (max_boost - min_boost)
    if boost > max_boost:
        boost = max_boost
    return boost

def calculate_boosted_rewards(base_apy, boost_multiplier):
    return base_apy * boost_multiplier

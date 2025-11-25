def calculate_pLBTC_fair_value(LBTC_APY: float, time_to_maturity_years: float):
    if time_to_maturity_years == 0:
        return 1.0
    return 1.0 / (1.0 + LBTC_APY * time_to_maturity_years)

def calculate_yxLBTC_fair_value(LBTC_APY: float, time_to_maturity_years: float):
    return LBTC_APY * time_to_maturity_years

def calculate_discount_recovery_apy(pLBTC_purchase_price: float, time_to_maturity_years: float):
    if time_to_maturity_years == 0:
        return 0.0
    gain_per_year = (1.0 - pLBTC_purchase_price) / time_to_maturity_years
    apy = gain_per_year / pLBTC_purchase_price if pLBTC_purchase_price>0 else 0.0
    return apy

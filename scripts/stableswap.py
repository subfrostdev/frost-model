import math

def calculate_D(reserves, A):
    return sum(reserves)

def stableswap_get_y(x, A, D):
    if A == 0:
        return D**2 / (4 * x) if x>0 else 0.0
    c = D**3 / (4 * A * x) if x>0 else 0.0
    b = x + D / A if A!=0 else x
    y = (b + math.sqrt(max(0.0, b*b + 4*c))) / 2.0
    return y

def stableswap_swap(amount_in, reserve_in, reserve_out, A, fee_rate=0.0004):
    D = calculate_D([reserve_in, reserve_out], A)
    amount_in_with_fee = amount_in * (1 - fee_rate)
    new_reserve_in = reserve_in + amount_in_with_fee
    new_reserve_out = stableswap_get_y(new_reserve_in, A, D)
    amount_out = reserve_out - new_reserve_out
    return amount_out

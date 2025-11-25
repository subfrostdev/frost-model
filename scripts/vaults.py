"""Vault related formulas (from gist) - simplified implementations."""
import math
from typing import List

class TWAPState:
    def __init__(self):
        self.buffer = [0.0]*6
        self.index = 0
        self.last_block = None

    def update(self, total_yvfrbtc_value_in_frbtc: float, total_dxbtc_supply: float, current_block: int):
        rate = 0.0
        if total_dxbtc_supply > 0:
            rate = (total_yvfrbtc_value_in_frbtc * 1e8) / total_dxbtc_supply
        self.buffer[self.index] = rate
        self.index = (self.index + 1) % 6
        self.last_block = current_block
        return rate

    def calculate_twap(self):
        return sum(self.buffer)/6.0

    def calculate_growth_per_block(self):
        oldest_idx = (self.index) % 6
        newest_idx = (self.index - 1) % 6
        rate_6_blocks_ago = self.buffer[oldest_idx]
        rate_current = self.buffer[newest_idx]
        if rate_6_blocks_ago == 0 or rate_current == 0:
            return 1.0
        growth_6_blocks = rate_current / rate_6_blocks_ago
        growth_per_block = growth_6_blocks ** (1/6.0)
        return growth_per_block

def deposit_frbtc(amount_frbtc: float, total_dxbtc_supply: float, total_assets_value: float, yvfrbtc_rate: float):
    yvfrbtc_shares = amount_frbtc / yvfrbtc_rate if yvfrbtc_rate>0 else 0.0
    if total_dxbtc_supply == 0:
        dxbtc_shares = amount_frbtc
    else:
        dxbtc_shares = (amount_frbtc * total_dxbtc_supply) / total_assets_value if total_assets_value>0 else 0.0
    return dxbtc_shares, yvfrbtc_shares

def withdraw_dxbtc(dxbtc_shares: float, total_assets_value: float, total_dxbtc_supply: float, yvfrbtc_rate: float):
    frbtc_value = (dxbtc_shares * total_assets_value) / total_dxbtc_supply if total_dxbtc_supply>0 else 0.0
    yvfrbtc_to_burn = frbtc_value / yvfrbtc_rate if yvfrbtc_rate>0 else 0.0
    frbtc_received = yvfrbtc_to_burn * yvfrbtc_rate
    return frbtc_received

def calculate_total_assets(vault_yvfrbtc_balance: float, yvfrbtc_rate: float):
    return vault_yvfrbtc_balance * yvfrbtc_rate

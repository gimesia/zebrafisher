"""
TODO: add ref
"""

from src.filters.high_pass_filter import high_pass_filter
from src.filters.low_pass_filter import low_pass_filter


def high_boost_filter(size: tuple[int, int], cutoff: float, n: int, boost: float):
    if cutoff < 0 or cutoff > 0.5:
        raise Exception("cutoff frequency must be between 0 and 0.5")

    if n % 1 != 0 or n < 1:
        raise Exception("n must be an integer >= 1")

    if boost >= 1:
        f = (1 - 1 / boost * high_pass_filter(size, cutoff, n) + 1 / boost)
    else:
        f = (1 - boost) * low_pass_filter(size, cutoff, n) + boost

    return f

"""
TODO: add ref
"""

from src.filters.low_pass_filter import low_pass_filter


def high_pass_filter(size: tuple[int, int], cutoff: float, n: int):
    if cutoff < 0 or cutoff > 0.5:
        raise Exception("cutoff frequency must be between 0 and 0.5")

    if n % 1 != 0 or n < 1:
        raise Exception("n must be an integer >= 1")

    return 1.0 - low_pass_filter(size, cutoff, n)

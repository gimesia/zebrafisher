import numpy as np


def histc(x: np.ndarray, bins: np.ndarray) -> np.ndarray:
    map_to_bins = np.digitize(x, bins)
    r = np.zeros(bins.shape)
    for i in map_to_bins:
        r[i - 1] += 1
    # Used to be, but I don't need it: return [r, map_to_bins]
    return r

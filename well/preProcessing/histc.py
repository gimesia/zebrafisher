import numpy as np


def histc(x: np.ndarray, bins: np.ndarray):
    map_to_bins = np.digitize(x, bins)
    r = np.zeros(bins.shape)
    for i in map_to_bins:
        r[i - 1] += 1
    return [r, map_to_bins]


if __name__ == "__main__":
    X = np.array([0.9828, 0.4662, 0.5245, 0.9334, 0.2163])
    binny = np.array([0.0191, 0.2057, 0.2820, 0.2851, 1.0])
    [A, I] = histc(X, binny)
    print("X", X)
    print("bins", binny)
    print("A", A, "expecting", [0, 1, 0, 4, 0])
    print("I", I, "expecting", [4, 4, 4, 4, 2])

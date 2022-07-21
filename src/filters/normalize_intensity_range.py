import numpy as np

from src.terminal_msg import msg


def normalize_intensity_range(image: np.ndarray, rng: tuple[int, int]) -> np.ndarray:
    """
    Normalises the input image on a given range

    :rtype: np.ndarray, dtype = double
    """
    msg("Normalizing intensity")
    double_precision_image = np.double(image)
    mx = np.max(double_precision_image)
    mn = np.min(double_precision_image)

    # Element-wise (should be right-side) division, maybe I could use 'np.true_divide'
    normalised_first: np.ndarray = (double_precision_image - mn) / (mx - mn)

    return (normalised_first * (rng[1] - rng[0])) + rng[0]

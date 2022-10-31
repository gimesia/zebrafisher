import numpy as np
from skimage.morphology import dilation, square, erosion


def range_filter(img: np.ndarray, mask=None) -> np.ndarray:
    """
    Gets the max and min value in a 3x3 neighborhood and returns its difference

    @rtype: range-filtered image (not normalized)
    """
    se = square(3)
    dilated = dilation(img, se)
    eroded = erosion(img, se)
    if mask is not None:
        return (dilated - eroded) * mask
    return dilated - eroded

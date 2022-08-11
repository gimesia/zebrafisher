import numpy as np
from skimage.measure import regionprops, label


def is_fish(img: np.ndarray) -> bool:
    """
    Determines whether if object on image is a fish or not
    :param img: input image
    :return: True or False
    """
    labeled = label(img)
    reg_props = regionprops(labeled)
    if reg_props[0].eccentricity > 0.9:  # 0.92
        fish = True
    else:
        fish = False
    return fish

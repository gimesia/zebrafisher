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
    print(reg_props)
    if reg_props[0].eccentricity < 0.92:  # 0.92
        print("Isn't eccentric enough")
        return False
    if reg_props[0].area > (img.size / 4):
        print("Too big")
        return False

    return True

import numpy as np
from skimage.measure import regionprops, label

from src.utils import keep_largest_object


def is_fish(img: np.ndarray) -> bool:
    """
    Determines whether if object on image is a fish or not

    :param img: input image
    :return: True or False
    """
    img = keep_largest_object(img)
    labeled = label(img)
    reg_props = regionprops(labeled)
    if len(reg_props) != 1:
        raise Exception("Should have only one object")

    if reg_props[0].eccentricity < 0.92:  # 0.92
        print("NOT FISH!")
        print(f"Isn't eccentric enough: {reg_props[0].eccentricity}")
        return False

    if reg_props[0].area > (img.size / 4):
        print("NOT FISH!")
        print(f"Too big! object / well = {reg_props[0].area / img.size}")
        return False

    print("IS FISH!")
    return True

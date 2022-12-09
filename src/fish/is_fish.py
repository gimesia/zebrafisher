import numpy as np
from skimage.measure import regionprops, label

from ..utils import keep_largest_object


def is_fish(img: np.ndarray, well_mask: np.ndarray) -> bool:
    """
    Determines whether if object on image is a fish or not

    :param img: input image
    :return: True or False
    """
    well_area = len(well_mask.nonzero()[0])

    img = keep_largest_object(img)
    labeled = label(img)
    reg_props = regionprops(labeled)
    if len(reg_props) != 1:
        raise Exception("Should have only one object")

    if reg_props[0].eccentricity < 0.90:  # 0.92
        print("NOT FISH!")
        print(f"Isn't eccentric enough: {reg_props[0].eccentricity}")
        return False

    if reg_props[0].area > (well_area * 0.10):
        print("NOT FISH!")
        print(f"Too big! object.area / well.area = {reg_props[0].area / well_area}")
        return False

    if reg_props[0].area < (well_area * 0.02):
        print("NOT FISH!")
        print(f"Too big! object.area / well.area = {reg_props[0].area / well_area}")
        return False

    image = reg_props[0].image_filled

    if image.shape[0] > image.shape[1]:
        image = image.transpose()
        well_mask = well_mask.transpose()

    if image.shape[1] < well_mask.shape[1] * 0.2:
        print("NOT FISH!")
        print(f"Too big! object.width / well.width = {reg_props[0].area / well_area}")
        return False

    print("IS FISH!")
    return True

import numpy as np
from skimage.measure import regionprops_table, label
from skimage.morphology import remove_small_objects, convex_hull_image, binary_dilation, disk

from src.models import InputImage
from src.terminal_msg import show_img


def keep_largest_object(binary_img: np.ndarray) -> np.ndarray:
    """
    Removes all objects from an image but the largest one
    :param binary_img: input image
    :return: same image, with only the largest object area-wise
    """
    labeled = label(binary_img)
    props = regionprops_table(binary_img.astype(int), properties=('area', 'label'))
    max_area = props['area'].max()

    removed = remove_small_objects(binary_img.astype(bool), max_area - 100).astype(int)

    return removed


def convex_hull_for_fish(input_img: InputImage) -> InputImage:
    """
    Notes:  - uses images from the '.processed' image not the '.binary' attributes
            - stores images in the '.fish_props.mask' attributes

    :param input_img:
    :return: InputImage object with mask for the fish
    """

    hull = fish_convex_hull(input_img.processed)
    input_img.fish_props.mask.og = hull
    input_img.fish_props.mask.masked = hull * input_img.well_props.mask.cropped_masked

    return input_img


def fish_convex_hull(binary_img: np.ndarray) -> np.ndarray:
    one_object_img = keep_largest_object(binary_img)
    hull = convex_hull_image(one_object_img)
    hull = binary_dilation(hull, disk(15))
    return hull.astype(int)

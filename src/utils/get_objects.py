import numpy as np
from skimage.measure import label, regionprops_table
from skimage.morphology import remove_small_objects

from src.utils.terminal_msg import msg


def keep_largest_object(binary_img: np.ndarray) -> np.ndarray:
    """
    Removes all objects from an image but the largest one
    :param binary_img: input image
    :return: same image, with only the largest object area-wise
    """
    labeled = label(binary_img)
    props = regionprops_table(labeled.astype(int), properties=('area', 'label'))
    print(props)
    if len(props) != 0:
        max_area = props['area'].max()
        removed = remove_small_objects(binary_img.astype(bool), max_area - (max_area * 0.2)).astype(np.uint8)
        return removed
    else:
        msg("Error in getting objects")
    return binary_img

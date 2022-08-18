import numpy as np
from skimage.measure import label, regionprops_table
from skimage.morphology import remove_small_objects

from src.utils.terminal_msg import msg, show_img


def keep_largest_object(binary_img: np.ndarray) -> np.ndarray:
    """
    Removes all objects from an image but the largest one

    :param binary_img: input image
    :return: same image, with only the largest object area-wise
    """
    msg("Finding largest object")

    labeled = label(binary_img)
    props = regionprops_table(labeled.astype(int), properties=('area', 'label', 'image_filled', 'bbox'))

    if len(props) != 0:
        max_index = np.where(props['area'] == props['area'].max())[0]
        x1, y1, x2, y2 = props['bbox-0'][max_index][0], props['bbox-1'][max_index][0], props['bbox-2'][max_index][0], \
                         props['bbox-3'][max_index][0]

        removed = np.zeros_like(binary_img)
        removed[x1:x2, y1:y2] = props['image_filled'][max_index][0]

        return removed
    else:
        print(Warning("No objects found"))
        return binary_img


def keep_largest_object_convex(binary_img: np.ndarray) -> np.ndarray:
    """
    Removes all objects from an image but the largest one, and return its convex hull

    :param binary_img: input image
    :return: same image, with only the largest object's convex hull
    """
    msg("Finding largest object's convex hull")

    labeled = label(binary_img)
    props = regionprops_table(labeled.astype(int), properties=('area', 'label', 'image_convex', 'bbox'))

    if len(props) != 0:
        max_index = np.where(props['area'] == props['area'].max())[0]
        x1, y1, x2, y2 = props['bbox-0'][max_index][0], props['bbox-1'][max_index][0], props['bbox-2'][max_index][0], \
                         props['bbox-3'][max_index][0]

        removed = np.zeros_like(binary_img)
        removed[x1:x2, y1:y2] = props['image_convex'][max_index][0]

        return removed
    else:
        print(Warning("No objects found"))
        return binary_img


def get_filled_object(binary_img: np.ndarray) -> np.ndarray:
    """
    Removes all objects from an image but the largest one
    :param binary_img: input image
    :return: same image, with only the largest object area-wise
    """
    labeled = label(binary_img)
    props = regionprops_table(labeled.astype(int), properties=('label', 'image_convex'))

    if len(props['label']) == 1:
        return props['image_convex'][0]
    else:
        msg(f"More than one object {len(props['label'])}")
        return binary_img

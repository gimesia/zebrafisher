import numpy as np
from skimage.measure import label, regionprops_table

from src.models import BoundingBox
from src.utils.terminal_msg import msg


def keep_largest_object(binary_img: np.ndarray) -> np.ndarray:
    """
    Removes all objects from an image but the largest one

    :param binary_img: input image
    :return: same image, with only the largest object area-wise
    """
    msg("Finding largest object")

    labeled = label(binary_img)
    props = regionprops_table(labeled.astype(int), properties=('area', 'label', 'image', 'bbox'))
    if len(props['area']) != 0:
        max_index = np.where(props['area'] == props['area'].max())[0]
        x1, y1, x2, y2 = props['bbox-0'][max_index][0], props['bbox-1'][max_index][0], \
                         props['bbox-2'][max_index][0], props['bbox-3'][max_index][0]

        removed = np.zeros_like(binary_img)
        removed[x1:x2, y1:y2] = props['image'][max_index][0]

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


def keep_second_largest_object(binary_img: np.ndarray) -> np.ndarray:
    """
    Removes all objects from an image but the largest one

    :param binary_img: input image
    :return: same image, with only the second to largest object area-wise
    """
    labeled = label(binary_img)
    props = regionprops_table(labeled, properties=('area', 'label', 'image', 'bbox'))

    if len(props) < 2:
        raise Exception(f"{len(props)} objects found")

    max_2_area = np.sort(props['area'])[-2:]
    second = max_2_area[0]
    second_i = np.where((props['area'] == second))

    bbox_second = BoundingBox(props['bbox-0'][second_i][0], props['bbox-1'][second_i][0], props['bbox-2'][second_i][0],
                              props['bbox-3'][second_i][0])

    removed = np.zeros_like(binary_img, dtype=np.uint8)
    removed[bbox_second.x1:bbox_second.x2, bbox_second.y1:bbox_second.y2] = props['image'][second_i][0]
    return removed


def keep_2_largest_object(binary_img: np.ndarray) -> np.ndarray:
    """
    Removes all objects from an image but the largest one

    :param binary_img: input image
    :return: same image, with only the 2 largest object area-wise
    """
    labeled = label(binary_img)
    props = regionprops_table(labeled, properties=('area', 'label', 'image_filled', 'bbox'))

    if len(props) < 2:
        raise Exception(f"{len(props)} objects found")

    max_2_area = np.sort(props['area'])[-2:]

    if len(max_2_area) < 2:
        return keep_largest_object(binary_img)

    first = max_2_area[1]
    second = max_2_area[0]

    first_i = np.where((props['area'] == first))
    second_i = np.where((props['area'] == second))

    bbox_first = BoundingBox(props['bbox-0'][first_i][0], props['bbox-1'][first_i][0], props['bbox-2'][first_i][0],
                             props['bbox-3'][first_i][0])
    bbox_second = BoundingBox(props['bbox-0'][second_i][0], props['bbox-1'][second_i][0], props['bbox-2'][second_i][0],
                              props['bbox-3'][second_i][0])

    removed = np.zeros_like(binary_img, dtype=np.uint8)
    removed[bbox_second.x1:bbox_second.x2, bbox_second.y1:bbox_second.y2] = props['image_filled'][second_i][0]
    removed[bbox_first.x1:bbox_first.x2, bbox_first.y1:bbox_first.y2] = removed[bbox_first.x1:bbox_first.x2,
                                                                        bbox_first.y1:bbox_first.y2] + \
                                                                        props['image_filled'][first_i][0]
    return removed


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

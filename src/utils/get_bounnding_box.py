import numpy as np
from skimage.measure import regionprops, label

from src.models import BoundingBox


def get_bounding_box(img: np.ndarray) -> [int, int, int, int]:
    """
    Finds the bounding box of the first found object on an image
    Notes: - advised to use, when only one object is present

    :param img: input img
    :returns: bounding box coordinates [x1, y1, x2, y2]
    """
    actual_height, actual_width = img.shape[0], img.shape[1]

    labeled = label(img.astype(np.uint8))
    props = regionprops(labeled)

    if len(props) == 0:
        raise Exception("No object found")

    [x1, y1, x2, y2] = props[0].bbox

    if actual_height <= y2:
        y2 = y2 - 1

    if actual_width <= x2:
        x2 = x2 - 1

    return [x1, y1, x2, y2]


def get_bounding_box_obj(img: np.ndarray) -> BoundingBox:
    """
    Finds the bounding box of the first found object on an image
    Notes: - advised to use, when only one object is present

    :param img: input img
    :returns: bounding box object
    """
    bbox = BoundingBox()
    bbox.set(get_bounding_box(img))

    return bbox


def crop_to_bbox(bin_img: np.ndarray):
    """
    Crops binary image with one visible object to the size of the bounding box of the object

    :param bin_img: binary image with one object

    :returns: cropped binary image
    """
    props = regionprops(label(bin_img))[0]
    bbox = BoundingBox()
    bbox.set(props.bbox)
    return bbox.bound_img(bin_img)

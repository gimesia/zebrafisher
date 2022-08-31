import numpy as np
from skimage.measure import regionprops, label

from src.models import BoundingBox


def get_bounding_box(img: np.ndarray) -> [int, int, int, int]:
    """
    Finds the bounding box of the first found object on an image
    Notes: - advised to use, when only one object is present

    :param img: input img
    :return: bounding box coordinates [x1, y1, x2, y2]
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
    :return: bounding box object
    """
    bbox = BoundingBox()
    bbox.set(get_bounding_box(img))

    return bbox


if __name__ == "__main__":
    pass

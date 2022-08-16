import numpy as np
from skimage.measure import regionprops, label

from src.models import BoundingBox


def get_bounding_box(img: np.ndarray) -> [int, int, int, int]:
    actual_height, actual_width = img.shape[0], img.shape[1]

    labeled = label(img.astype(np.uint8))
    props = regionprops(labeled)
    [x1, y1, x2, y2] = props[0].bbox

    if actual_height <= y2:
        y2 = y2 - 1

    if actual_width <= x2:
        x2 = x2 - 1

    return [x1, y1, x2, y2]


def get_bounding_box_obj(img: np.ndarray) -> BoundingBox:
    bbox = BoundingBox()
    bbox.set(get_bounding_box(img))

    return bbox


if __name__ == "__main__":
    pass

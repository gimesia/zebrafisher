import numpy as np
from skimage.measure import regionprops

from src.models import EXAMPLE_IMG
from src.terminal_msg import msg


def get_bounding_box_coords(img: np.ndarray) -> [int, int, int, int]:
    msg("Get bounding box")
    actual_height, actual_width = img.shape[0], img.shape[1]

    # img.processed = bwareafilt(img.processed)

    props = regionprops(img)
    [x1, y1, x2, y2] = props[0].bbox

    if actual_height <= y2:
        y2 = y2 - 1

    if actual_width <= x2:
        x2 = x2 - 1

    return [x1, y1, x2, y2]


if __name__ == "__main__":
    a = EXAMPLE_IMG
    print(get_bounding_box_coords(a.processed))

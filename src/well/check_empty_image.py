import numpy as np


def is_image_empty(img: np.ndarray) -> bool:
    [rows, cols] = img.nonzero()
    if len(rows) == 0 or len(cols) == 0:
        return False
    return True

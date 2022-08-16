import numpy as np


def is_empty_img(img: np.ndarray) -> bool:
    [rows, cols] = img.nonzero()  # Gets the indexes of the elements with value True
    if len(rows) == 0 or len(cols) == 0:
        return True
    return False

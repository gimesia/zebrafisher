import numpy as np
from cv2 import normalize, NORM_MINMAX


def normalize_0_1(img: np.ndarray) -> np.ndarray:
    """
    Normalizes given image between 0 - 1

    :param img: input image
    :return: normalized image
    """
    return normalize(src=img, dst=None, alpha=0, beta=1, norm_type=NORM_MINMAX).astype(float)


def normalize_0_255(img: np.ndarray) -> np.ndarray:
    """
    Normalizes given image between 0 - 255

    :param img: input image
    :return: normalized image
    """
    return normalize(src=img, dst=None, alpha=0, beta=255, norm_type=NORM_MINMAX).astype(np.uint8)

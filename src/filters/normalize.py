import numpy as np
from cv2 import normalize, NORM_MINMAX


def normalize_0_1(img: np.ndarray) -> np.ndarray:
    return normalize(src=img, dst=None, alpha=0, beta=1, norm_type=NORM_MINMAX)


def normalize_0_255(img: np.ndarray) -> np.ndarray:
    return normalize(src=img, dst=None, alpha=0, beta=255, norm_type=NORM_MINMAX)

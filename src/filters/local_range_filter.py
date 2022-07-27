import numpy as np
from skimage import morphology


def range_filter(binary_img: np.ndarray) -> np.ndarray:
    # TODO: paraméter hibakezelés

    structuring_elem = morphology.square(5)

    eroded = morphology.erosion(binary_img, selem=structuring_elem)
    dilated = morphology.dilation(binary_img, selem=structuring_elem)

    return dilated ^ eroded

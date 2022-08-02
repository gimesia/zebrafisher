import numpy as np
from skimage.morphology import disk, erosion, dilation


def modify_circle(img: np.ndarray, kernel_size: int, e_or_d):
    structuring_element = disk(kernel_size)
    if e_or_d == "e":
        return erosion(img, structuring_element)
    elif e_or_d == "d":
        return dilation(img, structuring_element)
    else:
        raise Exception('put \'e\' or \'d\' as 3rd param')

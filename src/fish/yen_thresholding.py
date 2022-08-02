import numpy as np
from skimage.filters.thresholding import threshold_yen
from skimage.morphology import disk, binary_dilation, binary_erosion, remove_small_holes, remove_small_objects

from src.models import InputImage


def yen_th(img: np.ndarray):
    thresh = threshold_yen(img)
    binary = img > thresh

    se = disk(2)
    dilated = binary_dilation(binary, footprint=se)

    return remove_small_objects(remove_small_holes(dilated, connectivity=np.ndim(dilated), area_threshold=100))


def yen_thresholding(input_img: InputImage):
    th = yen_th(input_img.processed)
    input_img.binary = th.astype(int)
    input_img.processed = th.astype(int)
    return input_img

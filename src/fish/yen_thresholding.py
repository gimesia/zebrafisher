import numpy as np
import cv2 as cv
from skimage.filters.thresholding import threshold_yen
from skimage.morphology import disk, binary_dilation, binary_erosion, remove_small_holes, remove_small_objects

import matplotlib.pyplot as plt


from src.models import InputImage
from src.terminal_msg import msg


def removing_speckles(img: np.ndarray):
    se = disk(2)
    dilated = binary_dilation(img, footprint=se)

    return remove_small_objects(remove_small_holes(dilated, connectivity=np.ndim(dilated), area_threshold=100))


def yen_th(img: np.ndarray):
    thresh = threshold_yen(img)
    binary = img > thresh

    return binary.astype(int)


def yen_thresholding(input_img: InputImage):
    msg("Applying Yen-thresholding")

    th = yen_th(input_img.processed)

    input_img.binary = th.astype(int)
    msg("Stored binary image in object")

    input_img.processed = th.astype(int)
    return input_img

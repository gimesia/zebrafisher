import numpy as np
import cv2 as cv
from skimage.filters.thresholding import threshold_yen
from skimage.morphology import disk, binary_dilation, binary_erosion, remove_small_holes, remove_small_objects

from src.models import InputImage
from src.terminal_msg import msg, show_img


def removing_speckles(img: np.ndarray) -> np.ndarray:
    se = disk(2)
    dilated = binary_dilation(img, footprint=se)

    return remove_small_objects(remove_small_holes(dilated, connectivity=np.ndim(dilated), area_threshold=100))


def yen_th(img: np.ndarray) -> np.ndarray:
    """
    Runs a Yen-thresholding on given picture
    :param img: input image
    :return: Binary int picture
    """
    thresh = threshold_yen(img)
    binary = np.zeros(img.shape, dtype=int)
    binary[np.where(img > thresh)] = 1

    return binary


def yen_thresholding(input_img: InputImage) -> InputImage:
    """
    Stores the binary image in the object
    :param input_img: InputImage
    :return: InputImage with new .binary attribute
    """
    msg("Applying Yen-thresholding")

    th = yen_th(input_img.processed)

    input_img.binary = th
    msg("Stored binary image in object")

    return input_img

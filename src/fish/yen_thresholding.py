import numpy as np
from skimage.filters.thresholding import threshold_yen
from skimage.morphology import disk, binary_dilation, remove_small_holes, remove_small_objects

from src.models import InputImage
from src.terminal_msg import msg, show_img


def remove_speckles(img: np.ndarray) -> np.ndarray:
    min_area = img.size * 0.01  # Should be minimum 1% of the picture

    return remove_small_objects(remove_small_holes(img.astype(bool), min_area), min_area).astype(
        np.double)  # np.double for openCV to be able to open it


def yen_th(img: np.ndarray) -> np.ndarray:
    """
    Runs a Yen-thresholding on given picture
    :param img: input image
    :return: Binary int picture
    """
    thresh = threshold_yen(img)

    return (img > thresh).astype(np.double)  # np.double for openCV to be able to open it


def yen_thresholding(input_img: InputImage) -> InputImage:
    """
    Stores the binary image in the object
    :param input_img: InputImage
    :return: InputImage with new .binary attribute
    """
    msg("Applying Yen-thresholding")

    th = yen_th(input_img.processed)
    th = remove_speckles(th)
    th = th * input_img.well_props.mask.cropped
    input_img.binary = th.copy()
    input_img.processed = th.copy()
    msg("Stored binary image in object")

    return input_img

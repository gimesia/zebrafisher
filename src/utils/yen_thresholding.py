import numpy as np
from skimage.filters.thresholding import threshold_yen, threshold_isodata
from skimage.morphology import remove_small_holes, remove_small_objects

from .terminal_msg import msg
from ..models import InputImage


def remove_speckles(img: np.ndarray) -> np.ndarray:
    """
    Removes holes & object smaller than 1% of the original image
    :param img:
    :return:
    """
    min_area = img.size * 0.01  # Should be minimum 1% of the picture
    return remove_small_objects(remove_small_holes(img.astype(bool), min_area), min_area)


def yen_th(img: np.ndarray) -> np.ndarray:
    """
    Runs Yen-thresholding on given image

    :param img: input image
    :return: Binary int picture
    """
    thresh = threshold_yen(img)

    return img > thresh


def iso_th(img: np.ndarray) -> np.ndarray:
    """
    Runs Isodata-thresholding on given image

    :param img: input image
    :return: Binary int picture
    """
    thresh = threshold_isodata(img)

    return img > thresh


def yen_thresholding(input_img: InputImage, mask=None) -> InputImage:
    """
    Stores the binary image in the object

    :param input_img: InputImage
    :return: InputImage with new .binary attribute
    """
    msg("Applying Yen-thresholding")

    if mask is None:
        mask = input_img.well_props.mask.cropped

    th = yen_th(input_img.processed)
    th = remove_speckles(th)
    th = (th * mask).astype(float)

    input_img.binary = th.copy()
    input_img.processed = th.copy()

    msg("Stored binary image in object")
    return input_img

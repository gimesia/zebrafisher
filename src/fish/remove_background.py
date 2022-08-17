import numpy as np
from skimage.exposure import equalize_hist
from skimage.restoration import rolling_ball

from src.models import InputImage
from src.utils import msg


def remove_bg(img: np.ndarray) -> np.ndarray:
    """
    Reduces the background intensity of an image

    :param img: input image
    :return: image with background correction
    """
    bg = rolling_ball(img)
    return img - bg


def remove_background(input_img: InputImage) -> InputImage:
    msg("Removing background")
    no_bg = remove_bg(input_img.processed)
    input_img.processed = equalize_hist(no_bg)
    return input_img

import numpy as np
from skimage.exposure import equalize_hist
from skimage.restoration import rolling_ball
from skimage.util import invert

from src.models import InputImage
from src.utils import msg


def remove_bg(img: np.ndarray, inverted=False) -> np.ndarray:
    """
    Reduces the background intensity of an image

    :param img: input image
    :return: image with background correction
    """
    if not inverted:
        bg = rolling_ball(img)
        return img - bg
    else:
        image_inverted = invert(img)
        background_inverted = rolling_ball(image_inverted, radius=45)
        return invert(image_inverted - background_inverted)


def remove_background(input_img: InputImage, inverted=False) -> InputImage:
    msg("Removing background")
    no_bg = remove_bg(input_img.processed)
    input_img.processed = no_bg  # equalize_hist(no_bg)
    return input_img

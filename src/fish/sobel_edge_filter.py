import numpy as np
import cv2 as cv
from skimage.exposure import equalize_hist

from src.models import InputImage
from src.terminal_msg import msg


def sobel(img: np.ndarray) -> np.ndarray:
    """
    Performs Sobel filtering on a 2D grayscale image

    :param img: input image
    :return: Sobel (edge) filtered image
    """
    ddepth = cv.CV_16S
    grad_x = cv.Sobel(src=img, ddepth=ddepth, dx=1, dy=0, ksize=3)
    grad_y = cv.Sobel(src=img, ddepth=ddepth, dx=0, dy=1, ksize=3)

    abs_grad_x = cv.convertScaleAbs(grad_x)
    abs_grad_y = cv.convertScaleAbs(grad_y)

    grad = cv.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)
    eq_grad = equalize_hist(grad)  # Equalizing values for better separation
    return eq_grad


def sobel_edges(input_img: InputImage) -> InputImage:
    msg("Finding edges with Sobel filtering")
    input_img.processed = sobel(input_img.processed)
    return input_img

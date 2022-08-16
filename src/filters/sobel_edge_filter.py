import cv2 as cv
import numpy as np
from skimage.exposure import equalize_hist

from src.models import InputImage


def sobel(img: np.ndarray, equalized=True) -> np.ndarray:
    """
    Performs Sobel filtering on a 2D grayscale image, to find edges

    :param img: input image
    :param equalized: returns the equalized histogram, if set true
    :return: Sobel (edge) filtered image
    """
    ddepth = cv.CV_16S
    grad_x = cv.Sobel(src=img, ddepth=ddepth, dx=1, dy=0, ksize=3)
    grad_y = cv.Sobel(src=img, ddepth=ddepth, dx=0, dy=1, ksize=3)

    abs_grad_x = cv.convertScaleAbs(grad_x)
    abs_grad_y = cv.convertScaleAbs(grad_y)

    grad = cv.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)
    if equalized:
        eq_grad = equalize_hist(grad)  # Equalizing values for better separation
        return eq_grad
    else:
        return grad


def sobel_edges(input_img: InputImage) -> InputImage:
    input_img.processed = sobel(input_img.processed)
    return input_img

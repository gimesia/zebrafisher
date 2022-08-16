import cv2
import numpy as np

from src.models import InputImage


def sharpen_img(img: np.ndarray) -> np.ndarray:
    """
    Sharpens an image's details

    :param img: Input image
    :return: Sharpened image
    """
    kernel = np.array([[0, -1, 0],
                       [-1, 5, -1],
                       [0, -1, 0]])
    return cv2.filter2D(src=img, ddepth=-1, kernel=kernel)


def sharpen_image(input_img: InputImage) -> InputImage:
    """
    Stores processed (sharpened) image in InputImage object

    :param input_img: Object to be processed
    :return: Object with processed image
    """
    input_img.processed = sharpen_img(input_img.processed)
    return input_img

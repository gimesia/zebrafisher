import cv2 as cv
import numpy as np

from src.models import InputImage


def sharpen_img(img: np.ndarray) -> np.ndarray:
    kernel = np.array([[0, -1, 0],
                       [-1, 5, -1],
                       [0, -1, 0]])
    return cv.filter2D(src=img, ddepth=-1, kernel=kernel)


def sharpen_image(input_img: InputImage) -> InputImage:
    input_img.processed = sharpen_img(input_img.processed)
    return input_img

import numpy as np
from skimage.morphology import binary_closing, binary_dilation, binary_opening


def iterative_opening(img: np.ndarray, iterations: int, se: np.ndarray) -> np.ndarray:
    """
    Performs opening iteratively on an image

    :param img: input image
    :param iterations: times the opening done on the image
    :param se: structuring element
    :return: iteratively opened image
    """
    for i in range(iterations):
        img = binary_opening(img, se)
    return img


def iterative_closing(img: np.ndarray, iterations: int, se: np.ndarray):
    """
    Performs closing iteratively on an image

    :param img: input image
    :param iterations: times the closing done on the image
    :param se: structuring element
    :return: iteratively closed image
    """
    for i in range(iterations):
        img = binary_closing(img, se)
    return img


def iterative_dilation(img: np.ndarray, iterations: int, se: np.ndarray):
    """
    Performs dilation iteratively on an image

    :param img: input image
    :param iterations: times the dilation done on the image
    :param se: structuring element
    :return: iteratively dilated image
    """
    for i in range(iterations):
        img = binary_dilation(img, se)
    return img

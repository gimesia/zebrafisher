import cv2
import numpy as np

from skimage.color import gray2rgb
from src.utils import show_img
import cv2


def get_limits_of_object(img: np.ndarray):
    """
    Calculates the extreme points of a 2D image

    :param img: 2D image

    :rtype: coordinates of the endpoints (left, right, top, bottom)
    """
    img = img.copy()
    nz = img.nonzero()

    r_index = np.where(nz[1] == nz[1].max())
    right_max = (nz[1][r_index].max(), nz[0][r_index].max())

    b_index = np.where(nz[0] == nz[0].max())
    bottom_max = (nz[1][b_index].max(), nz[0][b_index].max())

    l_index = np.where(nz[1] == nz[1].min())
    left_max = (nz[1][l_index].min(), nz[0][l_index].min())

    t_index = np.where(nz[0] == nz[0].min())
    top_max = (nz[1][t_index].min(), nz[0][t_index].min())

    return left_max, right_max, top_max, bottom_max


def limits_marked(img: np.ndarray) -> np.ndarray:
    """
    Marks the limits on an image in each direction

    :param img: input image
    :rtype: image with marked endpoints
    """
    img = img.astype(float)
    img = gray2rgb(img)

    left_max, right_max, top_max, bottom_max = get_limits_of_object(img)

    cv2.circle(img, right_max, 8, (255, 0, 0), 3)
    cv2.circle(img, left_max, 8, (255, 255, 0), 3)
    cv2.circle(img, top_max, 8, (0, 255, 0), 3)
    cv2.circle(img, bottom_max, 8, (0, 0, 255), 3)

    return img

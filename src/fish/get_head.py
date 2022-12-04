import cv2
import numpy as np

from src.models import BoundingBox
from src.utils.terminal_msg import show_img


def get_side_img(img: np.ndarray, side: str) -> np.ndarray:
    """
    Crops the given image to the side given in the parameter (left or right)

    :param img: input image
    :param side: desired side
    :return: side of the input image
    """
    sides = get_two_sides_img(img)
    if side == "l":
        return sides[0]
    elif side == "r":
        return sides[1]


def get_two_sides_img(img: np.ndarray) -> [np.ndarray, np.ndarray]:
    """
    Divides the image into 2 halves lengthwise

    :rtype: tuple(np.ndarray, np.ndarray)
    """
    if should_be_rotated(img):
        img = np.transpose(img)
    h, w = img.shape
    ch, cw = int(h / 2), int(w / 2)

    left_side = img[:, 0:cw]
    right_side = img[:, cw:]
    return [left_side, right_side]


def get_two_sides_bbox(bbox: BoundingBox) -> (BoundingBox, BoundingBox):
    """
    Divides the bounding box into 2 halves lengthwise

    :rtype: tuple(BoundingBox,BoundingBox)
    """
    shape = (bbox.x2 - bbox.x1, bbox.y2 - bbox.y1)
    rotated = shape[0] > shape[1]
    if rotated:
        bbox = BoundingBox(bbox.y1, bbox.x1, bbox.y2, bbox.x2)
    h, w = shape
    ch, cw = int(h / 2), int(w / 2)

    if not rotated:
        left_side = BoundingBox(bbox.x1, bbox.y1, cw, bbox.y2)
        right_side = BoundingBox(cw, bbox.y1, bbox.x2, bbox.y2)
    else:
        left_side = BoundingBox(bbox.y1, bbox.x1, bbox.y2, cw)
        right_side = BoundingBox(bbox.y1, cw, bbox.y2, bbox.x2)
    return left_side, right_side


def mean_of_col_sums(bin_img: np.ndarray) -> float:
    """
    Calculates of the average length of the columns
    :rtype: float
    """
    summed = np.sum(bin_img, axis=0)
    return np.mean(summed[summed != 0])


def should_be_rotated(img: np.ndarray) -> bool:
    """
    Returns True if height of image is greater than its width

    :rtype: bool
    """
    if img.shape[0] > img.shape[1]:
        return True
    return False


def get_head(bin_img: np.ndarray) -> (np.ndarray, str):
    """
    Identifies the side & image of the head part

    :rtype: (np.ndarray, str)
    :return:  image of head, side of head
    """
    l, r = get_two_sides_img(bin_img)
    l_m, r_m = mean_of_col_sums(l), mean_of_col_sums(r)
    return (l, 'l') if l_m > r_m else (r, 'r')


if __name__ == '__main__':
    pass

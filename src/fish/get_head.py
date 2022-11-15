import cv2
import numpy as np

from src.models import BoundingBox
from src.utils.terminal_msg import show_img


def get_two_sides_img(img: np.ndarray) -> [np.ndarray, np.ndarray]:
    if should_be_rotated(img):
        img = np.transpose(img)
    h, w = img.shape
    ch, cw = int(h / 2), int(w / 2)

    left_side = img[:, 0:cw]
    right_side = img[:, cw:]
    return left_side, right_side


def get_two_sides_bbox(bbox: BoundingBox) -> [BoundingBox, BoundingBox]:
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
    return np.mean(np.sum(bin_img, axis=0))


def should_be_rotated(img: np.ndarray) -> bool:
    return img.shape[0] > img.shape[1]


def get_head(bin_img: np.ndarray) -> (np.ndarray,str):
    l, r = get_two_sides_img(bin_img)
    l_m, r_m = mean_of_col_sums(l), mean_of_col_sums(r)
    return (l, 'l') if l_m > r_m else (r, 'r')


if __name__ == '__main__':
    # WIP
    im = cv2.imread('output.png', 0)
    a = get_head(im)
    print(a[1])

# !!! TODO: UNFINISHED

import math
import numpy as np
from skimage.measure import profile_line
from src.InputImage import InputImage, EXAMPLE_IMG
from src.terminal_msg import msg, show_img
from skimage.filters import threshold_triangle
import cv2 as cv


def get_inner_roi(input_img: InputImage):
    msg("Getting the inner region of interest")
    show_img(input_img.processed)

    threshold_level, img = cv.threshold(input_img.processed, 0, 255, cv.THRESH_TRIANGLE + cv.THRESH_BINARY);
    # threshold_level = threshold_triangle(input_img.processed, nbins=256)
    print((img))
    show_img(img)
    print(threshold_level)

    return input_img


# TODO! Ezt azért le kell ellenőrizni még
def get_inner_circle(input_img: InputImage) -> [np.ndarray, np.ndarray]:
    center_x = math.floor(input_img.width / 2)
    center_y = math.floor(input_img.height / 2)
    theta = np.arange(0, 316, 45)  # 316 instead of 315 in order to include 315
    radius = input_img.width / 2

    [start_x, start_y, end_x, end_y] = get_coordinates(center_x, center_y, theta, radius)

    o = 1

    # It's the second dim in MATLAB, but there the dims are (1,8) whereas here it's (8,)
    for i in range(start_x.shape[0]):
        x_line = [start_x[i], end_x[i]]
        y_line = [start_y[i], end_y[i]]

        # Necces, szerintem nem fog működni, de nem tudom tesztelni MATLAB on
        p = profile_line(input_img.processed, x_line, y_line)
        print(f"P[{i}]:\n{p}")

    # TODO!!
    return None


def get_coordinates(center_x: int, center_y: int, theta: np.ndarray, radius: float):
    x = radius * np.cos(np.deg2rad(theta)) + center_x
    y = radius * np.sin(np.deg2rad(theta)) + center_y

    end_pos_x = np.zeros(8)
    end_pos_y = np.zeros(8)
    start_pos_x = np.full(8, center_x)
    start_pos_y = np.full(8, center_y)

    # IDK what this loop does!
    j = 0  # Originally 1 in MATLAB, because it isn't 0 start-index based
    for i in range(x.shape[0]):
        if i < 31:
            end_pos_x[j] = x[i]
            end_pos_y[j] = y[i]
            j += 1

    return [start_pos_x, start_pos_y, end_pos_x, end_pos_y]


if __name__ == '__main__':
    img = EXAMPLE_IMG
    get_inner_roi(img)

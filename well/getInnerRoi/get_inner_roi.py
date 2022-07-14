# !!! TODO: UNFINISHED

import math
import numpy as np

from InputImage import InputImage


def get_inner_roi(input_img: InputImage):
    return input_img


# TODO! Ezt azért le kell ellenőrizni még
def get_inner_circle(input_img: InputImage):
    center_x = math.floor(input_img.width / 2)
    center_y = math.floor(input_img.height / 2)
    theta = np.arange(0, 316, 45)  # 316 instead of 315 in order to include 315
    radius = input_img.width / 2

    [start_pos_x, start_pos_y, end_pos_x, end_pos_y] = get_coordinates(center_x, center_y, theta, radius)

    o = 1  # What could this be?  ¯\_(ツ)_/¯

    for i in range(start_pos_x[1]):
        x_line = [start_pos_x[i], end_pos_x[i]]
        y_line = [start_pos_y[i], end_pos_y[i]]

    return


def get_coordinates(center_x, center_y, theta, radius):
    x = radius * np.cos(np.deg2rad(theta)) + center_x
    y = radius * np.sin(np.deg2rad(theta)) + center_y

    j = 1

    end_pos_x = np.zeros(8)
    end_pos_y = np.zeros(8)
    start_pos_x = np.full(8, center_x)
    start_pos_y = np.full(8, center_y)

    for i in range(x.shape[1]):
        if i < 31:
            end_pos_x[j] = x[i]
            end_pos_y[j] = y[i]
            j += 1

    return [start_pos_x, start_pos_y, end_pos_x, end_pos_y]

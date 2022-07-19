import numpy as np

from circle_fit import hyper_fit
from math import pi
from src.InputImage import InputImage
from src.terminal_msg import msg


def create_circle_mask(input_img: InputImage) -> InputImage:
    msg("Create circle mask for image")
    center = input_img.well_props.center
    radius = input_img.well_props.radius
    size = (input_img.width, input_img.height)

    input_img.well_props.mask = circle_mask(center, size, radius)
    return input_img


def circle_mask(center: tuple[int, int], size: tuple[int, int], radius: int) -> np.ndarray:
    msg("Creating mask")
    x, y = center[0], center[1]

    width, height = size[0], size[1]

    theta = np.arange(0, 2 * pi + (pi / 50), pi / 50)

    x_unit = radius * np.cos(theta) + x
    y_unit = radius * np.sin(theta) + y

    # An array that has both x and y coords
    concatenated = np.dstack((x_unit, y_unit))[0]

    [x_fit, y_fit, r_fit, residue] = hyper_fit(concatenated)

    [x, y] = np.meshgrid(np.arange(-(x_fit - 1), (width - x_fit)), np.arange(-(y_fit - 1), (height - y_fit)))

    mask = (np.power(x, 2) + np.power(y, 2) <= (r_fit ** 2))

    return mask


# For testing
if __name__ == "__main__":
    a = circle_mask((100, 100), (200, 200), 70)
    a = np.uint8(a)
    np.savetxt("mask.csv", a, delimiter=",")

    from numpy import genfromtxt

    b = np.uint8(genfromtxt('mask_m.csv', delimiter=','))

    false_count = 0
    for i in range(a.shape[0]):
        for j in range(a.shape[1]):
            res = a[i][j] == b[i][j]
            if not res:
                false_count += 1
    print(false_count)

# !!! TODO: UNFINISHED


from math import pi

import numpy as np
from circle_fit import hyper_fit

from src.terminal_msg import msg


def create_circle_mask(center: tuple[int, int], size: tuple[int, int], r: int) -> np.ndarray:
    # msg("Create circle mask")
    x, y = center[0], center[1]

    width, height = size[0], size[1]

    theta = np.arange(0, 2 * pi + (pi / 50), pi / 50)

    x_unit = r * np.cos(theta) + x
    y_unit = r * np.sin(theta) + y

    # An array that has both x and y coords
    concatenated = np.dstack((x_unit, y_unit))[0]

    [x_fit, y_fit, r_fit, residue] = hyper_fit(concatenated)

    [x, y] = np.meshgrid(np.arange(-(x_fit - 1), (width - x_fit)), np.arange(-(y_fit - 1), (height - y_fit)))

    mask = (np.power(x, 2) + np.power(y, 2) <= (r_fit ** 2))

    return mask


if __name__ == "__main__":
    a = create_circle_mask((10, 10), (20, 20), 5)
    print(a)

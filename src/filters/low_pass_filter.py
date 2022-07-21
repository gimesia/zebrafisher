"""
TODO: add ref
"""

import numpy as np


def low_pass_filter(size: tuple[int, int], cutoff: float, n: int):
    if cutoff < 0 or cutoff > 0.5:
        raise Exception("cutoff frequency must be between 0 and 0.5")

    if n % 1 != 0 or n < 1:
        raise Exception("n must be an integer >= 1")

    [rows, cols] = size

    if cols % 2 == 0:
        x_range = np.arange((-cols / 2), cols / 2) / cols
    else:
        x_range = np.arange((-(cols - 1) / 2), (cols - 1) / 2) / (cols - 1)

    if rows % 2 == 0:
        y_range = np.arange((-rows / 2), rows / 2) / rows
    else:
        y_range = np.arange((-(rows - 1) / 2), (rows - 1) / 2) / (rows - 1)

    [x, y] = np.meshgrid(x_range, y_range)

    radius = np.sqrt(x ** 2 + y ** 2)

    return np.fft.ifftshift(1 / (1 + (radius / cutoff) ** (2 * n)))


if __name__ == '__main__':
    lpf = low_pass_filter((1040, 1388), 0.25, 100)
    a = np.genfromtxt('lpf.csv', delimiter=",")

    diff = np.abs(lpf - a)

    b = (diff == 0)

    print(b.shape == (1040, 1388))

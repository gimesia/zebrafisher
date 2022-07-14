# !!! TODO: UNFINISHED


from math import pi

import numpy as np


def create_cicrle_mask(center: tuple[int, int], size: tuple[int, int], r: int):
    x = center[0]
    y = center[1]

    th = np.arange(0, pi / 50, 2 * pi)

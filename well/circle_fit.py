# !!! TODO: UNFINISHED, but could use 'circle-fit.hiper_fit'

import numpy as np

def circle_fit(x: np.ndarray, y: np.ndarray):
    """
    :param x: vector of x coordinates
    :param y: vector of y coordinates

    :returns c_x: X coordinate of the center
    :returns c_y: Y coordinate of the center
    :returns R: radius of the circle
    """

    x = x.reshape(-1, 1)
    y = y.reshape(-1, 1)

    a = []

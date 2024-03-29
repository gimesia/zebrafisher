# from circle_fit import hyper_fit
from math import pi

import numpy as np

from src.models import InputImage
from src.utils.terminal_msg import msg
from .circle_fit import hyper_fit


def create_circle_mask(input_img: InputImage, correction=0) -> InputImage:
    """
    Sets the OG (circle) mask for well

    :param input_img: Input image without 'well_props.mask.og'
    :param correction: pixels subtracted from the radius
    :return: Input image with 'well_props.mask.og'
    """
    msg("Creating circle mask for well")

    try:
        center = input_img.well_props.center
        radius = input_img.well_props.radius
        size = (input_img.height, input_img.width)
    except():
        print(f"center: {center}, radius: {radius}, img size: {size}")
        raise Exception("Cannot make circle mask without required parameters! (center, radius, img size")

    input_img.well_props.mask.og = circle_mask(center, size, radius, correction)

    msg("Circle mask for well created")
    return input_img


def circle_mask(center: tuple[int, int], size: tuple[int, int], radius: int, correction=0) -> np.ndarray:
    """
    Creates a circle of True values with given :param center, :param radius in an image with given :param size

    :param center: Center of the mask
    :param size: Size of the containing image
    :param radius: Radius of circle
    :param correction: pixels subtracted from the radius
    :return: Circle masked image
    """
    x, y = center[0], center[1]
    height, width = size[0], size[1]

    theta = np.arange(0, 2 * pi + (pi / 50), pi / 50)

    subtracted_radius = radius - correction

    x_unit = subtracted_radius * np.cos(theta) + x
    y_unit = subtracted_radius * np.sin(theta) + y

    # An array that has both x and y coords
    concatenated = np.dstack((x_unit, y_unit))[0]

    [x_fit, y_fit, r_fit, residue] = hyper_fit(concatenated)

    [x, y] = np.meshgrid(np.arange(-(x_fit - 1), (width - x_fit + 1)), np.arange(-(y_fit - 1), (height - y_fit + 1)))

    mask = (np.power(x, 2) + np.power(y, 2) <= (r_fit ** 2))
    return mask.astype(np.uint8)

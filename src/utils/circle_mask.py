import numpy as np

# from circle_fit import hyper_fit
from math import pi
from src.models import InputImage
from src.utils.terminal_msg import msg
from .circle_fit import hyper_fit


def create_circle_mask(input_img: InputImage) -> InputImage:
    """
    Sets the OG (circle) mask for well

    :param input_img: Input image without 'well_props.mask.og'
    :return: Input image with 'well_props.mask.og'
    """
    msg("Creating mask for well")
    try:
        center = input_img.well_props.center
        radius = input_img.well_props.radius
        size = (input_img.height, input_img.width)
    except():
        raise Exception("Cannot make circle mask without required parameters! (center, radius, img size")

    input_img.well_props.mask.og = circle_mask(center, size, radius)
    return input_img


def circle_mask(center: tuple[int, int], size: tuple[int, int], radius: int) -> np.ndarray:
    """

    :param center: Center of the mask
    :param size: Size of the containing image
    :param radius: Radius of circle
    :return: Circle masked image
    """
    x, y = center[0], center[1]
    height, width = size[0], size[1]

    theta = np.arange(0, 2 * pi + (pi / 50), pi / 50)

    x_unit = radius * np.cos(theta) + x
    y_unit = radius * np.sin(theta) + y

    # An array that has both x and y coords
    concatenated = np.dstack((x_unit, y_unit))[0]

    [x_fit, y_fit, r_fit, residue] = hyper_fit(concatenated)

    [x, y] = np.meshgrid(np.arange(-(x_fit - 1), (width - x_fit + 1)), np.arange(-(y_fit - 1), (height - y_fit + 1)))

    mask = (np.power(x, 2) + np.power(y, 2) <= (r_fit ** 2)).astype(int)

    """if mask.shape != size:
        raise Exception(f"The mask and the image are not the same dimensions\n"
                        f"Mask shape: {mask.shape}\n"
                        f"OG shape: {size}")"""

    return mask


if __name__ == "__main__":
    pass

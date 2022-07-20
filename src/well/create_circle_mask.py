import numpy as np

from circle_fit import hyper_fit
from math import pi
from src.InputImage import InputImage
from src.terminal_msg import msg


def create_circle_mask(input_img: InputImage) -> InputImage:
    msg("Create circle mask for image")
    center = input_img.well_props.center
    radius = input_img.well_props.radius
    size = (input_img.height, input_img.width)

    input_img.well_props.mask.og = circle_mask(center, size, radius)
    return input_img


def circle_mask(center: tuple[int, int], size: tuple[int, int], radius: int) -> np.ndarray:
    msg("Creating mask")

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


# For testing
if __name__ == "__main__":
    pass

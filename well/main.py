# !!! TODO: UNFINISHED

from InputImage import InputImage
from terminal_msg import msg
from well.well_hough_transform import well_hough_transformation


def main(input_img: InputImage) -> InputImage:
    # Finding the properties of the
    if input_img.height >= input_img.width:
        input_img.wellProps.min_circle = 0 if (input_img.height - 400) < 0 else input_img.height - 400
        input_img.wellProps.max_circle = input_img.height
    else:
        input_img.wellProps.min_circle = 0 if (input_img.width - 400) < 0 else input_img.width - 400
        input_img.wellProps.max_circle = input_img.width

    msg("Well (minRadius/ maxRadius)", f"{input_img.wellProps.min_circle} / {input_img.wellProps.max_circle}")

    # Finding well via Hough-transformation
    input_img = well_hough_transformation(input_img)

    #
    if input_img.wellProps.radius < input_img.height / 2 * .8:
        pass

    return input_img

import cv2 as cv
import numpy as np
from skimage.color import gray2rgb, rgb2gray

from src.models import InputImage
from src.utils.terminal_msg import msg


def get_circle_limits(input_img: InputImage) -> [int, int]:
    """

    :param input_img:
    :type input_img:
    :return:
    :rtype:
    """
    if input_img.height >= input_img.width:
        min_circle = 0 if (input_img.height - 400) < 0 else input_img.height - 400
        max_circle = input_img.height
    else:
        min_circle = 0 if (input_img.width - 400) < 0 else input_img.width - 400
        max_circle = input_img.width

    return [min_circle, max_circle]


def well_hough_transformation(input_img: InputImage):
    msg("Hough-transformation for the well")
    image = input_img.processed

    [min_circle, max_circle] = get_circle_limits(input_img)

    # Apply blur
    image = cv.medianBlur(image, 5)

    # Use Hough transform (might have to change params)
    circles = cv.HoughCircles(image, cv.HOUGH_GRADIENT, 0.99, 100, param1=50, param2=30,
                              minRadius=int(min_circle / 2),
                              maxRadius=int(max_circle / 2))

    # Rounding values for int16
    circles = np.uint16(np.around(circles))

    # Selecting first circle
    try:
        circle = circles[0][0]
    except():
        input_img.well_props.is_well = False
        return input_img

    """ FROM line 28-35 is for visual testing, will need to comment it out"""
    # Converting back to RGB to be able to put colorful indicators for center and line
    """
    c_image = gray2rgb(image)
    # draw the outer circle
    cv.circle(c_image, (circle[0], circle[1]), circle[2], (0, 255, 0), 2)
    # draw the center
    cv.circle(c_image, (circle[0], circle[1]), 1, (0, 100, 255), 4)
    # input_img.processed = c_image
    """
    # Storing circle radius in input object
    input_img.well_props.radius = circle[2]
    # Storing circle center in input object
    input_img.well_props.center = (circle[0], circle[1])  # Storing result in the input object

    return input_img

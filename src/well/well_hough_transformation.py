import cv2 as cv
import numpy as np

from ..models import InputImage
from ..utils import msg


def get_circle_limits(input_img: InputImage) -> [int, int]:
    """
    Calculates the minimum & maximum estimated values for the well

    :param input_img: input image object to calculate from
    :return: min & max parameter
    """
    if input_img.height >= input_img.width:
        min_circle = 0 if (input_img.height - 400) < 0 else input_img.height - 400
        max_circle = input_img.height
    else:
        min_circle = 0 if (input_img.width - 400) < 0 else input_img.width - 400
        max_circle = input_img.width

    return [min_circle, max_circle]


def hough_transformation(img: np.ndarray, min_r: int, max_r: int, draw_circle=False):
    image = cv.medianBlur(img, 3)  # Apply blur

    # Use Hough transform (might have to change params)
    circles = cv.HoughCircles(image, cv.HOUGH_GRADIENT, 0.99, 100, param1=50, param2=30,
                              minRadius=int(min_r / 2),
                              maxRadius=int(max_r / 2))

    if len(circles) == 0:
        print("No circles found!")
    return circles


def well_hough_transformation(input_img: InputImage):
    """
    Searches for a circle for in the 'InputImage.processed' image

    :param input_img: input image
    :return: the same input image with .well_props.center & .well_props.radius attributes
    """
    msg("Hough-transformation for the well")

    [min_circle, max_circle] = get_circle_limits(input_img)

    circles = hough_transformation(input_img.processed, min_circle, max_circle)
    circles = np.uint16(np.around(circles))  # Rounding values for int16

    # Selecting first circle
    try:
        circle = circles[0][0]
    except():
        raise Exception("No well found!")

    """ FROM line 28-35 is for visual testing, will need to comment it out"""
    """
    c_image = gray2rgb(image)  # Converting back to RGB to be able to put colorful indicators for center and line
    cv.circle(c_image, (circle[0], circle[1]), circle[2], (0, 255, 0), 2)  # draw the outer circle
    cv.circle(c_image, (circle[0], circle[1]), 1, (0, 100, 255), 4)  # draw the center
    show_img(c_image)
    """

    input_img.well_props.radius = circle[2]  # Storing circle radius in input object
    input_img.well_props.center = (circle[0], circle[1])  # Storing circle center in input object

    msg("Hough-transformation finished")
    return input_img

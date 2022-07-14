import numpy as np
import cv2 as cv
from skimage.color import rgb2gray, gray2rgb

from InputImage import InputImage
from terminal_msg import msg


def well_hough_transformation(input_img: InputImage):
    image = input_img.processed
    msg("Image ready for Hough-transformation", image)

    # Apply blur
    image = cv.medianBlur(image, 5)
    msg("Applied median blur to image", image)

    # Use Hough transform (might have to change params)
    circles = cv.HoughCircles(image, cv.HOUGH_GRADIENT, 0.99, 100, param1=50, param2=30,
                              minRadius=int(input_img.well_props.min_circle / 2),
                              maxRadius=int(input_img.well_props.max_circle / 2))

    # Rounding values for int16
    circles = np.uint16(np.around(circles))

    # Selecting first circle
    circle = circles[0][0]
    msg("Circle:", circle)

    # Converting back to RGB to be able to put colorful indicators for center and line
    c_image = gray2rgb(image)

    # draw the outer circle
    cv.circle(c_image, (circle[0], circle[1]), circle[2], (0, 255, 0), 2)
    # draw the center
    cv.circle(c_image, (circle[0], circle[1]), 1, (0, 100, 255), 4)

    # Storing circle properties in InputImage object
    input_img.well_props.radius, input_img.well_props.center = circle[2], (circle[0], circle[1])

    # Storing result in the input object
    input_img.processed = c_image  # Nem biztos, hogy kell

    return input_img


if __name__ == "__main__":
    img = InputImage("preProcessing/zf.png")
    img.well_props.min_circle = 0
    img.well_props.max_circle = 200
    well_hough_transformation(img)

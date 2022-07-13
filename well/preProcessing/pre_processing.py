import numpy as np
import cv2 as cv
from skimage.morphology import disk

from InputImage import InputImage
from terminal_msg import show_img
from well.preProcessing.illumination_correction import illumination_correction


def pre_processing(input_img: InputImage) -> InputImage:
    # cannot specify 'n' from the original, the number of line structuring elements used to approximate the disk shape
    structuring_element = disk(15)

    # translation of imclose() (maybe could use scipy.grey_closing())
    closed_img = cv.morphologyEx(input_img.processed, cv.MORPH_CLOSE, structuring_element)
    input_img.processed = closed_img

    # Illumination correction
    input_img = illumination_correction(input_img)

    # TODO! input_img = fibermetric(filteredImg, 113, 'ObjectPolarity', 'dark');

    return input_img


if __name__ == "__main__":
    res = InputImage("zf.png")
    res = pre_processing(res)
    show_img(res.processed)


import numpy as np
import cv2 as cv

from src.fish import find_fish_props
from src.models.InputImage import InputImage
from src.well.find_well_props import find_well_props
from terminal_msg import msg, show_img
from src.filters.normalize_intensity_range import normalize_intensity_range


def image_processing_pipeline(filename) -> InputImage:
    msg("Start image processing pipeline")
    input_img = InputImage(filename)

    # Handled this in the constructor of InputImage!!
    # Storing height & width based on the shape of the array (pixels)
    input_img.height, input_img.width = np.shape(input_img.processed)[0], np.shape(input_img.processed)[1]

    # Normalizing intensity
    input_img.processed = cv.normalize(src=input_img.processed, dst=None, alpha=0, beta=255,
                                       norm_type=cv.NORM_MINMAX)

    # Converting back to unsigned integers Double -> UInt8
    input_img.processed = np.uint8(input_img.processed)

    input_img = find_well_props(input_img)

    if not input_img.well_props.is_well:
        raise Exception("No well was found")
    else:
        msg("FOUND WELL!")

    input_img = find_fish_props(input_img)
    show_img(input_img.processed)

    if not input_img.fish_props.is_fish:
        raise Exception("No fish was found")
    else:
        msg("FOUND FISH!")

    return input_img


if __name__ == '__main__':
    res = image_processing_pipeline("zf1.jpg")
    print(res.__dict__)
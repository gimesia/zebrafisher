import numpy as np

from InputImage import InputImage
from src.well.find_well_props import find_well_props
from terminal_msg import msg, show_img
from src.well.normalize_intensity_range import normalize_intensity_range

image_width: int
image_height: int


def image_processing_pipeline(filename) -> InputImage:
    msg("Start image processing pipeline")
    input_img = InputImage(filename)

    """ Handled this in the constructor of InputImage!!
        # Checking for RGB by looking for 3rd dimension besides x,y -> colors
    is_rgb = (np.shape(input_img.processed)[2] == 3)
    # If rgb -> conversion to grayscale image
    if is_rgb:
        input_img.processed = rgb2gray(input_img.processed)

        msg("RGB -> Gray image", input_img.processed)"""

    # Storing height & width based on the shape of the array (pixels)
    input_img.height, input_img.width = np.shape(input_img.processed)[0], np.shape(input_img.processed)[1]

    # Normalizing intensity
    input_img.processed = normalize_intensity_range(input_img.processed, (0, 255))

    # Converting back to unsigned integers Double -> UInt8
    input_img.processed = np.uint8(input_img.processed)

    input_img = find_well_props(input_img)

    return input_img


if __name__ == '__main__':
    res = image_processing_pipeline("zf.png")
    show_img(res.processed, "Testy")
    # np.savetxt("P.__playground", ans, delimiter=",")

import numpy as np
import cv2 as cv

from InputImage import InputImage
from terminal_msg import msg, show_img
from well.normalize_intensity_range import normalize_intensity_range
from skimage.color import rgb2gray
from well.main import main as find_well_props

image_width: int
image_height: int


def image_processing_pipeline(filename) -> InputImage:
    input_img = InputImage(filename)

    """    # Checking for RGB by looking for 3rd dimension besides x,y -> colors
    is_rgb = (np.shape(input_img.processed)[2] == 3)
    # If rgb -> conversion to grayscale image
    if is_rgb:
        input_img.processed = rgb2gray(input_img.processed)

        msg("RGB -> Gray image", input_img.processed)"""

    # Storing height & width based on the shape of the array (pixels)
    input_img.height, input_img.width = np.shape(input_img.processed)[0], np.shape(input_img.processed)[1]

    msg("Image (height/width):", f"{input_img.height} / {input_img.width}")

    # Normalizing intensity
    input_img.processed = normalize_intensity_range(input_img.processed, (0, 255))

    msg("Normalized intensity:", input_img.processed)

    # Converting back to unsigned integers
    input_img.processed = np.uint8(input_img.processed)

    # Nem értem miért, de így van a MATLAB-ban
    # msg("Double -> UInt8:", input_img.processed)

    input_img = find_well_props(input_img)

    return input_img


if __name__ == '__main__':
    res = image_processing_pipeline("zf.png")
    show_img(res.processed, "Testy")
    # np.savetxt("P.__playground", ans, delimiter=",")

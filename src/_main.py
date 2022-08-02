import numpy as np

from src.models.InputImage import InputImage
from src.well.find_well_props import find_well_props
from terminal_msg import msg, show_img
from src.filters.normalize_intensity_range import normalize_intensity_range

image_width: int
image_height: int


def image_processing_pipeline(filename) -> InputImage:
    msg("Start image processing pipeline")
    input_img = InputImage(filename)

    # Handled this in the constructor of InputImage!!
    # Storing height & width based on the shape of the array (pixels)
    input_img.height, input_img.width = np.shape(input_img.processed)[0], np.shape(input_img.processed)[1]

    # Normalizing intensity
    input_img.processed = normalize_intensity_range(input_img.processed, (0, 255))

    # Converting back to unsigned integers Double -> UInt8
    input_img.processed = np.uint8(input_img.processed)

    input_img = find_well_props(input_img)

    if not input_img.well_props.is_well:
        # save_empty_measures()
        pass
    else:
        pass
    return input_img


if __name__ == '__main__':
    res = image_processing_pipeline("zf.jpg")
    show_img(res.well_props.mask.cropped_masked, "Testy")
    #    np.savetxt("P.csv", res.og, delimiter=",")
    # res = np.genfromtxt("P.csv",delimiter=",")
    print(vars(res.well_props))

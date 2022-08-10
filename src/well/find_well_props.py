import numpy as np

from src.models import InputImage, BoundingBox
from src.terminal_msg import msg
from src.well.create_circle_mask import create_circle_mask
from src.well.unused.get_inner_roi import get_inner_roi
from src.well.get_bounding_box_coords import get_bounding_box_coords
from src.well.is_empty_img import is_empty_img
from src.well.unused.pre_processing import pre_processing
from src.well.well_hough_transform import well_hough_transformation


def find_well_props(input_img: InputImage) -> InputImage:
    msg("Searching well properties")
    # Finding the properties of the well, might be wrong but this is how it was in the MATLAB script
    if input_img.height >= input_img.width:
        input_img.well_props.min_circle = 0 if (input_img.height - 400) < 0 else input_img.height - 400
        input_img.well_props.max_circle = input_img.height
    else:
        input_img.well_props.min_circle = 0 if (input_img.width - 400) < 0 else input_img.width - 400
        input_img.well_props.max_circle = input_img.width

    # Finding well via Hough-transformation
    input_img = well_hough_transformation(input_img)

    # If circle was found
    if input_img.well_props.center is not None:
        # If the well radius's length is not satisfactory (WAS IN MATLAB)
        if input_img.well_props.radius < input_img.height / 2 * .8:
            # Pre-processes image & gets ROI if the length of the radius is not satisfactory
            input_img = pre_processing(input_img)
            input_img.well_props.mask.og = get_inner_roi(input_img)
        else:
            input_img = create_circle_mask(input_img)
    # Pre-processes image & gets ROI if the Hough-transformation cannot find a circle
    else:
        input_img = pre_processing(input_img)
        input_img.well_props.mask = get_inner_roi(input_img)

    if is_empty_img(input_img.well_props.mask.og) or (input_img.well_props.mask is None):
        input_img.well_props.is_well = False
    else:
        input_img.well_props.is_well = True

        [x1, y1, x2, y2] = get_bounding_box_coords(input_img.well_props.mask.og)  # Getting boundaries of the mask
        input_img.well_props.bounding_box = BoundingBox(x1, y1, x2, y2)

        input_img.well_props.mask.cropped = input_img.well_props.mask.og[x1:x2 + 1, y1:y2 + 1]  # Creating cropped mask

        input_img.well_props.mask.masked = \
            np.uint8(input_img.well_props.mask.og) * np.uint8(input_img.processed)  # Applying mask to OG image

        input_img.well_props.mask.cropped_masked = \
            input_img.well_props.mask.masked[x1:x2 + 1, y1:y2 + 1]  # Cropping masked image

        input_img.processed = input_img.well_props.mask.cropped_masked

    return input_img

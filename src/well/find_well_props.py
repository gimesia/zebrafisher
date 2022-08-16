import numpy as np
from skimage.color import rgb2gray

from src.models import InputImage
from src.utils.terminal_msg import msg, show_img
from src.utils import create_circle_mask, is_empty_img, get_bounding_box_obj
from src.well import well_hough_transformation


def find_well_props(input_img: InputImage) -> InputImage:
    msg("Searching well properties")
    # Finding well via Hough-transformation
    input_img = well_hough_transformation(input_img)

    input_img = create_circle_mask(input_img)

    input_img = create_remaining_well_masks(input_img)

    return input_img


def create_remaining_well_masks(input_img: InputImage) -> InputImage:
    if is_empty_img(input_img.well_props.mask.og) or (input_img.well_props.mask is None):
        input_img.well_props.is_well = False
    else:
        input_img.well_props.is_well = True

        # Getting boundaries of the mask
        bbox = get_bounding_box_obj(input_img.well_props.mask.og)
        input_img.well_props.bounding_box = bbox
        # Creating cropped mask
        input_img.well_props.mask.cropped = input_img.well_props.mask.og[bbox.x1:bbox.x2 + 1, bbox.y1:bbox.y2 + 1]

        # Applying mask to OG image
        masked = input_img.well_props.mask.og.astype(np.uint8) * rgb2gray(input_img.og.astype(np.uint8))
        # Storing masked images
        input_img.well_props.mask.masked = masked
        input_img.well_props.mask.cropped_masked = masked[bbox.x1:bbox.x2 + 1, bbox.y1:bbox.y2 + 1]

        # Storing result
        input_img.processed = input_img.well_props.mask.cropped_masked.copy()

    return input_img

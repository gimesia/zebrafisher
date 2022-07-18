# !!! TODO: UNFINISHED

from src.InputImage import InputImage
from src.terminal_msg import msg
from src.well.getInnerRoi.get_inner_roi import get_inner_roi
from src.well.preProcessing.pre_processing import pre_processing
from src.well.well_hough_transform import well_hough_transformation


def find_well_props(input_img: InputImage) -> InputImage:
    msg("Find well props")

    # Finding the properties of the well, might be wrong but this is how it was in the MATLAB script
    if input_img.height >= input_img.width:
        input_img.well_props.min_circle = 0 if (input_img.height - 400) < 0 else input_img.height - 400
        input_img.well_props.max_circle = input_img.height
    else:
        input_img.well_props.min_circle = 0 if (input_img.width - 400) < 0 else input_img.width - 400
        input_img.well_props.max_circle = input_img.width

    # Finding well via Hough-transformation
    input_img = well_hough_transformation(input_img)

    if input_img.well_props.radius < input_img.height / 2 * .8:
        input_img = pre_processing(input_img)
        input_img.well_props.mask = get_inner_roi(input_img)
    else:
        mask = create_circle_mask()
    return input_img

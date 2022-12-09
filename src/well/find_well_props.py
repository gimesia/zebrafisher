from . import process_well_mask, well_hough_transformation
from ..models import InputImage
from ..utils import msg


def find_well_props(input_img: InputImage) -> InputImage:
    """
    Finds the properties of the well, then stores it in the input object

    :param input_img: input image object
    :return: input image object with 'well_props'
    """
    msg("Searching for well properties")

    input_img = well_hough_transformation(input_img)

    input_img = process_well_mask(input_img)

    return input_img

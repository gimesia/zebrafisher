from src.models import InputImage
from src.utils import create_circle_mask
from src.utils.terminal_msg import msg
from src.well import well_hough_transformation
from src.well.process_well_mask import process_well_mask


def find_well_props(input_img: InputImage) -> InputImage:
    """
    Finds the properties of the well, then stores it in the input object

    :param input_img: input image object
    :return: input image object with 'well_props'
    """
    msg("Searching for well properties")

    input_img = well_hough_transformation(input_img)

    input_img = process_well_mask(input_img)

    msg("Finished searching for well properties")
    return input_img

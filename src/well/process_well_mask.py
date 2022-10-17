from skimage.morphology import binary_dilation, disk

from src.models import InputImage
from src.utils import is_empty_img, msg, get_bounding_box_obj, create_circle_mask


def process_well_mask(input_img: InputImage) -> InputImage:
    """
     Creates masks of the well, stores it in the input object

    :param input_img: input image object
    :return: input image object with 'well_props.mask'
    """

    input_img = create_circle_mask(input_img)

    if is_empty_img(input_img.well_props.mask.og) or (input_img.well_props.mask is None):
        input_img.well_props.is_well = False
    else:
        input_img.well_props.is_well = True

        msg("Creating remaining masks:")

        bbox = get_bounding_box_obj(input_img.well_props.mask.og)  # Getting bbox of the mask
        input_img.well_props.bounding_box = bbox

        msg("Creating cropped mask")
        input_img.well_props.mask.cropped = input_img.well_props.mask.og[bbox.x1:bbox.x2 + 1, bbox.y1:bbox.y2 + 1]

        msg("Creating masked image (original)")
        dilated_mask = binary_dilation(input_img.well_props.mask.og, disk(10))
        masked = dilated_mask * input_img.og
        input_img.well_props.mask.masked = masked

        msg("Creating masked image (cropped)")
        input_img.well_props.mask.cropped_masked = masked[bbox.x1:bbox.x2 + 1, bbox.y1:bbox.y2 + 1]

        input_img.processed = input_img.processed[bbox.x1:bbox.x2 + 1, bbox.y1:bbox.y2 + 1]
    msg("Created remaining masks")
    return input_img

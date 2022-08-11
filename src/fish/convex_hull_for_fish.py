import numpy as np
from skimage.morphology import convex_hull_image, binary_dilation, disk

from src.fish.get_objects import keep_largest_object
from src.models import InputImage, BoundingBox
from src.terminal_msg import show_img, msg
from src.well import get_bounding_box_coords


def convex_hull_for_fish(input_img: InputImage) -> InputImage:
    """
    Notes:  - uses images from the '.processed' image not the '.binary' attributes
            - stores images in the '.fish_props.mask' attributes

    :param input_img:
    :return: InputImage object with mask for the fish
    """
    msg("Getting convex hull for fish")

    hull = fish_convex_hull(input_img.processed)
    masked = hull * input_img.well_props.mask.cropped_masked
    bbox = get_bounding_box_coords(hull)

    input_img.fish_props.mask.og = hull.copy().astype(np.uint8)
    input_img.binary = hull.copy().astype(np.uint8)

    input_img.fish_props.mask.masked = masked.copy().astype(np.uint8)
    input_img.processed = masked.copy().astype(np.uint8)

    input_img.fish_props.bounding_box = BoundingBox(bbox[0], bbox[1], bbox[2], bbox[3])

    msg("Stored fish mask & bounding box")
    return input_img


def fish_convex_hull(binary_img: np.ndarray) -> np.ndarray:
    one_object_img = keep_largest_object(binary_img)

    hull = convex_hull_image(one_object_img)
    hull = binary_dilation(hull, disk(20))

    return hull.astype(np.uint8)

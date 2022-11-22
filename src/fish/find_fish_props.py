import cv2
import numpy as np
from scipy.signal import wiener
from skimage.exposure import equalize_adapthist, adjust_gamma
from skimage.filters._unsharp_mask import unsharp_mask
from skimage.morphology import binary_closing, disk, convex_hull_image, binary_opening

from src.utils.rangefilter import range_filter
from .is_fish import is_fish
from .get_eyes import get_eyes
from .get_head import should_be_rotated, get_head
from .remove_container import iterative_dilation, get_meniscus_effect_
from ..models import InputImage, BoundingBox
from ..utils import keep_largest_object, get_bounding_box_obj, normalize_0_1, \
    normalize_0_255, yen_th, msg, show_img, iterative_closing, iterative_opening


def find_fish_props(input_img: InputImage) -> InputImage:
    msg("Searching for fish properties")

    input_img = get_possible_fish(input_img)

    if not is_fish(input_img.fish_props.mask.cropped, input_img.well_props.mask.cropped):
        input_img.fish_props.has_fish = False
        return input_img
    else:
        input_img.fish_props.has_fish = True

    input_img = get_eyes(input_img)

    return input_img


def get_possible_fish(input_img: InputImage) -> InputImage:
    msg("Localizing potential embryo")

    msg("Applying range-filter")
    sharpened = unsharp_mask(input_img.processed, radius=2)  # Sharpening
    input_img.processed = range_filter(sharpened, input_img.well_props.mask.cropped)  # Range-filter
    input_img.processed = normalize_0_1(input_img.processed)  # Normalizing for wiener
    input_img.processed = equalize_adapthist(input_img.processed)  # Equalizing

    msg("Applying wiener-filter")
    input_img.processed = wiener(input_img.processed, mysize=25)  # denoising with wiener filter
    input_img.processed = normalize_0_255(input_img.processed)  # Normalizing and sharpening for thresholding
    input_img.processed = unsharp_mask(input_img.processed, radius=2)  # Sharpening
    wiener_filtered = adjust_gamma(input_img.processed, 1.5)

    msg("Applying yen-threshold")
    binary_img = yen_th(input_img.processed)  # Yen-thresholding

    binary_img = binary_closing(binary_img, disk(2))  # Closing

    msg("Removing meniscus")
    meniscus = get_meniscus_effect_(binary_img, input_img.well_props.mask.cropped).astype(float)
    input_img.fish_props.meniscus = meniscus  # TEMP

    binary_img = binary_img - meniscus

    msg("Keeping only the possible fish")
    binary_img = keep_largest_object(binary_img, filled=True).astype(bool)

    # Creating convex hull for the fish
    msg("Convex hull for mask")
    convex_mask = iterative_dilation(convex_hull_image(binary_img), 4, disk(5))  #

    # Inner bbox (fish's bbox inside well's bbox)
    msg("Bounding box of fish")
    bbox_well_relative = get_bounding_box_obj(convex_mask)
    input_img.fish_props.bounding_box_well = bbox_well_relative

    # Refining mask -> removing holes and small objects
    msg("Refining mask")
    mask = bbox_well_relative.bound_img(binary_img)
    mask = iterative_closing(mask, 10, disk(5))
    mask = keep_largest_object(mask, filled=True)
    mask = iterative_opening(mask, 10, disk(5))
    mask = keep_largest_object(mask, filled=True)
    input_img.fish_props.mask.cropped = mask

    # Creating convex hull for the fish
    msg("Convex hull for mask")
    convex_mask = iterative_dilation(convex_hull_image(mask), 4, disk(5))
    input_img.fish_props.mask.og = convex_mask  # Storing as og mask (relative to the well)

    # Bbox relative to original image
    msg("Bounding box from OG")
    bbox_og_relative = BoundingBox(input_img.well_props.bounding_box.x1 + bbox_well_relative.x1,
                                   input_img.well_props.bounding_box.y1 + bbox_well_relative.y1,
                                   input_img.well_props.bounding_box.x1 + bbox_well_relative.x2,
                                   input_img.well_props.bounding_box.y1 + bbox_well_relative.y2)
    input_img.fish_props.bounding_box_og = bbox_og_relative

    # Storing image of original (masked) image cropped to display only the fish
    input_img.fish_props.cropped_og = input_img.well_props.mask.masked[bbox_og_relative.x1:bbox_og_relative.x2,
                                      bbox_og_relative.y1:bbox_og_relative.y2] * convex_mask
    input_img.processed = mask * input_img.fish_props.cropped_og

    return input_img

import cv2
import numpy as np
from scipy.signal import wiener
from skimage.exposure import equalize_adapthist
from skimage.filters._unsharp_mask import unsharp_mask
from skimage.morphology import binary_closing, disk, convex_hull_image

from src.utils.rangefilter import range_filter
from .get_head import should_be_rotated, get_head
from .remove_container import iterative_dilation, get_meniscus_effect_
from ..models import InputImage, BoundingBox
from ..utils import keep_largest_object, get_bounding_box_obj, normalize_0_1, \
    normalize_0_255, yen_th, msg, show_img


def find_fish_props(input_img: InputImage) -> InputImage:
    msg("Searching for fish properties")

    msg("Applying range-filter")
    sharpened = unsharp_mask(input_img.processed, radius=2)  # Sharpening
    input_img.processed = range_filter(sharpened, input_img.well_props.mask.cropped)  # Range-filter
    input_img.processed = normalize_0_1(input_img.processed)  # Normalizing for wiener
    input_img.processed = equalize_adapthist(input_img.processed)  # Equalizing

    msg("Applying wiener-filter")
    input_img.processed = wiener(input_img.processed, mysize=30)  # denoising with wiener filter
    input_img.processed = normalize_0_255(input_img.processed)  # Normalizing and sharpening for thresholding
    input_img.processed = unsharp_mask(input_img.processed, radius=2)  # Sharpening

    msg("Applying yen-threshold")
    binary_img = yen_th(input_img.processed)  # Yen-thresholding
    # show_img(binary_img, 'th')

    # Get convex hull of fish
    binary_img = binary_closing(binary_img, disk(2))  # Closing
    # show_img(binary_img, 'closing')

    msg("Removing meniscus")
    meniscus = get_meniscus_effect_(binary_img, input_img.well_props.mask.cropped).astype(float)
    binary_img = binary_img - meniscus

    msg("Keeping only the possible fish")
    binary_img = keep_largest_object(binary_img, filled=True).astype(bool)
    # show_img(binary_img, 'klo')

    # Creating convex hull for the fish
    convex_mask = iterative_dilation(convex_hull_image(binary_img), 6, disk(5))  #

    input_img.fish_props.mask.og = convex_mask  # Storing as og mask (relative to the well)
    # show_img(convex, 'convex')

    # Inner bbox (fish's bbox inside well's bbox)
    bbox_well_relative = get_bounding_box_obj(convex_mask)
    input_img.fish_props.bounding_box_well = bbox_well_relative

    # Bbox relative to original image
    bbox_og_relative = BoundingBox(input_img.well_props.bounding_box.x1 + bbox_well_relative.x1,
                                   input_img.well_props.bounding_box.y1 + bbox_well_relative.y1,
                                   input_img.well_props.bounding_box.x1 + bbox_well_relative.x2,
                                   input_img.well_props.bounding_box.y1 + bbox_well_relative.y2)
    input_img.fish_props.bounding_box_og = bbox_og_relative

    # Storing image of original (masked) image cropped to display only the fish
    input_img.fish_props.cropped_og = input_img.well_props.mask.masked[
                                      bbox_og_relative.x1:bbox_og_relative.x2,
                                      bbox_og_relative.y1:bbox_og_relative.y2
                                      ]

    # Storing position parameters of the fish
    input_img.fish_props.rotated = should_be_rotated(binary_img)
    input_img.fish_props.head = get_head(binary_img)[1]

    input_img.fish_props.mask.cropped = bbox_well_relative.bound_img(binary_img)
    input_img.processed = binary_img

    return input_img


def get_mask_from_meniscus(meniscus: np.ndarray) -> np.ndarray:
    inv = ~meniscus
    return keep_largest_object(inv)

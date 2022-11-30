import numpy as np
from scipy.signal import wiener
from skimage.exposure import equalize_adapthist
from skimage.filters._unsharp_mask import unsharp_mask
from skimage.morphology import binary_closing, disk, convex_hull_image

from src.models import InputImage, BoundingBox
from src.utils import msg, range_filter, normalize_0_1, normalize_0_255, yen_th, keep_largest_object, \
    iterative_dilation, get_bounding_box_obj, iterative_closing, iterative_opening, show_img
from .remove_container import get_meniscus_effect__


def get_possible_fish(input_img: InputImage) -> InputImage:
    msg("Localizing potential embryo")

    msg("Applying range-filter")
    """    sharpened = unsharp_mask(input_img.processed, radius=2)  # Sharpening
    input_img.processed = range_filter(sharpened, input_img.well_props.mask.cropped)  # Range-filter
    input_img.processed = normalize_0_1(input_img.processed)  # Normalizing for wiener
    input_img.processed = equalize_adapthist(input_img.processed)  # Equalizing"""
    input_img.processed = edge_detection(input_img.processed) * input_img.well_props.mask.cropped
    show_img(input_img.processed)

    msg("Applying wiener-filter")
    input_img.processed = wiener_denoising(input_img.processed)  # Denoising

    msg("Applying yen-threshold")
    binary_img = yen_th(input_img.processed)  # Yen-thresholding

    binary_img = binary_closing(binary_img, disk(2))

    msg("Removing meniscus")
    meniscus = get_meniscus_effect__(binary_img, input_img.well_props.mask.cropped).astype(float)
    input_img.fish_props.meniscus = meniscus  # TEMP

    binary_img = binary_img - meniscus

    msg("Keeping only the possible fish")
    binary_img = keep_largest_object(binary_img, filled=True).astype(bool)

    # Creating convex hull for the fish
    msg("Convex hull for mask")
    convex_mask = iterative_dilation(convex_hull_image(binary_img), 4, disk(5))  # Dilating hull to include eyes

    # Inner bbox (fish's bbox in well's bbox)
    msg("Bounding box of fish")
    bbox_well_relative = get_bounding_box_obj(convex_mask)
    input_img.fish_props.bounding_box_well = bbox_well_relative

    # Refining mask -> removing holes and small objects
    msg("Refining mask")
    mask = bbox_well_relative.bound_img(binary_img)
    mask = iterative_closing(mask, 8, disk(5))
    mask = keep_largest_object(mask, filled=True)
    mask = iterative_opening(mask, 8, disk(5))
    mask = keep_largest_object(mask, filled=True)
    input_img.fish_props.mask.cropped = mask

    # Creating convex hull for the fish
    msg("Convex hull for mask")
    convex_mask = iterative_dilation(convex_hull_image(mask), 4, disk(5))
    input_img.fish_props.mask.og = convex_mask  # Storing as og mask (relative to the well)

    # Bbox relative to original image TODO DELETE THIS!
    msg("Bounding box from OG")
    bbox_og_relative = BoundingBox(input_img.well_props.bounding_box.x1 + bbox_well_relative.x1,
                                   input_img.well_props.bounding_box.y1 + bbox_well_relative.y1,
                                   input_img.well_props.bounding_box.x1 + bbox_well_relative.x2,
                                   input_img.well_props.bounding_box.y1 + bbox_well_relative.y2)
    input_img.fish_props.bounding_box_og = bbox_og_relative

    # Storing image of original (masked) image cropped to display only the fish
    input_img.fish_props.cropped_og = input_img.well_props.mask.masked[
                                      bbox_og_relative.x1:bbox_og_relative.x2,
                                      bbox_og_relative.y1:bbox_og_relative.y2
                                      ] * convex_mask
    input_img.processed = mask * input_img.fish_props.cropped_og

    return input_img


def wiener_denoising(img: np.ndarray) -> np.ndarray:
    img = wiener(img, mysize=30)  # Denoising with wiener filter
    img = normalize_0_255(img)  # Normalizing and sharpening for thresholding
    img = unsharp_mask(img, radius=2)  # Sharpening
    return img


def edge_detection(img: np.ndarray) -> np.ndarray:
    sharpened = unsharp_mask(img, radius=2)  # Sharpening
    img = range_filter(sharpened)  # Range-filter
    img = normalize_0_1(img)  # Normalizing for wiener
    return equalize_adapthist(img)

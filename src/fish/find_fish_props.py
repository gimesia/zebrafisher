import numpy as np
from scipy import ndimage
from scipy.ndimage import binary_fill_holes
from skimage.exposure import equalize_adapthist
from skimage.filters.ridges import meijering
from skimage.filters.thresholding import threshold_isodata
from skimage.morphology import disk, binary_closing, binary_opening, convex_hull_image, binary_dilation, square, \
    binary_erosion, remove_small_objects
from skimage.restoration import rolling_ball

from src.filters import sharpen_image, sobel_edges, yen_thresholding, sobel, yen_th, sharpen_img
from src.models import InputImage
from src.utils import get_bounding_box, keep_largest_object
from src.utils.terminal_msg import msg, show_img
from .convex_hull_for_fish import convex_hull_for_fish
from .is_fish import is_fish
from .remove_background import remove_background
from .well_meniscus import remove_meniscus


def find_fish_props(input_img: InputImage) -> InputImage:
    msg("Searching fish properties")

    input_img = remove_background(input_img)

    input_img = yen_thresholding(input_img)
    filled = binary_fill_holes(binary_closing(binary_fill_holes(input_img.processed), disk(10))).astype(float)
    input_img.processed = filled * input_img.well_props.mask.cropped

    input_img.fish_props.mask.og = convex_hull_image(input_img.processed)  # Fish hull ready to be analyzed further

    if not is_fish(input_img.fish_props.mask.og):
        print("NOT FISH")
        input_img = refine_oversized_hull(input_img)

    # input_img = get_fish_convex_mask(input_img)
    # input_img = refine_fish_convex_mask(input_img)
    # input_img = refine_fish_mask(input_img)

    return input_img


def refine_oversized_hull(input_img: InputImage) -> InputImage:
    return input_img


"""
def get_fish_convex_mask(input_img: InputImage) -> InputImage:
    msg("Creating fish convex mask")
    for i in range(6):
        # show_img(input_img.processed, "before")
        input_img = sharpen_image(input_img)
        input_img = sobel_edges(input_img)
        input_img = yen_thresholding(input_img)
        input_img = remove_meniscus(input_img)
        input_img = convex_hull_for_fish(input_img)
        if is_fish(input_img.binary):
            return input_img


    if input_img.fish_props.mask.og.nonzero()[0].size > input_img.well_props.mask.cropped.nonzero()[0].size * 0.25:
        Warning("FISH_MASK BIGGER THAN QUARTER OF THE WELL_MASK")
        input_img = correct_fish_mask(input_img)

    return input_img


def refine_fish_convex_mask(input_img: InputImage) -> InputImage:
    bbox = input_img.fish_props.bounding_box
    remaining = np.zeros_like(input_img.fish_props.mask.masked)
    edges = sobel(input_img.fish_props.mask.masked[bbox.x1:bbox.x2, bbox.y1:bbox.y2])

    se = disk(2)
    x = binary_closing(binary_opening(yen_th(edges), se), se).astype(float)
    hull = convex_hull_image(x)

    remaining[bbox.x1:bbox.x2, bbox.y1:bbox.y2] = hull
    input_img.fish_props.bounding_box = get_bounding_box(remaining)
    input_img.fish_props.mask.og = remaining
    input_img.fish_props.mask.masked = remaining * input_img.well_props.mask.cropped_masked
    input_img.fish_props.mask.cropped = input_img.fish_props.mask.og[bbox.x1:bbox.x2, bbox.y1:bbox.y2]
    input_img.fish_props.mask.cropped_masked = input_img.fish_props.mask.masked[bbox.x1:bbox.x2, bbox.y1:bbox.y2]

    input_img.binary = input_img.binary[bbox.x1:bbox.x2, bbox.y1:bbox.y2] * input_img.fish_props.mask.cropped
    input_img.processed = input_img.fish_props.mask.cropped_masked.copy()

    return input_img


def refine_fish_mask(input_img: InputImage) -> InputImage:
    # Sharpening
    shp = sharpen_img(input_img.fish_props.mask.cropped_masked)
    # Finding background
    bg = rolling_ball(shp)
    # Removing background
    no_bg = shp - bg

    # Equalizing
    equalized = equalize_adapthist(no_bg)

    # Applying Meijering-vessel filter
    mej = meijering(equalized) * input_img.fish_props.mask.cropped

    # Isodata-thresholding
    iso_threshold = mej > threshold_isodata(mej)

    # Binary morphological operations
    opened = binary_opening(iso_threshold)
    dilated = binary_dilation(opened, disk(10))
    closed = binary_closing(dilated, disk(3))
    filled = binary_fill_holes(keep_largest_object(closed))

    masked = filled * input_img.fish_props.mask.cropped_masked

    input_img.fish_props.mask.cropped = filled
    input_img.fish_props.mask.cropped_masked = masked
    input_img.processed = masked

    return input_img
"""

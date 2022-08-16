import numpy as np
from skimage.morphology import disk, binary_closing, binary_opening, convex_hull_image

from src.filters import sharpen_image, sobel_edges, yen_thresholding, sobel, yen_th
from src.models import InputImage
from src.utils.terminal_msg import msg
from src.utils import get_bounding_box
from src.well.find_well_props import find_well_props

from .convex_hull_for_fish import convex_hull_for_fish
from .is_fish import is_fish
from .well_meniscus import remove_meniscus


def find_fish_props(input_img: InputImage) -> InputImage:
    msg("Searching fish properties")
    # input_img = gaussian_high_pass_filter(input_img)
    input_img = get_fish_convex_mask(input_img)
    input_img = refine_fish_convex_mask(input_img)

    return input_img


def get_fish_convex_mask(input_img: InputImage) -> InputImage:
    msg("Creating fish convex mask")
    for i in range(6):
        input_img = sharpen_image(input_img)
        input_img = sobel_edges(input_img)
        input_img = yen_thresholding(input_img)
        input_img = remove_meniscus(input_img)
        input_img = convex_hull_for_fish(input_img)
        if is_fish(input_img.binary):
            return input_img

    """if input_img.fish_props.mask.og.nonzero()[0].size > input_img.well_props.mask.cropped.nonzero()[0].size * 0.25:
        Warning("FISH_MASK BIGGER THAN QUARTER OF THE WELL_MASK")
        input_img = correct_fish_mask(input_img)"""

    return input_img


def refine_fish_convex_mask(input_img: InputImage) -> InputImage:
    bbox = input_img.fish_props.bounding_box
    remaining = np.zeros_like(input_img.fish_props.mask.masked)
    edges = sobel(input_img.fish_props.mask.masked[bbox.x1:bbox.x2, bbox.y1:bbox.y2])

    se = disk(2)
    x = binary_closing(binary_opening(yen_th(edges), se), se).astype(float)
    hull = convex_hull_image(x)

    remaining[bbox.x1:bbox.x2, bbox.y1:bbox.y2] = hull

    input_img.binary = remaining.copy()
    input_img.fish_props.mask.og = remaining.copy()
    input_img.fish_props.mask.masked = remaining * input_img.well_props.mask.cropped_masked
    input_img.fish_props.bounding_box = get_bounding_box(remaining)
    input_img.processed = remaining * input_img.well_props.mask.cropped_masked.copy()

    return input_img


if __name__ == '__main__':
    a = InputImage("zf3.jpg")
    a = find_well_props(a)
    a = find_fish_props(a)

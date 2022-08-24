from scipy.ndimage import binary_fill_holes
from skimage.filters import unsharp_mask, meijering
from skimage.measure import label, find_contours
from skimage.morphology import disk, binary_closing, convex_hull_image, binary_dilation, remove_small_objects, \
    binary_erosion, binary_opening

from src.filters import yen_th, sobel
from src.models import InputImage
from src.utils import keep_largest_object_convex, get_bounding_box_obj, keep_largest_object
from src.utils.terminal_msg import msg
from .is_fish import is_fish
from .remove_background import remove_background


def find_fish_props(input_img: InputImage) -> InputImage:
    msg("Searching fish properties")

    input_img = remove_background(input_img)

    th = yen_th(input_img.processed)

    closed = binary_closing(th, disk(3))
    filled = binary_fill_holes(closed)
    filled_masked = filled * input_img.well_props.mask.cropped
    input_img.processed = filled_masked

    largest_object = keep_largest_object(filled_masked)
    fish_mask = convex_hull_image(largest_object).astype(float)

    input_img.fish_props.mask.og = fish_mask

    for i in range(6):
        if is_fish(input_img.fish_props.mask.og):
            break
        input_img = refine_oversized_hull(input_img, step=(i + 1))

    dilated_mask = binary_dilation(input_img.fish_props.mask.og, disk(20))
    input_img.fish_props.mask.masked = dilated_mask * input_img.well_props.mask.cropped_masked
    masked = dilated_mask * input_img.well_props.mask.cropped_masked

    input_img.fish_props.mask.masked = masked
    input_img.processed = masked

    input_img = refine_fish_mask(input_img)

    return input_img


def refine_oversized_hull(input_img: InputImage, step=0) -> InputImage:
    msg(f"Refining convex hull of fish, step #{step}")
    hull = input_img.fish_props.mask.og
    well_masked = input_img.well_props.mask.cropped_masked

    um = unsharp_mask(hull * well_masked, amount=10 + (step * 0.75), radius=2)
    meijered = meijering(um)
    th = yen_th(meijered)
    proc = th * hull

    largest_obj_convex = keep_largest_object_convex(proc)
    input_img.fish_props.mask.og = largest_obj_convex

    return input_img


def refine_fish_mask(input_img: InputImage) -> InputImage:
    msg("Refining fish mask")
    um = unsharp_mask(input_img.fish_props.mask.masked, amount=20, radius=3)
    sob = sobel(um)
    th = yen_th(sob)
    refined = remove_small_objects(th)

    dilated_mask = binary_dilation(input_img.fish_props.mask.og, disk(20))
    eroded_masked = refined * binary_erosion(dilated_mask, disk(10))
    closed_masked = binary_closing(eroded_masked, disk(5))

    refined_filled = binary_fill_holes(closed_masked)
    refined_masked = remove_small_objects(
        binary_opening(refined_filled, disk(3))) * input_img.well_props.mask.cropped_masked

    labeled = label(refined_masked.astype(bool))
    largest_label = keep_largest_object(labeled)
    contour = find_contours(largest_label)
    bbox = get_bounding_box_obj(largest_label)

    input_img.fish_props.contours.body = contour
    input_img.fish_props.bounding_box = bbox
    input_img.fish_props.mask.cropped = largest_label
    input_img.fish_props.mask.cropped_masked = largest_label * input_img.well_props.mask.cropped_masked

    return input_img
